import os

def getDefaultConfig():
    config = []
    config.append("# Config file for use with Fansite submission script\n")
    config.append("# your simulation token (provided by the Fansite)")
    config.append("token=00000000000000000000000000000000")
    config.append("# the name of the simulator")
    config.append("simulator=iteratedecks")
    config.append("# the number of simulations per deck")
    config.append("numSims=20000")
    return("\n".join(config))

def getArgs(config = "fansite_config.txt"):
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

    args = {}
    for line in contents.splitlines():
        if(len(line) == 0 or line[0] == "#"):
            continue
        arg = line.split('=')
        args[arg[0]] = arg[1]
    return args
