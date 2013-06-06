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
        fileDest = os.path.join(dataDirectory, filename)
        if(os.path.exists(fileDest)):
            with open(fileDest, 'rb') as f:
                data = f.read()
    if(data is None):
        data = updateTests(dataDirectory, filename, host, path)
    json_data = json.loads(data)
    decks = json_data["decks"]
    return decks

def loadSimulators():
    simulators = {}
    
    # add extra simulators here. don't forget to import any files you need
    from simulatorIteratedecks import SimulatorIteratedecks
    simulators[SimulatorIteratedecks.name] = SimulatorIteratedecks
    from simulatorIteratedecks3 import SimulatorIteratedecks3
    simulators[SimulatorIteratedecks3.name] = SimulatorIteratedecks3

    return simulators

def printTestFailure(expected, actual, key, comment):
    print("TEST FAILED on " + key + " (" + str(expected) + " vs. " + str(actual) + "): " + comment)

def testKey(deck, key, actual, threshold = 8):
    if(key in deck):
        expected = deck[key]
        if((expected == 100 or expected == 0) and expected != actual):
            printTestFailure(expected, actual, key, deck["comments"])
        elif((expected + threshold) < actual or (expected - threshold) > actual):
            printTestFailure(expected, actual, key, deck["comments"])
