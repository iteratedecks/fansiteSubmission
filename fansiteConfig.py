import sys
import os
import argparse

def getDefaultConfig():
    return """\
# Config file for use with Fansite submission script

# your simulation token (provided by the Fansite)
token=00000000000000000000000000000000
# the name of the simulator
simulator=Tyrant Optimizer
# the number of simulations per deck
numSims=1000000
# the number of CPU threads for simulation
numThreads=1
"""

def getArgs():
    args = getCommandArgs()
    args = getConfigArgs(args, args.config)
    return args

def getCommandArgs():
    argParser = argparse.ArgumentParser(description='Submit simulator results to the Fansite.')
    argParser.add_argument('-t', '--test', action='store_const', default=0, const=1, help='run against test repo')
    argParser.add_argument('--config', default='fansite_config.txt', help='path to config file')
    argParser.add_argument('--token', help='simulator token')
    argParser.add_argument('--simulator', help='simulator used')
    argParser.add_argument('--numSims', help='number of simulations to run per deck')
    argParser.add_argument('--numThreads', help='number of CPU threads for simulation')
    argParser.add_argument('--limit', default=None, help='amount of decks to simulate')
    argParser.add_argument('--runForever', action='store_const', default=0, const=1, help='run forever (Ctrl-Break to stop)')
    args = argParser.parse_args()
    return args

def getConfigArgs(args, config = "fansite_config.txt"):
    contents = None
    if(not os.path.exists(config)):
        print("Could not find config file. Creating one with default settings.")
        with open(config, 'w') as f:
            contents = getDefaultConfig()
            f.write(contents)
    else:
        with open(config, 'r') as f:
            contents = f.read()

    for line in contents.splitlines():
        if(len(line) == 0 or line[0] == "#"):
            continue
        arg = line.split('=')
        if getattr(args, arg[0]) is None:
            setattr(args, arg[0], arg[1])
    return args

