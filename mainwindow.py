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

        self.evt_flag = True # Флаг разрешения прима событий

        self.Bind(EVT_ZENOSS_NEW_EVENT, self.zenoss_event)
        t = threading.Thread(target=GetEvents, args=(self, evt_zenoss_new_event))
        t.setDaemon(True)
        t.start()

        self.panel = wx.Panel(self, wx.ID_ANY)

        self.lst = EventsList(self.panel,-1)


        devclass_list = [
            u'/Network/Sweetch',
            u'/Power/UPS',
            u'/Network/Modem',
            u'/Network/DSLAM',
            u'/Network/Eth-to-COM',
            u'/Network/GPON',
            u'/Network/Multiplexer',
            u'/Network/Router',
            u'/Network/VoIP',
            u'/Network/WiMax',
            u'/Network/Wireless',
            u'/Phone/ATC',
            u'/Server/iLO',
            u'/Server/Linux',
            u'/Server/Virtual Machine Host',
            u'/TV'
        ]

        evtclass_list = [
            u'/Perf/CPU',
            u'/Perf/Filesystem',
            u'/Perf/Interface',
            u'/Perf/Memory',
            u'/Perf/Snmp/Comments',
            u'/Perf/Snmp/EAU',
            u'/Perf/Snmp/Enatel',
            u'/Perf/Snmp/InterfaceStatus',
            u'/Perf/Snmp/OLT-TV',
            u'/Perf/Snmp/storm',
            u'/Perf/Snmp/TrCATV',
            u'/Perf/Snmp/UPS',
            u'/Perf/XmlRpc',
            u'/Status/DNS',
            u'/Status/Flapping',
            u'/Status/Heartbeat',
            u'/Status/Ping',
            u'/Status/interface',
        ]

        gBtn = wx.Button(self.panel, 10, u"Группы", (-1,-1))
        cBtn = wx.Button(self.panel, 10, u"Очистить", (-1,-1))
        lBtn = wx.Button(self.panel, 10, u"Загрузить", (-1,-1))
        cb_label = wx.StaticText(self.panel, id=wx.ID_ANY, label=u"Источник")
        self.cb = wx.ComboBox(self.panel, 500, u"Все", (-1, -1), (160, -1), [u'Все',u'Красноярск',u'Иркутск',u'Чита'], wx.CB_DROPDOWN|wx.CB_READONLY)
        devclass_label = wx.StaticText(self.panel, id=wx.ID_ANY, label=u"DevicesClass")
        self.devclass = wx.CheckListBox(self.panel, -1, size=(250, 80), choices=devclass_list, style=wx.LB_HSCROLL)
        evtclass_label = wx.StaticText(self.panel, id=wx.ID_ANY, label=u"EventsClass")
        self.evtclass = wx.CheckListBox(self.panel, -1, size=(250, 80), choices=evtclass_list, style=wx.LB_HSCROLL)

        topSizer = wx.BoxSizer(wx.VERTICAL)
        toolsizer = wx.BoxSizer(wx.HORIZONTAL)
        gbsizer = wx.BoxSizer(wx.VERTICAL)
        ssizer = wx.BoxSizer(wx.HORIZONTAL)
        gridsizer = wx.BoxSizer(wx.HORIZONTAL)

        gbsizer.Add(gBtn, 0, wx.ALL, 1)
        gbsizer.Add(cBtn, 0, wx.ALL, 1)
        gbsizer.Add(lBtn, 0, wx.ALL, 1)
        ssizer.Add(cb_label, 0, wx.ALL|wx.ALIGN_TOP, 5)
        ssizer.Add(self.cb, 0, wx.ALL, 5)
        ssizer.Add(devclass_label, 0, wx.ALL|wx.ALIGN_TOP, 5)
        ssizer.Add(self.devclass, 0, wx.ALL, 5)
        ssizer.Add(evtclass_label, 0, wx.ALL|wx.ALIGN_TOP, 5)
        ssizer.Add(self.evtclass, 0, wx.ALL, 5)

        gridsizer.Add(self.lst, 0, wx.ALL)

        toolsizer.Add(gbsizer, 0, wx.ALL)
        toolsizer.Add(ssizer, 0, wx.ALL)

        topSizer.Add(toolsizer, 0, wx.ALL)
        topSizer.Add(gridsizer, 0, wx.ALL)

        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)

        cBtn.Bind(wx.EVT_BUTTON, self.clear_evts, cBtn)
        lBtn.Bind(wx.EVT_BUTTON, self.zenoss_event_h, lBtn)


    def zenoss_event(self,evt):
        self.lst.zenoss_evt(evt)

    # Загрузка "исторических" событий
    def zenoss_event_h(self, evt):
        self.evt_flag = False
        self.lst.zenoss_evt_h(evt)
        self.evt_flag = True

    ## Очистка всех событий
    def clear_evts(self,evt):
        self.lst.DeleteAllEvents(evt)




if __name__ == '__main__':

    class MyApp(wx.App):
        def OnInit(self):
            MainFrame = MFrame()
            MainFrame.Show(True)
            self.SetTopWindow(MainFrame)
            return True


    app = MyApp(False)
    app.MainLoop()

