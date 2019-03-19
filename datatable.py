#coding:utf-8

import sys
import json
import wx



class EventsList(wx.ListCtrl):

    def __init__(self, parent, ID, pos=(0,0), size=(2050,2000), style=wx.LC_REPORT|wx.SUNKEN_BORDER):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)


        self.InsertColumn(0, "evid")
        self.InsertColumn(1, "LastSeen")
        self.InsertColumn(2, "FirstSeen")
        self.InsertColumn(3, "DeviceGroup")
        self.InsertColumn(4, "DeviceClass")
        self.InsertColumn(5, "EventClass")
        self.InsertColumn(6, "DeviceSystem")
        self.InsertColumn(7, "DeviceNetAddress")
        self.InsertColumn(8, "DeviceLocation")
        self.InsertColumn(9, "ElementIdentifier")
        self.InsertColumn(10, "Status")
        self.InsertColumn(11, "Severity")
        self.InsertColumn(12, "Summary")


        self.SetColumnWidth(0, 20)
        self.SetColumnWidth(1, 150)
        self.SetColumnWidth(2, 150)
        self.SetColumnWidth(3, 200)
        self.SetColumnWidth(4, 200)
        self.SetColumnWidth(5, 200)
        self.SetColumnWidth(6, 200)
        self.SetColumnWidth(7, 150)
        self.SetColumnWidth(8, 200)
        self.SetColumnWidth(9, 200)
        self.SetColumnWidth(10, 100)
        self.SetColumnWidth(11, 100)
        self.SetColumnWidth(12, 300)



        self.bottom_item = None



    def zenoss_evt(self, evt):
        print evt.m

        zenoss_source = self.GetTopLevelParent().cb.GetStringSelection()

        e = json.loads(evt.m)
        pref = e['evid'].split('-')[0]
        if pref == "krsk" and zenoss_source == u"Красноярск":
            self.appendRow(e)
        elif pref == "irk" and zenoss_source == u"Иркутск":
            self.appendRow(e)
        elif pref == "chi" and zenoss_source == u"Чита":
            self.appendRow(e)
        elif zenoss_source == u"Все":
            self.appendRow(e)


    def appendRow(self, e):


        item = self.FindItem(-1,e['evid'])


        if e['severity'] == 'Critical' and e['status'] == 'New' and item == -1:


            pos = self.InsertStringItem(0,e['evid'])

            self.SetStringItem(pos, 0, e['evid'])
            self.SetStringItem(pos, 1, e['last_seen'])
            self.SetStringItem(pos, 2, e['first_seen'])
            self.SetStringItem(pos, 3, e['device_group'])
            self.SetStringItem(pos, 4, e['device_class'])
            self.SetStringItem(pos, 5, e['event_class'])
            self.SetStringItem(pos, 6, e['device_system'])
            self.SetStringItem(pos, 7, e['device_net_address'])
            self.SetStringItem(pos, 8, e['device_location'])
            self.SetStringItem(pos, 9, e['element_identifier'])
            self.SetStringItem(pos, 10, e['status'])
            self.SetStringItem(pos, 11, e['severity'])
            self.SetStringItem(pos, 12, e['summary'])

        elif item != -1:

            self.DeleteItem(item)

            pos = self.InsertStringItem(0,e['evid'])

            self.SetStringItem(pos, 0, e['evid'])
            self.SetStringItem(pos, 1, e['last_seen'])
            self.SetStringItem(pos, 2, e['first_seen'])
            self.SetStringItem(pos, 3, e['device_group'])
            self.SetStringItem(pos, 4, e['device_class'])
            self.SetStringItem(pos, 5, e['event_class'])
            self.SetStringItem(pos, 6, e['device_system'])
            self.SetStringItem(pos, 7, e['device_net_address'])
            self.SetStringItem(pos, 8, e['device_location'])
            self.SetStringItem(pos, 9, e['element_identifier'])
            self.SetStringItem(pos, 10, e['status'])
            self.SetStringItem(pos, 11, e['severity'])
            self.SetStringItem(pos, 12, e['summary'])



        if self.GetItemCount() > 5000:
            self.DeleteAllItems()



