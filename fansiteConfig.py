import argparse
import os

def getDefaultConfig():
    config = []
    config.append("# Config file for use with Fansite submission script\n")
    config.append("# your simulation token (provided by the Fansite)")
    config.append("token=00000000000000000000000000000000")
    config.append("# the name of the simulator")
    config.append("simulator=iteratedecks")
    config.append("# the number of simulations per deck")
    config.append("numSims=200000")
    return("\n".join(config))

def getArgs():
    args = getCommandArgs()
    args = getConfigArgs(args, args.config)
    return args

def getCommandArgs():
    argParser = argparse.ArgumentParser(description='Submit simulator results to the Fansite.')
    argParser.add_argument('-t', '--test', type=int, nargs='?', default=0, const=1, help='run against test repo')
    argParser.add_argument('--config', default='fansite_config.txt', help='path to config file')
    argParser.add_argument('--token', default='', help='simulator token')
    argParser.add_argument('--simulator', default='', help='simulator used')
    argParser.add_argument('--numSims', default='', help='number of simulations to run per deck')

    args = argParser.parse_args()

    return args

def getConfigArgs(args = {}, config = "fansite_config.txt"):
    contents = None
    if(not os.path.exists(config)):
        print("Could not find config file. Creating one with default settings.")
        f = None
        try:
            f = open(config, 'w')
            contents = getDefaultConfig()
            f.write(contents)
        finally:
            f.close()
    else:
        f = None
        try:
            f = open(config, 'r')
            contents = f.read()
        finally:
            f.close()

    for line in contents.splitlines():
        if(len(line) == 0 or line[0] == "#"):
            continue
        arg = line.split('=')

        if(arg[0] == "token" and args.token == ''):
            args.token = arg[1]
        elif(arg[0] == "simulator" and args.simulator == ''):
            args.simulator = arg[1]
        elif(arg[0] == "numSims" and args.numSims == ''):
            args.numSims = arg[1]

    return args
