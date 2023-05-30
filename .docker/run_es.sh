docker run --rm --net elastic -p 9200:9200 -p 9300:9300 -e "xpack.security.enabled=false" -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.7.0

# docker run --name kib-01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.8.0

# docker network create elastic


# docker run \
#   --name kibana \
#   --publish 5601:5601 \
#   --network elastic \
#   --env "ELASTICSEARCH_HOSTS=http://localhost:9200" \
#   docker.elastic.co/kibana/kibana:8.8.0