#coding:utf-8

# kafka
ka_server = ['kafka-node1:9092','kafka-node2:9092','kafka-node3:9092']
ka_topic = 'zenoss'

# сервисы ЗКЛ
zkl_service = 'http://10.6.0.22:8000/equipment/devices/apidata/'

# Постгрес
pg_host = '10.6.0.246'
pg_port= 6432
pg_base = 'monitor'
pg_user = 'muser'
pg_password = 'av4uchau'

# memcached
#memcach = [('10.3.1.46',11211),]
memcach = [('10.6.3.54',11211),]