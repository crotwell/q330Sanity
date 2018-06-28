
import arrow
from lxml import etree

import util

def printInstructions(outfile, q330, filename):
    outfile.write('----------- SIS Logger Configuration ({})-----------\n'.format(filename))
    updated = arrow.get(q330.find("writer").find("updated").text, 'DD MMM YYYY HH:mm:ss ZZZ')
    outfile.write("  Install time: {}\n".format(updated.format('YYYY-MM-DD HH:mm:ss ZZ')))
    tokens1 = q330.find("tokens1")
    outfile.write("  Tokens 1\n");
    outfile.write("  Dip and Azimuth are only guesses based on channel code\n");
    allChans = util.organizeLcqList(tokens1)

    outfile.write('\n')
    outfile.write("------------ Data --------------------------\n")
    outfile.write("{:3} {:3} {:2} {:4} {:5} {:>5} {:8}\n".format('pin', 'chan', 'loc', 'az', 'dip', 'sps', 'disabled'))
    outfile.write("--------------------------------------------\n")
    for k in sorted(allChans.keys()):
        if k == 0:
            continue
        cList = allChans[k]
        for v in cList:
            outfile.write("{:3} {:3}  {:2} {:4} {:5} {:6} {:8}\n".format(v['sispin'],
                                                     v['chanCode'],
                                                     v['locCode'],
                                                     util.azmuthFromChanCode(v['chanCode']),
                                                     util.dipFromChanCode(v['chanCode']),
                                                     v['sps'],
                                                     v['disabled']))
    outfile.write('\n')
    outfile.write("------------ SOH -------------------------------------------\n")
    outfile.write("{:30} {:3} {:2} {:>5} {:8}\n".format('component', 'chan', 'loc', 'sps', 'disabled'))
    outfile.write("------------------------------------------------------------\n")
    sohList = allChans[0]
    for v in sohList:
        outfile.write("{:30} {:3}  {:2} {:5} {:8}\n".format(util.getSOHComponentNameFromChanCode(v['chanCode']),
                                                 v['chanCode'],
                                                 v['locCode'],
                                                 v['sps'],
                                                 v['disabled']))
    if tokens1.find('cfgflgbeg').text == '1' or tokens1.find('cfgflgend').text == '1' or tokens1.find('cfgflgint').text == '1':
        msgname = tokens1.find('msgname').text.strip('"')
        msgloc = tokens1.find('msgloc').text.strip('"')
        outfile.write("{:30} {:3}  {:2} {:5} {:8}\n".format(util.getSOHComponentNameFromChanCode(msgname),
                                                 msgname,
                                                 msgloc,
                                                 0,
                                                 ''))
        timname = tokens1.find('timname').text.strip('"')
        timloc = tokens1.find('timloc').text.strip('"')
        outfile.write("{:30} {:3}  {:2} {:5} {:8}\n".format(util.getSOHComponentNameFromChanCode(timname),
                                               timname,
                                               timloc,
                                               0,
                                               ''))
        cfgname = tokens1.find('cfgname').text.strip('"')
        cfgloc = tokens1.find('cfgloc').text.strip('"')
        outfile.write("{:30} {:3}  {:2} {:5} {:8}\n".format(util.getSOHComponentNameFromChanCode(cfgname),
                                                 cfgname,
                                                 cfgloc,
                                                 0,
                                                 ''))
    outfile.write('\n')
    outfile.write("Net: {}\n".format(q330.find("tokens1").find('network').text))
    outfile.write("Station code: {}\n".format(q330.find("tokens1").find('station').text))
    outfile.write('\n')
