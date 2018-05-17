import util

networkCode = '"CO"'

def test(tokenNum, tokens):
    result = {}
    result['testname'] = util.getTestName(__file__)
    result['tokens'] = tokens
    result['tokenNum'] = tokenNum
    result['ok'] = True
    tokenNet = tokens.find("network").text
    if (tokenNet != networkCode):
        result['ok'] = False
        result['msg'] = "network code {} is not {}".format(tokenNet, networkCode)
    return result
