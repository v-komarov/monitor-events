#coding:utf-8


import wx
import wx.lib.newevent as NE
import threading

from gridtable import EventsList
from eventsdata import GetEvents


evt_zenoss_new_event, EVT_ZENOSS_NEW_EVENT = NE.NewEvent()


class MFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, 1, "monitor-events", size=(700,500), style=wx.DEFAULT_FRAME_STYLE)
        self.MId=wx.NewId()

        self.Bind(EVT_ZENOSS_NEW_EVENT, self.zenoss_event)
        t = threading.Thread(target=GetEvents, args=(self, evt_zenoss_new_event))
        t.setDaemon(True)
        t.start()

        self.panel = wx.Panel(self, wx.ID_ANY)

        self.el = EventsList(self.panel)

        gBtn = wx.Button(self.panel, 10, "Группировки", (-1,-1))
        cb = wx.ComboBox(self.panel, 500, "Все", (-1, -1), (160, -1), ['Все','Красноярск','Иркутск','Чита'], wx.CB_DROPDOWN)
        topSizer = wx.BoxSizer(wx.VERTICAL)
        toolsizer = wx.BoxSizer(wx.HORIZONTAL)
        gbsizer = wx.BoxSizer(wx.VERTICAL)
        ssizer = wx.BoxSizer(wx.VERTICAL)
        gridsizer = wx.BoxSizer(wx.HORIZONTAL)

        gbsizer.Add(gBtn, 0, wx.ALL, 5)
        ssizer.Add(cb, 0, wx.ALL, 5)

        gridsizer.Add(self.el, 0, wx.ALL)

        toolsizer.Add(gbsizer, 0, wx.ALL)
        toolsizer.Add(ssizer, 0, wx.ALL)

        topSizer.Add(toolsizer, 0, wx.ALL)
        topSizer.Add(gridsizer, 0, wx.ALL)

        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)




    def zenoss_event(self,evt):
        self.el.zenoss_evt(evt)




if __name__ == '__main__':

    class MyApp(wx.App):
        def OnInit(self):
            MainFrame = MFrame()
            MainFrame.Show(True)
            self.SetTopWindow(MainFrame)
            return True


    app = MyApp(False)
    app.MainLoop()

