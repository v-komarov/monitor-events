#coding:utf-8

from kafka import KafkaConsumer
import wx


import conf as co


consumer = KafkaConsumer(co.ka_topic,bootstrap_servers=co.ka_server)


def GetEvents(win, evt_zenoss_new_event):

    for m in consumer:
        evt = evt_zenoss_new_event(m=m.value)
        wx.PostEvent(win, evt)



if __name__ == '__main__':

    for m in consumer:
        print m.value

