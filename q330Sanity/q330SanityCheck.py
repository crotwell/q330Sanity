
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

def printSanity(outfile, resultList):
    outfile.write('----------- Sanity Tests -----------\n')
    if VERBOSE:
        outfile.write("   - Verbose output {}\n".format(VERBOSE))
    allOk = printSanityRecursive(outfile, resultList)
    if allOk:
        outfile.write('All OK\n')
    outfile.write('\n')

def printSanityRecursive(outfile, resultList, allOk=True):
    for result in resultList:
        if isinstance(result, list):
            allOk = allOk and printSanityRecursive(outfile, result, allOk)
        else:
            if VERBOSE or not result['ok']:
                allOk = False
                printResult(outfile, result)
    return allOk

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

def printResult(outfile, result):
    if ('lcq' in result):
        lcq = result['lcq']
        loc = lcq.find("loc").text
        seedChan = lcq.find("seed").text
        outfile.write('{}:  tokens{}: {!s} {!s}.{!s} {}\n'.format(result['testname'], result['tokenNum'], result['ok'], loc, seedChan, result['msg']))
    elif 'token' in result:
        outfile.write('{}:  tokens{}: {!s} {!s}\n'.format(result['testname'], result['tokenNum'], result['ok'], result['msg']))
    else:
        outfile.write('{}:  {!s} {!s}\n'.format(result['testname'], result['ok'], result['msg']))


def parseQ330Config(outfile, filename):
    print("Loading: "+filename)
    tree = etree.parse(filename)
    sanityResultList = runSanity(tree.getroot())
    printSanity(outfile, sanityResultList)
    outfile.write('\n')
    sisInstallInfo.printInstructions(outfile, tree, filename)

def main():
    parseArgs = initArgParser()
    print("parseArgs.verbose: {}".format(parseArgs.verbose))
    global VERBOSE
    if parseArgs.verbose:
        VERBOSE=True
    if parseArgs.q330:
        if not os.path.exists(parseArgs.q330):
            print("ERROR: can't fine q330 xml file %s"%(parseArgs.q330,))
            return
        parseQ330Config(parseArgs.outfile, parseArgs.q330)
