import hashlib
import httplib
import json
import os
import re
import subprocess
import sys
import time
import traceback

from fansiteSimulator import FansiteSimulator
import fansiteConfig
import fansiteHttp
import testRepo
import tyrantData

def askToUpdateDataFiles():
    input_var = raw_input("Would you like to download the latest Tyrant xml files (y/n)? ")
    if(input_var == "Y" or input_var == "y"):
        tyrantData.updateDataFiles()

def startSession(token, version, check = None):
    if(check is None):
        check = tyrantData.getCheck()
    json_data = fansiteHttp.getSession(token, version, check)

    # TODO this is a bit of a hack
    if("errorCode" in json_data and json_data["errorCode"] >= 101 and json_data["errorCode"] <= 110):
        askToUpdateFiles()

    if(not "sessId" in json_data):
        return None

    return json_data["sessId"]

def loadSimulators():
    simulators = {}
    
    # add extra simulators here. don't forget to import any files you need
    from simulatorIteratedecks import SimulatorIteratedecks
    simulators[SimulatorIteratedecks.name] = SimulatorIteratedecks

    return simulators

def simDeck(simulator, deck, num):
    deckId = deck["deckId"]

    start = time.time()
    results = simulator.simulate(deck, num)
    timeTaken = int(time.time() - start)
    results["time"] = timeTaken

    return results

def fansiteTest():
    args = fansiteConfig.getArgs()
    simulators = loadSimulators()

    simulator = None
    if(args.simulator in simulators):
        simulator = simulators[args.simulator]()
    else:
        print("Unsupported simulator: " + args.simulator)
        return

    token = args.token
    num = args.numSims
    version = simulator.getVersion()

    if(args.test):
        num = 1000

    print("Using " + simulator.name + " version " + version + " with " + str(num) + " sims per deck")

    if(not args.test):
        print("Requesting session id...")
        sessId = startSession(token, version)
        if(sessId is None):
            print("No session started.")
            return
        print(" ... started session with id " + sessId)

    print("Getting decks...")
    if(not args.test):
        json_data = fansiteHttp.getDecks(sessId)
        decks = json_data["decks"]
    else:
        decks = testRepo.loadTests(True)
    print(" ... " + str(len(decks)) + " decks retrieved")

    for deck in decks:
        deckId = deck["deckId"]

        try:
            results = simDeck(simulator, deck, num)

            if(not args.test):
                print(" ... result was: " + results["wins"] + "/" + results["total"])
                json_data = fansiteHttp.submitSimulation(deckId, sessId, results["total"], results["wins"], results["time"], results["anp"])
            else:
                testRepo.testKey(deck, "winrate", 100 * int(results["wins"]) / int(results["total"]))
                testRepo.testKey(deck, "drawrate", 100 * int(results["draws"]) / int(results["total"]))
                testRepo.testKey(deck, "lossrate", 100 * int(results["losses"]) / int(results["total"]))
        except NotImplementedError, Argument:
            ex, val, tb = sys.exc_info()
            traceback.print_exception(ex, val, tb)

if __name__ == '__main__':
    #while(True):
    fansiteTest()
