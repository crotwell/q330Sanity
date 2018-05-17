import util

def test(tokenNum, lcq):
    result = {}
    result['testname'] = util.getTestName(__file__)
    result['lcq'] = lcq
    result['tokenNum'] = tokenNum
    bandCode = lcq.find("seed").text[1]
    bandRange = bandToSpsMap[bandCode]
    sps = float(lcq.find('rate').text)
    if sps < 0:
        sps = -1.0/sps
    if sps < bandRange[0] or sps >= bandRange[1]:
        result['msg'] = "band code {!s} but sps of {!s} is not >= {!s} and < {!s}".format(bandCode, sps, bandRange[0], bandRange[1])
        result['ok'] = False
    else:
        result['ok'] = True
    return result

bandToSpsMap = {
    'F':[1000, 5000],
    'G':[1000, 5000],
    'D':[250, 1000],
    'C':[250, 1000],
    'E':[80, 250],
    'S':[10, 80],
    'H':[80, 250],
    'B':[10, 80],
    'M':[1, 10],
    'L':[1, 1.001],
    'V':[.1, .1001],
    'U':[.01, .01001],
    'R':[.0001, .001],
    'P':[.00001, .0001],
    'T':[.000001, .00001],
    'Q':[0, .000000],
    'A':[0, 9999999],
    'O':[0, 9999999]
}
