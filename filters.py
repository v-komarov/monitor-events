#coding:utf-8



## Фильтр по источнику
def FilterSource(e, zenoss_source):

    pref = e['evid'].split('-')[0]

    if pref == "krsk" and zenoss_source == u"Красноярск":
        return True
    elif pref == "irk" and zenoss_source == u"Иркутск":
        return True
    elif pref == "chi" and zenoss_source == u"Чита":
        return True
    elif zenoss_source == u"Все":
        return True

    return False


## Фильтр по классу устройства
def FilterDevice(e, devclass_list):

    if len(devclass_list) == 0:
        return True

    for item in devclass_list:
        if e['device_class'].find(item) != 1:
            return True

    return False


## Фильтр по классу события
def FilterEvent(e, evtclass_list):

    if len(evtclass_list) == 0:
        return True

    for item in evtclass_list:
        if e['event_class'].find(item) != 1:
            return True

    return False



## Фильтр в итоге
def FiltersEvents(e, zenoss_source, devclass_list, evtclass_list):

    if FilterSource(e, zenoss_source) and FilterDevice(e, devclass_list) and FilterEvent(e, evtclass_list):
        return True
    else:
        return False


