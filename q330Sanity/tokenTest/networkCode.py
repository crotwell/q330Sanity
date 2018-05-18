import util

testname = util.getTestName(__file__)

networkCode = '"CO"'

def test(tokenNum, tokens):
    result = util.createEmptyTestResult(testname)
    result['tokens'] = tokens
    result['tokenNum'] = tokenNum
    tokenNet = tokens.find("network").text
    if (tokenNet != networkCode):
        result['ok'] = False
        result['msg'] = "network code {} is not {}".format(tokenNet, networkCode)
    return result
