import numbers
import util

def test(tokenNum, lcq):
    result = {}
    result['testname'] = util.getTestName(__file__)
    result['lcq'] = lcq
    result['tokenNum'] = tokenNum
    channelNum = util.getChanBinaryValue(lcq.find("chan").text)
    subchan = int(lcq.find("subchan").text)+1
    orientCode = lcq.find("seed").text[3]
    if isinstance(channelNum, numbers.Number) and chanNumToCodes[channelNum].count(orientCode) == 0:
        result['msg'] = "chan comes from q330 '{!s}' but not in {!s} ".format(channelNum, chanNumToCodes[channelNum])
        result['ok'] = False
    elif channelNum == 'MP' and chanNumToCodes[subchan].count(orientCode) == 0:
        result['msg'] = "mass position chan comes from subchan '{!s}' but not in {!s} ".format(subchan, chanNumToCodes[subchan])
        result['ok'] = False
    else:
        result['ok'] = True
    return result


chanNumToCodes = {1:['Z','U'], 2:['N','1','W'], 3:['E','2','V'],
                  4:['Z','U'], 5:['N','1','W'], 6:['E','2','V']}
