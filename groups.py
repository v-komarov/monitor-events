#coding:utf-8

import wx
import json
import sys
import psycopg2
import uuid
import datetime
import platform
from pymemcache.client.hash import HashClient

from devices import DevicesFrame

from conf import memcach, pg_host, pg_port, pg_base, pg_user, pg_password


client = HashClient(memcach)
conn = psycopg2.connect("dbname={} user={} host={} port={} password={}".format(pg_base,pg_user,pg_host,pg_port,pg_password))
conn.autocommit = True
cursor = conn.cursor()



### Определение названия группы
def GroupName(group_id):
    cursor.execute("SELECT group_name FROM groups_list WHERE group_id=%s;", [group_id,])
    data = cursor.fetchone()
    name = data[0]
    if wx.Platform == "__WXMSW__":

        if platform.win32_ver()[0] == '7':
            name = data[0].decode('utf-8').encode('cp1251')


    return name



# Проверка в memcached ключах, если есть - пишем в (update) postgresql
def CheckGroup(evt):

    e = json.loads(evt.m)
    h = "{}".format(hash(evt.m))
    k = client.get(e['evid'])
    if k != None:
        ### Значение ключа совпадает - нет необходимости писать в базу
        if k == h:
            return False
        else:
            ### Необходимо обновить запись события в базе
            client.set(e['evid'], h)
            cursor.execute("UPDATE groups_data SET event_data=%s, rec_update=%s WHERE event_id=%s", [evt.m, datetime.datetime.now(), e['evid']])
            return False
    else:
        # В ключах нет идентификатора события - отображать событие на экране
        return True




## Отправка событий в группу
def events2group(group_id, events):
    ## Создание ключей
    for ev in events:
        client.set(ev,"")
        # Запись в базу данных
        cursor.execute("INSERT INTO groups_data(group_id,event_id) VALUES(%s,%s);", [group_id, ev])



## Диалог списка групп
class GroupList(wx.Dialog):

    def __init__(self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE):


        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        self.PostCreate(pre)

        topSizer = wx.BoxSizer(wx.VERTICAL)

        self.glist = GroupNameList(self, -1)
        topSizer.Add(self.glist, 0, wx.ALL)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        topSizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.BoxSizer(wx.HORIZONTAL)



        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.Add(btn, 0, wx.ALL)

        btn2 = wx.Button(self, wx.ID_ADD)
        btnsizer.Add(btn2, 0, wx.ALL)

        btn3 = wx.Button(self, wx.ID_DELETE)
        btnsizer.Add(btn3, 0, wx.ALL)

        btn4 = wx.Button(self, wx.ID_CANCEL)
        btnsizer.Add(btn4, 0, wx.ALL)


        topSizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.ALL, 5)

        self.SetSizer(topSizer)
        topSizer.Fit(self)

        btn2.Bind(wx.EVT_BUTTON, self.add_group, btn2)
        btn3.Bind(wx.EVT_BUTTON, self.delete_group, btn3)


    ## Возвращаемое значение - id group
    def GetValue(self):
        return self.glist.SelectedGrId


    # Создание новой группы
    def add_group(self, evt):
        dlg = wx.TextEntryDialog(self, u'Задайте название группы', u'Создание новой группы')
        dlg.SetValue(u"Группа")
        if dlg.ShowModal() == wx.ID_OK:
            newgroup = dlg.GetValue()
            if newgroup != u"":
                cursor.execute("INSERT INTO groups_list (group_id, group_name) VALUES(%s,%s);", [str(uuid.uuid4()),newgroup])
                self.glist.show_group()

        dlg.Destroy()


    # Удаление группы
    def delete_group(self, evt):

        if self.glist.SelectedGrId:
            g_name = self.glist.SelectedGrName
            g_id = self.glist.SelectedGrId
            dlg = wx.MessageDialog(self, u'Удалить группу {} ?'.format(g_name), caption=u'Удаление', style=wx.OK|wx.CANCEL|wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_OK:
                cursor.execute("DELETE FROM groups_list WHERE group_id=%s", [g_id])
                ## очистка memcached
                cursor.execute("SELECT event_id FROM groups_data WHERE group_id=%s", [g_id])
                for row in cursor.fetchall():
                    client.delete(row[0])
                cursor.execute("DELETE FROM groups_data WHERE group_id=%s", [g_id])


                self.glist.show_group()
            dlg.Destroy()





class GroupNameList(wx.ListCtrl):

    def __init__(self, parent, ID, pos=(0,0), size=(600,400), style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        self.SelectedEvId = set()
        self.InsertColumn(0, u"Название групп")
        self.SetColumnWidth(0, 600)

        self.SelectedGrId = None # Выбранная группа
        self.SelectedGrName = None # Выбранная группа
        self.myRowDict = {}

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.SelectItem)


        self.show_group()


    def SelectItem(self,evt):
        self.SelectedGrId = self.myRowDict[evt.m_itemIndex]
        self.SelectedGrName = self.GetItemText(evt.m_itemIndex)



    ## Отображените групп
    def show_group(self):

        self.DeleteAllItems()
        self.myRowDict = {}
        cursor.execute("SELECT group_id,group_name FROM groups_list;")
        index = 0
        for row in cursor.fetchall():
            pos = self.InsertStringItem(index, row[0])
            group_name = row[1]
            if wx.Platform == "__WXMSW__":

                if platform.win32_ver()[0] == '7':
                    group_name = data[0].decode('utf-8').encode('cp1251')

            self.SetStringItem(pos, 0, group_name)
            self.myRowDict[index] = row[0]
            index += 1




### Фрейм отображения событий группы
class GroupFrame(wx.Frame):
    def __init__(self, group_id, group_name):
        wx.Frame.__init__(self, None, 1, group_name, size=(700,500), style=wx.DEFAULT_FRAME_STYLE)
        self.MId=wx.NewId()

        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.Bitmap("icon.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        self.group_id = group_id


        self.panel = wx.Panel(self, wx.ID_ANY)


        iBtn = wx.Button(self.panel, wx.ID_INFO)
        rBtn = wx.Button(self.panel, wx.ID_REFRESH)

        self.lst = EventsGroupList(self.panel,-1)


        topSizer = wx.BoxSizer(wx.VERTICAL)
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)

        btnsizer.Add(iBtn, 0, wx.ALL, 1)
        btnsizer.Add(rBtn, 0, wx.ALL, 1)

        topSizer.Add(btnsizer, 0, wx.ALL, 1)
        topSizer.Add(self.lst, 0, wx.ALL, 1)


        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)

        rBtn.Bind(wx.EVT_BUTTON, self.lst.appendRow)
        iBtn.Bind(wx.EVT_BUTTON, self.InfoGroup, iBtn)



    ### Информация по группе
    def InfoGroup(self, evt):
        # Список ip
        ips = []
        cursor.execute("SELECT event_data FROM groups_data WHERE group_id=%s", [self.group_id,])
        data = cursor.fetchall()
        for ip in data:
            ips.append(ip[0]['device_net_address'])

        f = DevicesFrame(ips)
        f.Show(True)





class EventsGroupList(wx.ListCtrl):

    def __init__(self, parent, ID, pos=(0,0), size=(2050,2000), style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)


        self.SelectedEvId = None

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


        self.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.SelectItem)


        ### Отображение информации о событиях
        self.appendRow(None)



    def SelectItem(self,evt):
        self.SelectedEvId = self.GetItemText(evt.m_itemIndex)


    ## Меню
    def OnRightClick(self, event):
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.DeleteRec, id=self.popupID1)

        menu = wx.Menu()
        menu.Append(self.popupID1, u"Удалить")

        self.PopupMenu(menu)
        menu.Destroy()




    ### Удаление строки с данными
    def DeleteRec(self, evt):
        evid =  self.SelectedEvId
        if evid != None:
            client.delete(evid)
            cursor.execute("DELETE FROM groups_data WHERE event_id=%s", [evid,])
            self.appendRow(evt)



    ## Загрузка даннных событий из базы
    def appendRow(self,evt):

        self.SelectedEvId = None

        cursor.execute("SELECT event_id, event_data FROM groups_data WHERE group_id=%s;", [self.GetParent().GetParent().group_id])
        data = cursor.fetchall()

        self.DeleteAllItems()

        for row in data:
            pos = self.InsertStringItem(0, row[0])

            self.SetStringItem(pos, 0, row[0])
            if row[1] != None:
                self.SetStringItem(pos, 1, row[1]['last_seen'])
                self.SetStringItem(pos, 2, row[1]['first_seen'])
                self.SetStringItem(pos, 3, row[1]['device_group'])
                self.SetStringItem(pos, 4, row[1]['device_class'])
                self.SetStringItem(pos, 5, row[1]['event_class'])
                self.SetStringItem(pos, 6, row[1]['device_system'])
                self.SetStringItem(pos, 7, row[1]['device_net_address'])
                self.SetStringItem(pos, 8, row[1]['device_location'])
                self.SetStringItem(pos, 9, row[1]['element_identifier'])
                self.SetStringItem(pos, 10, row[1]['status'])
                self.SetStringItem(pos, 11, row[1]['severity'])
                self.SetStringItem(pos, 12, row[1]['summary'])




if __name__ == '__main__':

    cursor.execute("SELECT 1;")
    data = cursor.fetchone()
    print data

