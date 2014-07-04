#!/usr/bin/python

#
# planet-fetcher.py
# Pulls down a copy of the Open Street Map database and copies it to
# HDFS. Various mirrors are attempted for direct download, most
# reliable first.
#

import hashlib
import urlgrabber
import time
import os
import logging
import subprocess
from planetmirrors import mirrors

logLevel = logging.DEBUG

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('miway.fetcher')
logger.setLevel(logLevel)


def getRemoteURL(url):
    logger.info('downloading %s' % url)
    start = time.time()
    try: 
        fileName = urlgrabber.urlgrab(url, config.localOSMPath)
        fileSize = os.path.getsize(fileName)
    except Exception, e:
        logger.warning('urlgrabber: %s' % e.strerror)
        return(None)
    elapsed = round(time.time() - start) + 1
    logger.debug('rcvd: %d bytes' % fileSize)
    logger.debug('time: %d seconds' % elapsed)
    logger.debug('speed: %d MB/s' % round((fileSize/1048576)/elapsed))
    return(fileName)


def HDFSPut(localPath, remotePath):
    logger.info('putting local %s to HDFS %s' % (localPath, remotePath))
    start = time.time()
    try:
        cmd = ['hdfs','dfs','-put', localPath, remotePath]
        out = subprocess.check_output(["hdfs","dfs","-put","-f",localPath,remotePath])
        if (len(out) == 0):
            out = 'file put succeeded'
        logger.info(format(out))
    except subprocess.CalledProcessError, e:
        logger.warning('HDFSPut: %s' % e.output.strip())
        return(None)
    fileSize = os.path.getsize(localPath)
    elapsed = round(time.time() - start) + 1
    logger.debug('sent: %d bytes' % fileSize)
    logger.debug('time: %d seconds' % elapsed)
    logger.debug('speed: %d MB/s' % round((fileSize/1048576)/elapsed))
    return(remotePath)
    

def main():
    
    planetFile = None
    for m in mirrors:
        planetFile = getRemoteURL(m)
        if (planetFile != None):
            break

    if (planetFile == None):
        logger.error('failed to download OSM file, giving up')
        return(1)
        
    if (HDFSPut(planetFile, config.remoteOSMPath) == None):
        logger.error('failed to put file to HDFS, exiting')
        return(1)

    return(0)


if __name__ == "__main__":
    main()
