# single node speed test on 1/1000 of the data
time bzcat ~/osm-planet.bz2 | ./mapper.py | sort | ./reducer.py > part-00000
