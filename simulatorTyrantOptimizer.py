#!/usr/bin/env python

import re
import subprocess

from fansiteSimulator import FansiteSimulator

class SimulatorTyrantOptimizer(FansiteSimulator):
    name = "Tyrant Optimizer"
    executable = "tyrant_optimize.exe"
    results_regex = re.compile(r"win%: \S+ \((\d+) out of (\d+)\)"
        r"\s+draw%: \S+ \((\d+) out of \d+\)"
        r"\s+loss%: \S+ \((\d+) out of \d+\)"
        r"\s+ANP: (\S+)")
    results_keys = ["wins", "total", "draws", "losses", "anp"]

    def loadVersion(self):
        commandArgs = [self.executable, "-version"]
        result = subprocess.check_output(commandArgs)
        return result.split()[2]

    def processResults(self, results):
        match = self.results_regex.search(results)
        if match:
            return dict(zip(self.results_keys, match.groups()))
        print("ERROR: Cannot find results from output {{{\n", results, "}}}")

    def addAchievement(self, commandArgs, achievementId, missionId):
        commandArgs.append("Mission #%s" % missionId)
        commandArgs.extend(["-A", str(achievementId)])

    def addAttackingDeck(self, commandArgs, attackingDeck, attackingDeckCards):
        commandArgs.append(attackingDeck)

    def addBattlegroundId(self, commandArgs, battlegroundId):
        commandArgs.extend(["-e", str(battlegroundId)])

    def addCustom(self, commandArgs, custom):
        commandArgs.append(custom)

    def addExtraArgs(self, commandArgs, args):
        commandArgs.extend(["-t", str(getattr(args, "numThreads", 1))])
        commandArgs.extend(["sim", str(args.numSims)])

    def addMission(self, commandArgs, missionId):
        commandArgs.append("Mission #%s" % missionId)

    def addOrdered(self, commandArgs):
        commandArgs.append("-r")

    def addQuest(self, commandArgs, questId):
        commandArgs.append("Quest #%s" % questId)

    def addRaid(self, commandArgs, raidId):
        commandArgs.append("Raid #%s" % raidId)

    def addSurge(self, commandArgs):
        commandArgs.append("-s")

