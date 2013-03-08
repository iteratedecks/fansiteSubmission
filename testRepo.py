import httplib
import json
import os

def updateTests(dataDirectory = "", filename = "tests.json", host = "haileon.com", path = "/SimTyrantJS_ListTestCases"):
    fileDest = dataDirectory + filename
    http = httplib.HTTPConnection(host, 80, timeout=10)
    http.request("GET", path)

    print("Getting http://" + host + path + " ...")
    resp = http.getresponse()
    contents = resp.read()

    print("Saving " + fileDest + " ...")
    f = None
    try:
        f = open(fileDest, 'wb')
        f.write(contents)
    finally:
        f.close()

    return contents

def loadTests(forceUpdate = False, dataDirectory = "", filename = "tests.json", host = "haileon.com", path = "/SimTyrantJS_ListTestCases"):
    data = None
    if(not forceUpdate):
        fileDest = dataDirectory + filename
        f = None
        try:
            f = open(fileDest, 'rb')
            contents = f.read()
        finally:
            f.close()
        if(data is None):
            forceUpdate = True

    if(forceUpdate):
        data = updateTests(dataDirectory, filename, host, path)

    json_data = json.loads(data)
    decks = json_data["decks"]
    return decks

def loadSimulators():
    simulators = {}
    
    # add extra simulators here. don't forget to import any files you need
    from simulatorIteratedecks import SimulatorIteratedecks
    simulators[SimulatorIteratedecks.name] = SimulatorIteratedecks

    return simulators

def printTestFailure(expected, actual, key, comment):
    print("TEST FAILED on " + key + " (" + str(expected) + " vs. " + str(actual) + "): " + comment)

def testKey(deck, key, actual):
    testThreshold = 10

    if(key in deck):
        expected = deck[key]
        if((expected == 100 or expected == 0) and expected != actual):
            printTestFailure(expected, actual, key, deck["comments"])
        elif((expected + testThreshold) < actual or (expected - testThreshold) > actual):
            printTestFailure(expected, actual, key, deck["comments"])
