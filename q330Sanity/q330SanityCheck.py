
'''
Sanity checks on Q330 XML config file.
'''

import argparse
import datetime
import arrow
import os
import re
import subprocess
import sys
from lxml import etree
import unittest

import channelTest.orientationCode
import channelTest.bandCode
import channelTest.locCodeBlank
import tokenTest.networkCode
import tokenTest.threeCompLocCode
import util
import sisInstallInfo
import globalTest.gainUnity

VERBOSE = False
#VERBOSE = True

USAGE_TEXT = """
Usage: python <Parser>.py <in_xml_file>
"""

NRL_PREFIX = "http://ds.iris.edu/NRL"

SCHEMA_FILE = "sis_extension_2.2.xsd"

def usage():
    print(USAGE_TEXT)
    sys.exit(1)

def initArgParser():
  parser = argparse.ArgumentParser(description='Sanity checks on Q330 XML config file.')
  parser.add_argument('-q', '--q330', required=True, help="input Q330 config file, often from Willard.")
  parser.add_argument('--nrl', default='nrl', help="replace matching responses with links to NRL")
  parser.add_argument('--namespace', default='Testing', help="SIS namespace to use for named responses, see http://anss-sis.scsn.org/sis/master/namespace/")
  parser.add_argument('--operator', default='Testing', help="SIS operator to use for stations, see http://anss-sis.scsn.org/sis/master/org/")
  parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
  parser.add_argument('-v', '--verbose', action='store_true', help="verbose output")
  return parser.parse_args()

allTests = {
    'lcq': [
        channelTest.orientationCode.test,
        channelTest.bandCode.test,
        channelTest.locCodeBlank.test
    ],
    'token': [
        tokenTest.networkCode.test,
        tokenTest.threeCompLocCode.test,
    ],
    'global': [
        globalTest.gainUnity.test,]
}

def runSanity(root):
    out = []
    out.append(globalSanity(root))
    tokens1 = root.find("tokens1")
    out.append(tokenSanity(1, tokens1))
    tokens2 = root.find("tokens2")
    out.append(tokenSanity(2, tokens2))
    tokens4 = root.find("tokens4")
    out.append(tokenSanity(4, tokens4))
    return out

def printSanity(resultList):
    print('----------- Sanity Tests -----------')
    printSanityRecursive(resultList)
    print()

def printSanityRecursive(resultList):
    for result in resultList:
        if isinstance(result, list):
            printSanityRecursive(result)
        else:
            if not result['ok']:
                printResult(result)

def globalSanity(root):
    out = []
    for test in allTests['global']:
        result = test(root)
        out.append(result)
    return out

def tokenSanity(tokenNum, token):
    out = []
    for test in allTests['token']:
        result = test(tokenNum, token)
        out.append(result)
    lcqList = token.findall("lcq")
    for lcq in lcqList:
        out.extend(lcqSanity(tokenNum, lcq))
    return out


def lcqSanity(tokenNum, lcq):
    out = []
    for test in allTests['lcq']:
        result = test(tokenNum, lcq)
        out.append(result)
    return out

def printResult(result):
    if ('lcq' in result):
        lcq = result['lcq']
        loc = lcq.find("loc").text
        seedChan = lcq.find("seed").text
        print('{}:  tokens{}: {!s} {!s}.{!s} {}'.format(result['testname'], result['tokenNum'], result['ok'], loc, seedChan, result['msg']))
    else:
        print('{}:  tokens{}: {!s} {!s}'.format(result['testname'], result['tokenNum'], result['ok'], result['msg']))

def parseQ330Config(filename):
    print("Loading: "+filename)
    tree = etree.parse(filename)
    sanityResultList = runSanity(tree.getroot())
    printSanity(sanityResultList)
    print()
    sisInstallInfo.printInstructions(tree, filename)

def main():
    VERBOSE = False
    sisNamespace = "TESTING"
    parseArgs = initArgParser()
    print("in main")
    if parseArgs.verbose:
        VERBOSE=True
        for k, v in vars(parseArgs).iteritems():
            print("    Args: %s %s"%(k, v))
    sisNamespace = parseArgs.namespace
    if parseArgs.q330:
        if not os.path.exists(parseArgs.q330):
            print("ERROR: can't fine q330 xml file %s"%(parseArgs.q330,))
            return
        parseQ330Config(parseArgs.q330)
