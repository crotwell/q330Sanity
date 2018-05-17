import util

def test(root):
    resultList = []
    result = {}
    result['testname'] = util.getTestName(__file__)
    result['ok'] = True
    globalEl = root.find("global")
    for i in range(1,7):
        gain = globalEl.find("gains{}".format(i)).text
        if gain != '1.0':
            resultList.append({
                'testname': util.getTestName(__file__),
                'ok': False,
                'msg': "gain for q330 {} is not 1.0".format(i)
            })
    if len(resultList) == 0:
        return result
    else:
        return resultList
