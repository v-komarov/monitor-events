#coding:utf-8

import wx
import urllib2, urllib
import json
import	sys

from conf import zkl_service


class DevicesFrame(wx.Frame):
    def __init__(self,ips):
        wx.Frame.__init__(self, None, 1, u"Информация по устройствам", size=(600,400), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.MId=wx.NewId()



        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.Bitmap("icon.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        self.panel = wx.Panel(self, wx.ID_ANY)

        self.lst = DevicesList(self.panel,-1)
        self.lst.appendRow(ips)

        topSizer = wx.BoxSizer(wx.VERTICAL)
        toolsizer = wx.BoxSizer(wx.HORIZONTAL)
        gbsizer = wx.BoxSizer(wx.HORIZONTAL)
        ssizer = wx.BoxSizer(wx.HORIZONTAL)
        gridsizer = wx.BoxSizer(wx.HORIZONTAL)


        gridsizer.Add(self.lst, 0, wx.ALL)

        toolsizer.Add(gbsizer, 0, wx.ALL)
        toolsizer.Add(ssizer, 0, wx.ALL)

        topSizer.Add(toolsizer, 0, wx.ALL)
        topSizer.Add(gridsizer, 0, wx.ALL)

        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)







class DevicesList(wx.ListCtrl):

    def __init__(self, parent, ID, pos=(0,0), size=(600,400), style=wx.LC_REPORT|wx.SUNKEN_BORDER):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)

        self.InsertColumn(0, u"Название")
        self.InsertColumn(1, u"ip")
        self.InsertColumn(2, u"Адрес")
        self.InsertColumn(3, u"Портов используется")
        self.InsertColumn(4, u"Портов технологических")
        self.InsertColumn(5, u"Портов в резерве")


        self.SetColumnWidth(0, 150)
        self.SetColumnWidth(1, 150)
        self.SetColumnWidth(2, 200)
        self.SetColumnWidth(3, 100)
        self.SetColumnWidth(4, 100)
        self.SetColumnWidth(5, 100)





    def appendRow(self, ips):


        ### суммарные значения
        use = 0
        tech = 0
        reserv = 0

        for ip in list(ips):

            response = urllib2.urlopen('{}?action=get_zkllist&ipaddress={}'.format(zkl_service,ip))
            data = response.read()
            response.close()
            j = json.loads(data)



            if len(j) != 0:

                j = j[0]

                pos = self.InsertStringItem(0,j['ip'])

                self.SetStringItem(pos, 0, j['sysname'])
                self.SetStringItem(pos, 1, j['ip'])
                self.SetStringItem(pos, 2, j['address'])
                self.SetStringItem(pos, 3, u"{}".format(j['port_use']))
                self.SetStringItem(pos, 4, u"{}".format(j['port_tech']))
                self.SetStringItem(pos, 5, u"{}".format(j['port_reserv']))


                use += j['port_use']
                tech += j['port_tech']
                reserv += j['port_reserv']

        pos = self.InsertStringItem(sys.maxint, u"")

        self.SetStringItem(pos, 0, u"")
        self.SetStringItem(pos, 1, u"")
        self.SetStringItem(pos, 2, u"")
        self.SetStringItem(pos, 3, u"{}".format(use))
        self.SetStringItem(pos, 4, u"{}".format(tech))
        self.SetStringItem(pos, 5, u"{}".format(reserv))


        query_args = { 'action':'writeaddressstr', 'iplist':";".join(list(ips)) }
        data = urllib.urlencode(query_args)
        request = urllib2.Request(zkl_service, data)
        response = urllib2.urlopen(request)
        data = response.read()
        response.close()
        print json.loads(data)

