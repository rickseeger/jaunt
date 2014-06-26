hdfs dfs -rm -r osm-out
hadoop jar /opt/cloudera/parcels/CDH/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming.jar \
    "-Dstream.recordreader.begin=<node" \
    "-Dstream.recordreader.end=</node>" \
    -inputreader "StreamXmlRecordReader" \
    -input /user/ubuntu/osm-planet.bz2 \
    -mapper mapper.py \
    -file mapper.py \
    -reducer reducer.py \
    -file reducer.py \
    -output osm-out \
    -numReduceTasks 1
