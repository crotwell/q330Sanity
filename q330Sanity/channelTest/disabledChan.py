import util

def test(tokenNum, lcq):
    result = {}
    result['testname'] = util.getTestName(__file__)
    result['lcq'] = lcq
    result['tokenNum'] = tokenNum
    disabled = lcq.find("disable").text
    if disabled == 1:
        result['msg'] = "disabled channel"
        result['ok'] = False
    else:
        result['ok'] = True
    return result
