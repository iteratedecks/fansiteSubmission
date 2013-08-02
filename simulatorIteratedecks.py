import re
import subprocess
import os

from fansiteSimulator import FansiteSimulator

class SimulatorIteratedecks(FansiteSimulator):
    name = "iteratedecks"

    # Bugfix: On posix the simulator is called without .exe
    if os.name == "posix":
        executable = "./iteratedecks-cli3"
    else:
        executable = "iteratedecks-cli3.exe"

    def loadVersion(self):
        commandArgs = [SimulatorIteratedecks.executable, "--core-version"]
        result = subprocess.check_output(commandArgs)
        version = result.strip();
        return version;

    def processResults(self, results):
        iterateDecksRegex = "\D+(\d+)[^\n]*\n"
        iterateDecksRegex += "\D+(\d+)[^\n]*\n"
        iterateDecksRegex += "\D+(\d+)[^\n]*\n"
        iterateDecksRegex += "\D+(\d+)[^\n]*\n"
        iterateDecksRegex += "\D+(\d+)[^\n]*\n"
        iterateDecksRegex = re.compile(iterateDecksRegex)
        simResults = iterateDecksRegex.match(results).groups()

        results = {}
        results["wins"] = simResults[1]
        results["total"] = simResults[0]
        results["losses"] = simResults[2]
        results["draws"] = simResults[3]
        results["ard"] = float(simResults[4]) / float(simResults[0])

        return results

    def simulate(self, deck, args):
        commandArgs = [self.executable]
        deck2Type = deck["type"]

        if ("attackingDeck" in deck):
            deck1Base64RLEMinus = deck["attackingDeck"]
            # unclear what this testrepository actually supports, I guess
            # the attacker is limited to BASE64 enconding with RLE and a
            # freaky minus, optionally ordered.
            if("isOrdered" in deck and deck["isOrdered"]):
                commandArgs.append("--attacker")
                commandArgs.append("BASE64RLEMINUS_ORDERED:" + deck1Base64RLEMinus)
            else:
                commandArgs.append("--attacker")
                commandArgs.append("BASE64RLEMINUS:" + deck1Base64RLEMinus)
        elif("attackingDeckCards" in deck):
            attackingDeckCards = deck["attackingDeckCards"]
            if("isOrdered" in deck and deck["isOrdered"]):
                commandArgs.append("--attacker")
                commandArgs.append("IDS_ORDERED:" + attackingDeckCards)
            else:
                commandArgs.append("--attacker")
                commandArgs.append("IDS:" + attackingDeckCards)            

        # this all corresponds to the defender I guess
        if(deck2Type == "raid"):
            self.addRaid(commandArgs, deck["raidId"])
        elif(deck2Type == "mission"):
            self.addMission(commandArgs, deck["missionId"])
        elif(deck2Type == "quest"):
            self.addQuest(commandArgs, deck["questId"])
        elif(deck2Type == "custom"):
            self.addCustom(commandArgs, deck["defendingDeck"])

        elif(deck2Type == "ach"):
            #raise NotImplementedError, "achievements not yet supported"
            if("missionId" in deck):
                self.addMission(commandArgs, deck["missionId"])    
            self.addAchievement(commandArgs, deck["achId"])
            #else:
            #    print("Skipping achievement " + str(deck["achId"]) + " because it has no mission id.")
            #    return # don't run the simulation

        else:
            raise "Unknown deck type "+ deck2Type;

        if("battlegroundId" in deck):
            self.addBattlegroundId(commandArgs, deck["battlegroundId"])

        if("isSurge" in deck and deck["isSurge"]):
            self.addSurge(commandArgs)

        if("isDelayed" in deck and deck["isDelayed"]):
            self.addDelayed(commandArgs)

        self.addExtraArgs(commandArgs, args)

        #print("Running " + " ".join('"%s"' % arg if " " in arg else arg for arg in commandArgs))
        result = subprocess.check_output(commandArgs)
        return self.processResults(result)

    def addAchievement(self, commandArgs, achievementId):
        commandArgs.append("--achievement-id")
        commandArgs.append(str(achievementId))

    def addAttackingDeck(self, commandArgs, attackingDeck, attackingDeckCards):
        commandArgs.append("--attacker")
        commandArgs.append('BASE64RLEMINUS' + attackingDeck)

    def addBattlegroundId(self, commandArgs, battlegroundId):
        commandArgs.append("--battleground-id")
        commandArgs.append(str(battlegroundId))

    def addCustom(self, commandArgs, custom):
        commandArgs.append("--defender")
        commandArgs.append('BASE64RLEMINUS:' + custom)

    def addExtraArgs(self, commandArgs, args):
        commandArgs.extend(["-n", str(args.numSims)])
        commandArgs.append("--allow-invalid-decks");
        commandArgs.append("--no-cache-read");

    def addMission(self, commandArgs, missionId):
        commandArgs.append("--defender")
        commandArgs.append('MISSIONID:' + str(missionId))

    def addOrdered(self, commandArgs):
        # that should not happen
        raise NotImplementedError("Not possible: ordered without a deck.")

    def addQuest(self, commandArgs, questId):
        commandArgs.append("--defender")
        commandArgs.append('QUESTID:' + str(questId))
        raise NotImplementedError("Not supported yet")

    def addRaid(self, commandArgs, raidId):
        commandArgs.append("--defender")
        commandArgs.append('RAIDID:' + str(raidId))
        commandArgs.append("--raid-rules true")

    def addSurge(self, commandArgs):
        commandArgs.append("--surge")

