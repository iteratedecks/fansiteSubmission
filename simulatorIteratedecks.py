import re
import subprocess

from fansiteSimulator import FansiteSimulator

class SimulatorIteratedecks(FansiteSimulator):
    name = "iteratedecks"
    executable = "iteratedecks-cli.exe"

    def loadVersion(self):
        return "worldship"
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

        battlesWon = simResults[0]
        battlesTotal = simResults[1]
        anp = simResults[4]

        print(" ... result was: " + battlesWon + "/" + battlesTotal)
        return [battlesWon, battlesTotal, anp]

    def addAttackingDeck(self, commandArgs, attackingDeck, attackingDeckCards):
        commandArgs.append(attackingDeck)

    def addRaid(self, commandArgs, raidId):
        commandArgs.append("-r")
        commandArgs.append(str(raidId))

    def addMission(self, commandArgs, missionId):
        commandArgs.append("-m")
        commandArgs.append(str(missionId))

    def addQuest(self, commandArgs, questId):
        commandArgs.append("-Q")
        commandArgs.append(str(questId))

    def addCustom(self, commandArgs, custom):
        commandArgs.append(custom)

    def addAchievement(self, commandArgs, achievementId, missionId):
        commandArgs.append("-a")
        commandArgs.append(str(achievementId))
        commandArgs.append("-m")
        commandArgs.append(str(missionId))

    def addOrdered(self, commandArgs):
        commandArgs.append("-o")

    def addSurge(self, commandArgs):
        commandArgs.append("-s")

    def addNumSims(self, commandArgs, n):
        commandArgs.append("-n")
        commandArgs.append(str(n))
        commandArgs.append("--seed")
