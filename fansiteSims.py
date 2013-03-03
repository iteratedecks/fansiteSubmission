import hashlib
import httplib
import json
import os
import re
import subprocess
import time

from fansiteSimulator import FansiteSimulator
import fansiteConfig
import fansiteHttp
import tyrantData

def askToUpdateDataFiles():
    input_var = raw_input("Would you like to download the latest Tyrant xml files (y/n)? ")
    if(input_var == "Y" or input_var == "y"):
        tyrantData.updateDataFiles()

def loadSimulators():
    simulators = {}
    
    # add extra simulators here. don't forget to import any files you need
    from simulatorIteratedecks import SimulatorIteratedecks
    simulators[SimulatorIteratedecks.name] = SimulatorIteratedecks

    return simulators

def fansiteTest():
    args = fansiteConfig.getArgs()

    simulators = loadSimulators()

    simulator = None
    if(args["simulator"] in simulators):
        simulator = simulators[args["simulator"]]()
    else:
        print("Unsupported simulator: " + args["simulator"])
        return

    token = args["token"]
    num = args["numSims"]
    version = simulator.getVersion()

    print("Using " + simulator.name + " version " + version + " with " + str(num) + " sims per deck")
    print("Requesting session id...")

    check = tyrantData.getCheck()

    json_data = fansiteHttp.getSession(token, version, check)

    # TODO this is a bit of a hack
    if("errorCode" in json_data and json_data["errorCode"] >= 101 and json_data["errorCode"] <= 110):
        askToUpdateFiles()

    if(not "sessId" in json_data):
        print("No session started.")
        return

    sessId = json_data["sessId"]
    print(" ... started session with id " + sessId)

    print("Getting decks...")
    json_data = fansiteHttp.getDecks(sessId)
    decks = json_data["decks"]
    print(" ... " + str(len(decks)) + " decks retrieved")

    for deck in decks:
        deckId = deck["deckId"]

        start = time.time()
        [battlesWon, battlesTotal, anp] = simulator.simulate(deck, num)
        timeTaken = int(time.time() - start)

        json_data = fansiteHttp.submitSimulation(deckId, sessId, battlesTotal, battlesWon, timeTaken, anp)

if __name__ == '__main__':
    fansiteTest()
