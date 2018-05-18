import os

def createEmptyTestResult(testname):
    return {
        'testname': testname,
        'ok': True,
        'msg': 'ok'
    }

def getTestName(file):
    return os.path.basename(file)

chanBinaryMap = {}
chanBinaryMap["11100000"] = 1
chanBinaryMap["11100001"] = 2
chanBinaryMap["11100010"] = 3
chanBinaryMap["11100011"] = 4
chanBinaryMap["11100100"] = 5
chanBinaryMap["11100101"] = 6
chanBinaryMap["10100001"] = "MP"

def getChanBinaryValue(s):
    if s in chanBinaryMap:
        return chanBinaryMap[s]
    else:
        return "SOH"

def organizeLcqList(tokens):
    lcqList = tokens.findall("lcq")
    allChans = {}
    for lcq in lcqList:
        chanCode = lcq.find("seed").text[1:4]
        locCode = lcq.find("loc").text[1:3]
        pin = getChanBinaryValue(lcq.find("chan").text)
        sispin = pin
        if pin == 'MP':
            subchan = int(lcq.find("subchan").text)
            sispin = subchan+1
            if sispin <= 3:
                sispin += 3
            else:
                sispin += 9
            pin = '{}{}'.format(pin, sispin)
        elif pin == 'SOH':
            sispin = 0
        elif pin >= 4:
                sispin += 3 # q330 pin 4-6 => sis pin 7-9

        sps = float(lcq.find('rate').text)
        if sps < 0:
            sps = -1.0/sps

        disabled = lcq.find("disable").text
        if disabled == '0':
            disabled = ''
        else:
            disabled = "disabled"
        if not sispin in allChans:
            allChans[sispin] = []
        chanByPin = allChans[sispin]
        chanByPin.append({
            'lcq': lcq,
            'chanCode': chanCode,
            'locCode': locCode,
            'sps': sps,
            'q330pin': pin,
            'sispin': sispin,
            'disabled': disabled
        })
    return allChans

def azmuthFromChanCode(chan):
    if chan[-1] == 'Z':
        return 0
    elif chan[-1] == 'N' or chan[-1] == '1':
        return 0
    elif chan[-1] == 'E' or chan[-1] == '2':
        return 90
    elif chan[-1] == 'U':
        return 330
    elif chan[-1] == 'V':
        return 210
    elif chan[-1] == 'W':
        return 90
    else:
        return 'az?'

def dipFromChanCode(chan):
    if chan[-1] == 'Z':
        return -90
    elif chan[-1] == 'N' or chan[-1] == '1':
        return 0
    elif chan[-1] == 'E' or chan[-1] == '2':
        return 0
    elif chan[-1] == 'U':
        return -54.7
    elif chan[-1] == 'V':
        return -54.7
    elif chan[-1] == 'W':
        return -54.7
    else:
        return 'dip?'

def getSOHComponentFromChanCode(sohChan):
    return componentNameMap[sohChan]


def getSOHComponentNameFromChanCode(sohChan):
    return getSOHComponentFromChanCode(sohChan)['component']

componentNameMap = {
'ACE': { 'component':'CLOCKSTATUS', 'type':'Clock Status', 'gain':0, 'units':'' },
'LCE': { 'component':'CLOCKPHASE', 'type':'Clock Phase', 'gain':1000000, 'units':'count/s' },
'LCL': { 'component':'CLOCKLOCKLOSS', 'type':'Clock Lock Loss', 'gain':0.016667, 'units':'count/s' },
'LCO': { 'component':'CALIBRATIONINPUT', 'type':'Calibration Input', 'gain':0 , 'units':''		 },
'LCQ': { 'component':'CLOCKQUALITY', 'type':'Clock Quality', 'gain':1, 'units':'count/%' },
'LOG': { 'component':'LOG', 'type':'LOG', 'gain':0 , 'units':'' },
'OCF': { 'component':'OCF', 'type':'OCF', 'gain':0 , 'units':''},
'VCE': { 'component':'CLOCKPHASE', 'type':'Clock Phase', 'gain':1000000, 'units':'count/s' },
'VCO': { 'component':'VOLTAGECONTROLLEDOSCILLATOR', 'type':'Voltage Controlled Oscillator', 'gain':1, 'units':'count/number' },
'VCQ': { 'component':'CLOCKQUALITY', 'type':'Clock Quality', 'gain':1, 'units':'count/%' },
'VEA': { 'component':'GPSANTENNACURRENT', 'type':'GPS Antenna Current', 'gain':1000, 'units':'count/A' },
'VEC': { 'component':'SYSTEMCURRENT', 'type':'System Current', 'gain':1000, 'units':'count/A' },
'VEP': { 'component':'SYSTEMVOLTAGE', 'type':'System Voltage', 'gain':6.667, 'units':'count/V' },
'VFP': { 'component':'PACKETBUFFERUSAGE', 'type':'Packet Buffer Usage', 'gain':10, 'units':'count/%' },
'VKI': { 'component':'SYSTEMTEMPERATURE', 'type':'System Temperature', 'gain':1, 'units':'count/degC'  }
}
