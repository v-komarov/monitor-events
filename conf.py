#coding:utf-8

# kafka
ka_server = ['kafka-node1:9092','kafka-node2:9092','kafka-node3:9092']
ka_topic = 'zenoss'

# сервисы ЗКЛ
zkl_service = 'http://10.6.0.22:8000/equipment/devices/apidata/'


# Cassandra
ca_host = ['10.6.0.165',]
ca_port = 9042
ca_keyspace = "events"