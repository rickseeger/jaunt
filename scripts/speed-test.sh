# single node speed test on 1/1000 of the data
time bzcat ../data/san-francisco.xml.bz2 | ./mapper.py | sort | ./reducer.py > part-00000
