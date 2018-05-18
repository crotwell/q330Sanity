import util

testname = util.getTestName(__file__)

def test(tokenNum, lcq):
    result = util.createEmptyTestResult(testname)
    result['lcq'] = lcq
    result['tokenNum'] = tokenNum
    locCode = lcq.find("loc").text
    if locCode == '"  "':
        result['msg'] = "loc code {!s} is space-space".format(locCode, )
        result['ok'] = False
    else:
        result['ok'] = True
    return result
