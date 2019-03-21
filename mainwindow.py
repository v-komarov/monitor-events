#coding:utf-8


import wx
import wx.lib.newevent as NE
import threading

from datatable import EventsList
from eventsdata import GetEvents


evt_zenoss_new_event, EVT_ZENOSS_NEW_EVENT = NE.NewEvent()


class MFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, 1, "monitor-events", size=(700,500), style=wx.DEFAULT_FRAME_STYLE)
        self.MId=wx.NewId()

        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.Bitmap("icon.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        self.Bind(EVT_ZENOSS_NEW_EVENT, self.zenoss_event)
        t = threading.Thread(target=GetEvents, args=(self, evt_zenoss_new_event))
        t.setDaemon(True)
        t.start()

        self.panel = wx.Panel(self, wx.ID_ANY)

        self.lst = EventsList(self.panel,-1)

        gBtn = wx.Button(self.panel, 10, u"Группы", (-1,-1))
        cb_label = wx.StaticText(self.panel, id=wx.ID_ANY, label=u"Источник")
        self.cb = wx.ComboBox(self.panel, 500, u"Все", (-1, -1), (160, -1), [u'Все',u'Красноярск',u'Иркутск',u'Чита'], wx.CB_DROPDOWN|wx.CB_READONLY)
        topSizer = wx.BoxSizer(wx.VERTICAL)
        toolsizer = wx.BoxSizer(wx.HORIZONTAL)
        gbsizer = wx.BoxSizer(wx.HORIZONTAL)
        ssizer = wx.BoxSizer(wx.HORIZONTAL)
        gridsizer = wx.BoxSizer(wx.HORIZONTAL)

        gbsizer.Add(gBtn, 0, wx.ALL, 5)
        ssizer.Add(cb_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        ssizer.Add(self.cb, 0, wx.ALL, 5)

        gridsizer.Add(self.lst, 0, wx.ALL)

        toolsizer.Add(gbsizer, 0, wx.ALL)
        toolsizer.Add(ssizer, 0, wx.ALL)

        topSizer.Add(toolsizer, 0, wx.ALL)
        topSizer.Add(gridsizer, 0, wx.ALL)

        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)




    def zenoss_event(self,evt):
        self.lst.zenoss_evt(evt)








if __name__ == '__main__':

    class MyApp(wx.App):
        def OnInit(self):
            MainFrame = MFrame()
            MainFrame.Show(True)
            self.SetTopWindow(MainFrame)
            return True


    app = MyApp(False)
    app.MainLoop()

