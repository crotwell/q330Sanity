import util

testname = util.getTestName(__file__)

def test(tokenNum, lcq):
    result = util.createEmptyTestResult(testname)
    result['lcq'] = lcq
    result['tokenNum'] = tokenNum
    disabled = lcq.find("disable").text
    if disabled == 1:
        result['msg'] = "disabled channel"
        result['ok'] = False
    else:
        result['ok'] = True
    return result
