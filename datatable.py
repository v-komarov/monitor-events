#coding:utf-8

import sys
import json
import wx
import wx.lib.newevent as NE
from devices import DevicesFrame
from filters import FiltersEvents
from eventsdata import GetEventsTopic
from groups import CheckGroup, GroupList, events2group


evt_zenoss_new_event, EVT_ZENOSS_NEW_EVENT = NE.NewEvent()


class EventsList(wx.ListCtrl):

    def __init__(self, parent, ID, pos=(0,0), size=(2050,2000), style=wx.LC_REPORT|wx.SUNKEN_BORDER):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)





        self.SelectedEvId = set()

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

        self.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.SelectItem)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.DeselectItem)




    def SelectItem(self,evt):
        self.SelectedEvId.add(self.GetItemText(evt.m_itemIndex))


    def DeselectItem(self,evt):
        if self.GetItemText(evt.m_itemIndex) in self.SelectedEvId:
            self.SelectedEvId.remove(self.GetItemText(evt.m_itemIndex))



    ### --- Поиск строки
    def search_st(self,st):

        count = self.GetItemCount()
        cols = self.GetColumnCount()

        if st == "":
            for row in range(count):
                self.Select(row, on=0)
        else:
            for row in range(count):
                self.Select(row, on=0)
                for col in range(cols):
                    item = self.GetItem(itemId=row, col=col)
                    if (item.GetText()).find(st) != -1:
                        self.Select(row, on=1)
                        break




    ### --- Загрузка всех событий топика
    def zenoss_evt_h(self, evt):
        for e in GetEventsTopic():
            #print e
            evt = evt_zenoss_new_event(m=e)
            self.zenoss_evt(evt)





    ### ---Текущие события
    def zenoss_evt(self, evt):


        if self.GetTopLevelParent().evt_flag:

            print evt.m

            # Источник
            zenoss_source = self.GetTopLevelParent().cb.GetStringSelection()

            # Классы устройсв
            devclass_list = self.GetTopLevelParent().devclass.GetCheckedStrings()

            # Классы событий
            evtclass_list = self.GetTopLevelParent().evtclass.GetCheckedStrings()


            e = json.loads(evt.m)

            # Отображать или не отображать событие
            if CheckGroup(evt):
                if FiltersEvents(e, zenoss_source, devclass_list, evtclass_list):
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

            #evid = self.GetItemText(item)
            #if evid in self.SelectedEvId:
            #    self.SelectedEvId.remove(evid)
            #self.DeleteItem(item)


            #pos = self.InsertStringItem(0,e['evid'])
            #pos = self.GetItem(item)


            self.SetStringItem(item, 0, e['evid'])
            self.SetStringItem(item, 1, e['last_seen'])
            self.SetStringItem(item, 2, e['first_seen'])
            self.SetStringItem(item, 3, e['device_group'])
            self.SetStringItem(item, 4, e['device_class'])
            self.SetStringItem(item, 5, e['event_class'])
            self.SetStringItem(item, 6, e['device_system'])
            self.SetStringItem(item, 7, e['device_net_address'])
            self.SetStringItem(item, 8, e['device_location'])
            self.SetStringItem(item, 9, e['element_identifier'])
            self.SetStringItem(item, 10, e['status'])
            self.SetStringItem(item, 11, e['severity'])
            self.SetStringItem(item, 12, e['summary'])



        if self.GetItemCount() > 5000:
            self.DeleteAllItems()
            self.SelectedEvId = set()



    def OnRightClick(self, event):

        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.ToGroup, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.IpInfo, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.DeleteSelected, id=self.popupID3)

        menu = wx.Menu()
        menu.Append(self.popupID1, u"В группу")
        menu.Append(self.popupID2, u"Информация по ip адресу")
        menu.AppendSeparator()
        menu.Append(self.popupID3, u"Удалить")

        self.PopupMenu(menu)
        menu.Destroy()



    ### --- Удаление выделенных строк ---
    def DeleteSelected(self,evt):

        for evid in list(self.SelectedEvId):
            item = self.FindItem(-1,evid)
            if item != -1:
                if self.GetItemText(item) in self.SelectedEvId:
                    self.SelectedEvId.remove(evid)
                self.DeleteItem(item)



    ### --- Информация об устройствах по ip адресам
    def IpInfo(self,evt):
        ips = set()
        for evid in list(self.SelectedEvId):
            item = self.FindItem(-1,evid)
            ips.add(self.GetItemText(item,col=7))

        f = DevicesFrame(ips)
        f.Show(True)



    ### --- Отправка событий в группу
    def ToGroup(self,evt):

        dlg = GroupList(self, -1, u"Группы событий", size=(550, 200), style=wx.DEFAULT_DIALOG_STYLE)
        #dlg.ShowWindowModal()
        if dlg.ShowModal() == wx.ID_OK:
            group_id = dlg.GetValue()
            if group_id:
                events2group(group_id, list(self.SelectedEvId))
                for evid in list(self.SelectedEvId):
                    item = self.FindItem(-1,evid)
                    if item != -1:
                        if self.GetItemText(item) in self.SelectedEvId:
                            self.SelectedEvId.remove(evid)
                        self.DeleteItem(item)

        dlg.Destroy()



    ### --- Удаленние всех событий ---
    def DeleteAllEvents(self,evt):
        self.DeleteAllItems()
