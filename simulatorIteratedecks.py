import re
import subprocess

from fansiteSimulator import FansiteSimulator

class SimulatorIteratedecks(FansiteSimulator):
    name = "iteratedecks"
    executable = "iteratedecks-cli.exe"

    def loadVersion(self):
        commandArgs = [SimulatorIteratedecks.executable, "--version"]
        result = subprocess.check_output(commandArgs)
        return result.split()[2]

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

    def addAttackingDeck(self, commandArgs, attackingDeck, attackingDeckCards):
        commandArgs.append(attackingDeck)

    def addBattlegroundId(self, commandArgs, battlegroundId):
        commandArgs.append("-b")
        commandArgs.append(str(battlegroundId))

    def addCustom(self, commandArgs, custom):
        commandArgs.append(custom)

    def addExtraArgs(self, commandArgs, args):
        commandArgs.extend(["-n", str(args.numSims)])
        commandArgs.append("--seed")

    def addMission(self, commandArgs, missionId):
        commandArgs.append("-m")
        commandArgs.append(str(missionId))

    def addOrdered(self, commandArgs):
        commandArgs.append("-o")

    def addQuest(self, commandArgs, questId):
        commandArgs.append("-Q")
        commandArgs.append(str(questId))

    def addRaid(self, commandArgs, raidId):
        commandArgs.append("-r")
        commandArgs.append(str(raidId))

    def addSurge(self, commandArgs):
        commandArgs.append("-s")

