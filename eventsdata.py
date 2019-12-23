#coding:utf-8

from kafka import KafkaConsumer,TopicPartition
from cassandra.cluster import Cluster
import wx


import conf as co


consumer = KafkaConsumer(co.ka_topic,bootstrap_servers=co.ka_server)


#cluster = Cluster(co.ca_host,co.ca_port)
#session = cluster.connect()
#session.set_keyspace(co.ca_keyspace)





def GetEvents(win, evt_zenoss_new_event):

    for m in consumer:
        evt = evt_zenoss_new_event(m=m.value)
        wx.PostEvent(win, evt)





def GetEventsTopic():
    #for row in session.execute('SELECT data FROM events_buff'):
        #print row[0]
        #yield row[0]
    yield (0,0,0,0,0,0,0,0,0,0,0)





"""
def GetEventsTopic():

    tp = TopicPartition(co.ka_topic, 0)
    consumer_h.assign([tp])
    consumer_h.seek_to_end(tp)
    lastOffset = consumer_h.position(tp)
    consumer_h.seek_to_beginning(tp)

    for m in consumer_h:
        yield m.value
        if m.offset == lastOffset - 1:
            break
"""








if __name__ == '__main__':

    for m in consumer:
        print m.value

