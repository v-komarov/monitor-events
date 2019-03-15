#coding:utf-8

import json
import wx.grid



class EventsList(wx.grid.Grid):

    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1)
        self.moveTo = None

        maxrow = 5000

        self.CreateGrid(100, 12, selmode=wx.grid.Grid.SelectRows)
        self.EnableEditing(False)

        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour("YELLOW")

        attr2 = wx.grid.GridCellAttr()
        attr2.SetBackgroundColour("RED")

        for row in range(maxrow):
            self.SetRowLabelValue(row, str(row))

        #
        self.SetColSize(0, 150)
        self.SetColSize(1, 150)
        self.SetColSize(2, 200)
        self.SetColSize(3, 200)
        self.SetColSize(4, 200)
        self.SetColSize(5, 200)
        self.SetColSize(6, 150)
        self.SetColSize(7, 200)
        self.SetColSize(8, 200)
        self.SetColSize(9, 100)
        self.SetColSize(10, 100)
        self.SetColSize(11, 300)

        """

            if eval(row[4]) < 0 and eval(row[4]) >= (-1000):
                self.SetRowAttr(n, attr)
            elif eval(row[4]) < (-1000):
                self.SetRowAttr(n, attr2)

            n = n + 1


        """

        self.SetColLabelValue(0, "LastSeen")
        self.SetColLabelValue(1, "FirstSeen")
        self.SetColLabelValue(2, "DeviceGroup")
        self.SetColLabelValue(3, "DeviceClass")
        self.SetColLabelValue(4, "EventClass")
        self.SetColLabelValue(5, "DeviceSystem")
        self.SetColLabelValue(6, "DeviceNetAddress")
        self.SetColLabelValue(7, "DeviceLocation")
        self.SetColLabelValue(8, "ElementIdentifier")
        self.SetColLabelValue(9, "Status")
        self.SetColLabelValue(10, "Severity")
        self.SetColLabelValue(11, "Summary")


        self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)



    def zenoss_evt(self, evt):
        print evt.m
        e = json.loads(evt.m)
        print e['evid']
        self.appendRow(e)


    def appendRow(self, e):

        if e['severity'] == 'Critical' and e['status'] == 'New':

            self.InsertRows(0,1,updateLabels = False)
            #self.SetRowLabelValue(0, e['evid'])

            self.SetCellValue(0, 0, e['last_seen'])
            self.SetCellValue(0, 1, e['first_seen'])
            self.SetCellValue(0, 2, e['device_group'])
            self.SetCellValue(0, 3, e['device_class'])
            self.SetCellValue(0, 4, e['event_class'])
            self.SetCellValue(0, 5, e['device_system'])
            self.SetCellValue(0, 6, e['device_net_address'])
            self.SetCellValue(0, 7, e['device_location'])
            self.SetCellValue(0, 8, e['element_identifier'])
            self.SetCellValue(0, 9, e['status'])
            self.SetCellValue(0, 10, e['severity'])
            self.SetCellValue(0, 11, e['summary'])
