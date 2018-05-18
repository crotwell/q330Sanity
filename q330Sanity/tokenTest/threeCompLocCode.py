import util

testname = util.getTestName(__file__)

def test(tokenNum, token):
    resultList = []
    result = util.createEmptyTestResult(testname)
    result['token'] = token
    result['tokenNum'] = tokenNum
    allChans = util.organizeLcqList(token)
    byLoggerBoard = {'A':[], 'B':[], 'SOH':[] }
    lcqList = token.findall("lcq")
    for i in range(1, 7):
        if i in allChans:
            byLoggerBoard['A'].extend(allChans[i])
    for i in range(7, 13):
        if i in allChans:
            byLoggerBoard['B'].extend(allChans[i])
    if 0 in allChans:
        byLoggerBoard['SOH'].extend(allChans[0])
    for board in ['A', 'B', 'SOH']:
        allLocCodes = set()
        for lcqOb in byLoggerBoard[board]:
            allLocCodes.add(lcqOb['locCode'])
        if len(allLocCodes) > 1:
            r = util.createEmptyTestResult(testname)
            r['token'] = token
            r['tokenNum'] = tokenNum
            r['msg'] = "Expected one loc code for board {} but found {}: {}".format(board, len(allLocCodes), allLocCodes)
            r['ok'] = False
            resultList.append(r)
    if len(resultList) == 0:
        result['ok'] = True
    else:
        result = resultList
    return result
