import re
import subprocess
import os

from fansiteSimulator import FansiteSimulator

class SimulatorIteratedecks3(FansiteSimulator):
    name = "iteratedecks3"

    # Bugfix: On posix the simulator is called without .exe
    if os.name == "posix":
        executable = "./iteratedecks-cli3"
    else:
        executable = "iteratedecks-cli3.exe"

    def loadVersion(self):
        commandArgs = [SimulatorIteratedecks3.executable, "--core-version"]
        result = subprocess.check_output(commandArgs)
        version = result;        
        return version;

    def processResults(self, results):
        iterateDecksRegex = "\D+(\d+)\D+(\d+)"  # Wins  123 / 200
        iterateDecksRegex += "\D+(\d+)\D+\d+" # Losses    123 / 200
        iterateDecksRegex += "\D+(\d+)\D+\d+" # Draws    123 / 200
        iterateDecksRegex += "\s+.+ANP=([\d\.]+)" # ANP=25.000
        iterateDecksRegex = re.compile(iterateDecksRegex)
        simResults = iterateDecksRegex.match(results).groups()

        results = {}
        results["wins"] = simResults[0]
        results["total"] = simResults[1]
        results["losses"] = simResults[2]
        results["draws"] = simResults[3]
        results["anp"] = simResults[4]

        return results

    def addAchievement(self, commandArgs, achievementId, missionId):
        commandArgs.append("-a")
        commandArgs.append(str(achievementId))
        commandArgs.append("-m")
        commandArgs.append(str(missionId))
        raise "Not supported yet"

    def addAttackingDeck(self, commandArgs, attackingDeck, attackingDeckCards):
        commandArgs.append("--attacker")
        commandArgs.append('"BASE64RLEMINUS' + attackingDeck + '"')

    def addBattlegroundId(self, commandArgs, battlegroundId):
        commandArgs.append("-b")
        commandArgs.append(str(battlegroundId))
        raise "Not supported yet"

    def addCustom(self, commandArgs, custom):
        commandArgs.append(custom)

    def addExtraArgs(self, commandArgs, args):
        commandArgs.extend(["-n", str(args.numSims)])
        commandArgs.append("--seed")

    def addMission(self, commandArgs, missionId):
        commandArgs.append("--defender")
        commandArgs.append('"MISSIONID:' + str(missionId) + '"')

    def addOrdered(self, commandArgs):
        commandArgs.append("-o")
        raise "Not supported yet"

    def addQuest(self, commandArgs, questId):
        commandArgs.append("--defender")
        commandArgs.append('"QUESTID:' + str(questId) + '"')
        raise "Not supported yet"

    def addRaid(self, commandArgs, raidId):
        commandArgs.append("--defender")
        commandArgs.append('"RAIDID:' + str(raidId) + '"')

    def addSurge(self, commandArgs):
        commandArgs.append("--surge")

