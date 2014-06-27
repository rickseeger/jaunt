hdfs dfs -rm -r osm-out
hadoop jar /opt/cloudera/parcels/CDH/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming.jar \
    "-Dstream.recordreader.begin=<node" \
    "-Dstream.recordreader.end=</node>" \
    -inputreader "StreamXmlRecordReader" \
    -file mapper.py \
    -file reducer.py \
    -input /user/ubuntu/north-america.xml \
    -mapper mapper.py \
    -reducer reducer.py \
    -output osm-out \
    -numReduceTasks 1
