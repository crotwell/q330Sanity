
import arrow
from lxml import etree

import util

def printInstructions(q330, filename):
    print('----------- SIS Logger Configuration ({})-----------'.format(filename))
    updated = arrow.get(q330.find("writer").find("updated").text, 'DD MMM YYYY HH:mm:ss ZZZ')
    print("Install time: {}".format(updated.format('YYYY-MM-DD HH:mm:ss ZZ')))
    tokens1 = q330.find("tokens1")
    allChans = util.organizeLcqList(tokens1)

    print()
    print("------------ Data --------------------------")
    print("{:3} {:3} {:2} {:4} {:5} {:>5} {:8}".format('pin', 'chan', 'loc', 'az', 'dip', 'sps', 'disabled'))
    print("--------------------------------------------")
    for k in sorted(allChans.keys()):
        if k == 0:
            continue
        cList = allChans[k]
        for v in cList:
            print("{:3} {:3}  {:2} {:4} {:5} {:6} {:8}".format(v['sispin'],
                                                     v['chanCode'],
                                                     v['locCode'],
                                                     util.azmuthFromChanCode(v['chanCode']),
                                                     util.dipFromChanCode(v['chanCode']),
                                                     v['sps'],
                                                     v['disabled']))
    print()
    print("------------ SOH -------------------------------------------")
    print("{:30} {:3} {:2} {:>5} {:8}".format('component', 'chan', 'loc', 'sps', 'disabled'))
    print("------------------------------------------------------------")
    sohList = allChans[0]
    for v in sohList:
        print("{:30} {:3}  {:2} {:5} {:8}".format(util.getSOHComponentNameFromChanCode(v['chanCode']),
                                                 v['chanCode'],
                                                 v['locCode'],
                                                 v['sps'],
                                                 v['disabled']))
    if tokens1.find('cfgflgbeg').text == '1' or tokens1.find('cfgflgend').text == '1' or tokens1.find('cfgflgint').text == '1':
        msgname = tokens1.find('msgname').text.strip('"')
        msgloc = tokens1.find('msgloc').text.strip('"')
        print("{:30} {:3}  {:2} {:5} {:8}".format(util.getSOHComponentNameFromChanCode(msgname),
                                                 msgname,
                                                 msgloc,
                                                 0,
                                                 ''))
        timname = tokens1.find('timname').text.strip('"')
        timloc = tokens1.find('timloc').text.strip('"')
        print("{:30} {:3}  {:2} {:5} {:8}".format(util.getSOHComponentNameFromChanCode(timname),
                                               timname,
                                               timloc,
                                               0,
                                               ''))
        cfgname = tokens1.find('cfgname').text.strip('"')
        cfgloc = tokens1.find('cfgloc').text.strip('"')
        print("{:30} {:3}  {:2} {:5} {:8}".format(util.getSOHComponentNameFromChanCode(cfgname),
                                                 cfgname,
                                                 cfgloc,
                                                 0,
                                                 ''))
    print()
    print("Net: {}".format(q330.find("tokens1").find('network').text))
    print("Station code: {}".format(q330.find("tokens1").find('station').text))
    print()
