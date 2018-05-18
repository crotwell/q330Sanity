import util

testname = util.getTestName(__file__)

def test(root):
    resultList = []
    result = util.createEmptyTestResult(testname)
    result['ok'] = True
    globalEl = root.find("global")
    for i in range(1,7):
        gain = globalEl.find("gains{}".format(i)).text
        if gain != '1.0':
            r = result = util.createEmptyTestResult(testname)
            r['msg'] = "gain for q330 {} is not 1.0".format(i)
            r['ok'] = False
            resultList.append(r)
    if len(resultList) == 0:
        return result
    else:
        return resultList
