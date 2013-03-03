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
        self.addAttackingDeck(commandArgs, deck["attackingDeck"], deck["attackingDeckCards"])

        if(type == "raid"):
            self.addRaid(commandArgs, deck["raidId"])

        elif(type == "mission"):
            self.addMission(commandArgs, deck["missionId"])

        elif(type == "quest"):
            self.addQuest(commandArgs, deck["questId"])

        elif(type == "custom"):
            self.addCustom(deck["customHash"])
            commandArgs.append(commandArgs, str(deck["customHash"]))

        elif(type == "ach"):
            self.addAchievement(commandArgs, deck["achId"], deck["missionId"])

        else:
            print("unknown deck type: " + type)
            return

        if(deck["isOrdered"]):
            self.addOrdered(commandArgs)

        if(deck["isSurge"]):
            self.addSurge(commandArgs)

        if(deck["isDelayed"]):
            self.addDelayed(commandArgs)

        self.addNumSims(commandArgs, numSims)

        print("Running " + " ".join(commandArgs))
        result = subprocess.check_output(commandArgs)
        return self.processResults(result)

    def processResults(self, results):
        raise NotImplementedError

    def loadVersion(self):
        raise NotImplementedError

    def addAttackingDeck(self, commandArgs, attackingDeck, attackingDeckCards):
        raise NotImplementedError

    def addRaid(self, commandArgs, raidId):
        raise NotImplementedError

    def addMission(self, commandArgs, missionId):
        raise NotImplementedError

    def addQuest(self, commandArgs, questId):
        raise NotImplementedError

    def addCustom(self, commandArgs, custom):
        raise NotImplementedError

    def addAchievement(self, commandArgs, achievementId, missionId):
        raise NotImplementedError

    def addOrdered(self, commandArgs):
        raise NotImplementedError

    def addSurge(self, commandArgs):
        raise NotImplementedError

    def addDelayed(self, commandArgs):
        raise NotImplementedError

    def addNumSims(self, commandArgs, n):
        raise NotImplementedError
