#import hashlib
#import httplib
#import json
#import os
import re
import subprocess
#import time

class FansiteSimulator(object):
    name = "default"
    executable = None

    def __init__(self):
        self.version = None

    def getVersion(self):
        if(self.version is None):
            self.version = self.loadVersion()
        return self.version

    def simulate(self, deck, numSims):
        playerHash = deck["attackingDeck"]
        type = deck["type"]

        commandArgs = [self.executable]
        attackingDeckCards = None
        if("attackingDeckCards" in deck):
            attackingDeckCards = deck["attackingDeckCards"]

        self.addAttackingDeck(commandArgs, deck["attackingDeck"], attackingDeckCards)

        if(type == "raid"):
            self.addRaid(commandArgs, deck["raidId"])

        elif(type == "mission"):
            self.addMission(commandArgs, deck["missionId"])

        elif(type == "quest"):
            self.addQuest(commandArgs, deck["questId"])

        elif(type == "custom"):
            self.addCustom(commandArgs, deck["defendingDeck"])

        elif(type == "ach"):
            if("missionId" in deck):
                self.addAchievement(commandArgs, deck["achId"], deck["missionId"])
            else:
                print("Skipping achievement " + str(deck["achId"]) + " because it has no mission id.")
                return # don't run the simulation

        else:
            print("unknown deck type: " + type)
            return

        if("battlegroundId" in deck):
            self.addBattlegroundId(commandArgs, deck["battlegroundId"])

        if("isExactedOrdered" in deck and deck["isExactedOrdered"]):
            self.addExactOrdered(commandArgs)
        elif("isOrdered" in deck and deck["isOrdered"]):
            self.addOrdered(commandArgs)

        if("isSurge" in deck and deck["isSurge"]):
            self.addSurge(commandArgs)

        if("isDelayed" in deck and deck["isDelayed"]):
            self.addDelayed(commandArgs)

        self.addNumSims(commandArgs, numSims)

        print("Running " + " ".join(commandArgs))
        result = subprocess.check_output(commandArgs)
        return self.processResults(result)

    def processResults(self, results):
        raise NotImplementedError

    def loadVersion(self):
        raise NotImplementedError

    def addAchievement(self, commandArgs, achievementId, missionId):
        raise NotImplementedError

    def addAttackingDeck(self, commandArgs, attackingDeck, attackingDeckCards):
        raise NotImplementedError

    def addBattlegroundId(self, commandArgs, battlegroundId):
        raise NotImplementedError

    def addCustom(self, commandArgs, custom):
        raise NotImplementedError

    def addDelayed(self, commandArgs):
        raise NotImplementedError

    def addExactOrdered(self, commandArgs):
        raise NotImplementedError

    def addMission(self, commandArgs, missionId):
        raise NotImplementedError

    def addNumSims(self, commandArgs, n):
        raise NotImplementedError

    def addOrdered(self, commandArgs):
        raise NotImplementedError

    def addQuest(self, commandArgs, questId):
        raise NotImplementedError

    def addRaid(self, commandArgs, raidId):
        raise NotImplementedError

    def addSurge(self, commandArgs):
        raise NotImplementedError
