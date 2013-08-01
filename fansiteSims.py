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
        askToUpdateDataFiles()

    if(not "sessId" in json_data):
        return None

    return json_data["sessId"]

def loadSimulators():
    simulators = {}
    
    # add extra simulators here. don't forget to import any files you need
    from simulatorIteratedecks import SimulatorIteratedecks
    simulators[SimulatorIteratedecks.name] = SimulatorIteratedecks
    from simulatorTyrantOptimizer import SimulatorTyrantOptimizer
    simulators[SimulatorTyrantOptimizer.name] = SimulatorTyrantOptimizer
    from simulatorIteratedecks3 import SimulatorIteratedecks3
    simulators[SimulatorIteratedecks3.name] = SimulatorIteratedecks3

    return simulators

def simDeck(simulator, deck, args):
    deckId = deck["deckId"]

    start = time.time()
    results = simulator.simulate(deck, args)
    if results is None:
        return
    timeTaken = int(time.time() - start)
    results["time"] = max(1, timeTaken)

    return results

def fansiteTest():
    args = fansiteConfig.getArgs()
    print args
    simulators = loadSimulators()

    simulator = None
    if(args.simulator in simulators):
        simulator = simulators[args.simulator]()
    else:
        print("Unsupported simulator: " + args.simulator)
        return

    version = simulator.getVersion()

    if(args.test):
        args.numSims = 1000
        args.runForever = 0

    print("Using %s version %s with %s sims per deck" % (simulator.name, version, args.numSims))

    if(not args.test):
        print("Requesting session id...")
        sessId = startSession(args.token, version)
        if(sessId is None):
            print("No session started.")
            return
        print(" ... started session with id " + sessId)

    while 1:
        print("Getting decks...")
        if(not args.test):
            json_data = fansiteHttp.getDecks(sessId, args.limit)
            decks = json_data["decks"]
        else:
            decks = testRepo.loadTests(False)
        print(" ... " + str(len(decks)) + " decks retrieved")

        for deck in decks:
            deckId = deck["deckId"]
            try:
                results = simDeck(simulator, deck, args)
                if results is None:
                    print(" ... no result, skipped")
                if not args.test:
                    print(" ... result: %(wins)s/%(total)s, anp=%(anp)s, time=%(time)s" % results)
                    json_data = fansiteHttp.submitSimulation(deckId, sessId, results["total"], results["wins"], results["time"], results["anp"])
                else:
                    failed = False
                    if not testRepo.testKey(deck, "winrate", 100 * int(results["wins"]) / int(results["total"])):
                        failed = True
                    if "draws" in results:
                        if not testRepo.testKey(deck, "drawrate", 100 * int(results["draws"]) / int(results["total"])):
                            failed = True
                    if "losses" in results:
                        if not testRepo.testKey(deck, "lossrate", 100 * int(results["losses"]) / int(results["total"])):
                            failed = True
                    if "anp" in results:
                        if not testRepo.testKey(deck, "anp", float(results["anp"]), 5):
                            failed = True
                    if failed:
                        print "Failed test-case was:"
                        for key in deck:
                            print "\t", key, " = ", deck[key]
                        print ""
                        if args.oneFailureIsEnough:
                            return False
            except NotImplementedError, e:
                print("Error: Not Implemented: %s" % e)
                return False
            except Exception, e:
                traceback.print_exc()
                return False
        if not args.runForever:
            break
    return True

if __name__ == '__main__':
    if fansiteTest():
        sys.exit(0)
    else:
        sys.exit(1)
