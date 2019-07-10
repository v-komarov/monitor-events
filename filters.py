#coding:utf-8




city_source = {
    "krsk": u"Красноярск",
    "irk": u"Иркутск",
    "chi": u"Чита"
}




## Фильтр по источнику
def FilterSource(e, zenoss_source):

    #print zenoss_source

    pref = e['evid'].split('-')[0]

    if city_source[pref] in zenoss_source:
        return True

    return False


## Фильтр по классу устройства
def FilterDevice(e, devclass_list):

    if len(devclass_list) == 0:
        return True

    for item in devclass_list:
        if e['device_class'].find(item.encode("utf-8")) != -1:
            return True

    return False


## Фильтр по классу события
def FilterEvent(e, evtclass_list):

    if len(evtclass_list) == 0:
        return True

    for item in evtclass_list:
        if e['event_class'].find(item.encode("utf-8")) != -1:
            return True

    return False



## Фильтр в итоге
def FiltersEvents(e, zenoss_source, devclass_list, evtclass_list):

    if FilterSource(e, zenoss_source) and FilterDevice(e, devclass_list) and FilterEvent(e, evtclass_list):
        return True
    else:
        return False


