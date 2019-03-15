#coding:utf-8

import wx.grid


class EventsList(wx.grid.Grid):

    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1)
        self.moveTo = None

        maxrow = 5000

        self.CreateGrid(maxrow, 12, selmode=wx.grid.Grid.SelectRows)
        self.EnableEditing(False)

        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour("YELLOW")

        attr2 = wx.grid.GridCellAttr()
        attr2.SetBackgroundColour("RED")

        for row in range(maxrow):
            self.SetRowLabelValue(row, str(row))

        #
        self.SetColSize(0, 70)
        self.SetColSize(1, 70)
        self.SetColSize(2, 200)
        self.SetColSize(3, 200)
        self.SetColSize(4, 200)
        self.SetColSize(5, 200)
        self.SetColSize(6, 150)
        self.SetColSize(7, 200)
        self.SetColSize(8, 100)
        self.SetColSize(9, 100)
        self.SetColSize(10, 300)
        self.SetColSize(11, 100)

        """
        n = 0
        for row in ShowAbonentAll(UlDom):
            self.SetCellValue(n, 0, row[1])
            self.SetCellValue(n, 1, row[2])
            self.SetCellValue(n, 2, row[3])
            self.SetCellValue(n, 3, row[4])
            self.SetCellValue(n, 4, row[7])
            self.SetCellValue(n, 5, row[10])

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
        self.SetColLabelValue(8, "Status")
        self.SetColLabelValue(9, "Severity")
        self.SetColLabelValue(10, "Summary")
        self.SetColLabelValue(11, "Source")


        self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)




    def zenoss_event(self,evt):
        pass