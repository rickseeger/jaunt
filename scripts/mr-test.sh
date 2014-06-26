# test map-reduce scripts
bzcat ../data/pacifica.xml.bz2 | ./mapper.py | sort | ./reducer.py > part-00000
