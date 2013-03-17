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

    def simulate(self, deck, args):
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
            self.addAchievement(commandArgs, deck["achId"], deck["missionId"])

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

        self.addExtraArgs(commandArgs, args)

        print("Running " + " ".join('"%s"' % arg if " " in arg else arg for arg in commandArgs))
        result = subprocess.check_output(commandArgs)
        return self.processResults(result)

    def processResults(self, results):
        raise NotImplementedError, "Process Results from Output"

    def loadVersion(self):
        raise NotImplementedError, "Version"

    def addAchievement(self, commandArgs, achievementId, missionId):
        raise NotImplementedError, "Achievement"

    def addAttackingDeck(self, commandArgs, attackingDeck, attackingDeckCards):
        raise NotImplementedError, "Attacking Deck"

    def addBattlegroundId(self, commandArgs, battlegroundId):
        raise NotImplementedError, "Battlegroud Effect"

    def addCustom(self, commandArgs, custom):
        raise NotImplementedError, "Custom Deck"

    def addDelayed(self, commandArgs):
        raise NotImplementedError, "Delayed (tournament mode)"

    def addExactOrdered(self, commandArgs):
        raise NotImplementedError, "Exact Order (ignore 3-card hand rule)"

    def addExtraArgs(self, commandArgs, args):
        pass

    def addMission(self, commandArgs, missionId):
        raise NotImplementedError, "Mission Deck"

    def addOrdered(self, commandArgs):
        raise NotImplementedError, "Ordered Deck (honor 3-card hand rule)"

    def addQuest(self, commandArgs, questId):
        raise NotImplementedError, "Quest Deck"

    def addRaid(self, commandArgs, raidId):
        raise NotImplementedError, "Raid Deck"

    def addSurge(self, commandArgs):
        raise NotImplementedError, "Surge"

