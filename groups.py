#coding:utf-8

import wx
import json
import sys
import psycopg2
import uuid
from pymemcache.client.hash import HashClient


from conf import memcach, pg_host, pg_port, pg_base, pg_user, pg_password


client = HashClient(memcach)
conn = psycopg2.connect("dbname={} user={} host={} password={}".format(pg_base,pg_user,pg_host,pg_password))
conn.autocommit = True
cursor = conn.cursor()

# Проверка в memcached ключах, если есть - пишем в (update) postgresql

def CheckGroup(evt):

    e = json.loads(evt.m)
    h = "{}".format(hash(evt.m))
    k = client.get(e['evid'])
    if k:
        ### Значение ключа совпадает - нет необходимости писать в базу
        if k == h:
            return False
        else:
            ### Необходимо обновить запись события в базе
            client.set(e['evid'], h)
            cursor.execute("UPDATE groups_data SET event_data=%s WHERE event_id=%s", [evt.m,e['evid']])
            return False
    else:
        # В ключах нет идентификатора события - отображать событие на экране
        return True






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


    # Создание новой группы
    def add_group(self, evt):
        dlg = wx.TextEntryDialog(self, u'Задайте название группы', u'Создание новой группы')
        dlg.SetValue(u"Проверка")
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
                self.glist.show_group()
            dlg.Destroy()





class GroupNameList(wx.ListCtrl):

    def __init__(self, parent, ID, pos=(0,0), size=(600,400), style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        self.SelectedEvId = set()
        self.InsertColumn(0, u"id")
        self.InsertColumn(1, u"Название групп")
        self.SetColumnWidth(0, 100)
        self.SetColumnWidth(1, 600)

        self.SelectedGrId = None # Выбранная группа
        self.SelectedGrName = None # Выбранная группа

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.SelectItem)


        self.show_group()


    def SelectItem(self,evt):
        self.SelectedGrId = self.GetItemText(evt.m_itemIndex)
        self.SelectedGrName = self.GetItemText(evt.m_itemIndex, col=1)



    ## Отображените групп
    def show_group(self):

        self.DeleteAllItems()

        cursor.execute("SELECT group_id,group_name FROM groups_list;")
        for row in cursor.fetchall():
            pos = self.InsertStringItem(sys.maxint, row[0])
            self.SetStringItem(pos, 0, row[0])
            self.SetStringItem(pos, 1, row[1])





if __name__ == '__main__':

    cursor.execute("SELECT 1;")
    data = cursor.fetchone()
    print data

