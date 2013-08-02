#import httplib
import json
import urllib2

def getHeaders():
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json"
    }
    return headers

def doRequest(path, data):
    fansiteUrl = "tyrant.40in.net"
    headers = getHeaders()

    requestData = json.dumps(data)

    request = urllib2.Request(url='http://' + fansiteUrl + path, data=requestData)
    resp = urllib2.urlopen(request)

    return json.loads(resp.read())

def handleGenericErrors(code):
    message = "Unknown error"
    if(code == 997):
        message = "Operation not allowed for your ip"
    elif(code == 998):
        message = "Internal error while processing request. Please try again."
    elif(code == 999):
        message = "Wrong request body. Please try again."

    printError(code, message)

def printError(code, message):
    print("ERROR " + str(code) + ": \t" + message)

# GET DECKS
def getDecks(sessId, limit = None):
    request = getDecksRequestData(sessId, limit)
    json_data = doRequest(request[0], request[1])

    if("errorCode" in json_data):
        handleGetDecksErrors(json_data["errorCode"])

    return json_data

def getDecksRequestData(sessId, limit = None):
    path = "/api/sim/getDecks"

    requestData = {}
    requestData["sessId"] = sessId

    if limit is not None:
        requestData["limit"] = int(limit)

    return [path, requestData]

def handleGetDecksErrors(code):
    if(code == 0):
        return code

    message = "Unknown error"
    if(code == 1):
        print("Empty sessId. Please try again.")
    elif(code == 2):
        print("Unknown sessId. Please try again. If you keep seeing these errors reduce the number of sims per deck.")
    elif(code == 3):
        print("Old sim version. You need to download the latest version of your sim.")
    elif(code == 4):
        print("Wrong limit param value.")
    elif(code > 900):
        handleGenericErrors(code)
    else:
        print("Unknown error code: " + str(code))

    printError(code, message)
    return code


# GET SESSION
def getSession(token, version, check = None):
    request = getSessionRequestData(token, version, check)
    json_data = doRequest(request[0], request[1])

    if("errorCode" in json_data):
        handleGetSessionErrors(json_data["errorCode"])

    return json_data

def getSessionRequestData(accessToken, version, check = None):
    path = "/api/sim/getSession"

    requestData = {}
    requestData["accessToken"] = accessToken
    requestData["version"] = version

    if(not check is None):
        requestData["check"] = check

    return [path, requestData]

def handleGetSessionErrors(code):
    if(code == 0):
        return code

    if(code > 900):
        return handleGenericErrors(code)

    message = "Unknown error"
    if(code == 1):
        message = "Invalid token. Please add your token to the config.txt file."
    elif(code == 2):
        message = "Unknown sim version. You need to download the latest version of your sim."
    elif(code == 3):
        message = "Old sim version. You need to download the latest version of your sim."
    elif(code == 4):
        message = "Invalid check data. You need to download the latest Tyrant xml files."
    elif(code == 101):
        message = "achievements.xml file is missing."
    elif(code == 102):
        message = "achievements.xml is out of date. You need to download the latest Tyrant xml files."
    elif(code == 103):
        message = "cards.xml file is missing."
    elif(code == 104):
        message = "cards.xml is out of date. You need to download the latest Tyrant xml files."
    elif(code == 105):
        message = "missions.xml file is missing."
    elif(code == 106):
        message = "missions.xml is out of date. You need to download the latest Tyrant xml files."
    elif(code == 107):
        message = "quests.xml file is missing."
    elif(code == 108):
        message = "quests.xml is out of date. You need to download the latest Tyrant xml files."
    elif(code == 109):
        message = "raids.xml file is missing."
    elif(code == 110):
        message = "raids.xml is out of date. You need to download the latest Tyrant xml files."

    printError(code, message)
    return code


# SUBMIT SIMULATION
def submitSimulation(deckId, sessId, battlesTotal, battlesWon, timeTaken, anp):
    request = submitSimulationRequestData(deckId, sessId, battlesTotal, battlesWon, timeTaken, anp)
    json_data = doRequest(request[0], request[1])

    if("errorCode" in json_data):
        handleSubmitSimulationErrors(json_data["errorCode"])

    return json_data

def submitSimulationRequestData(deckId, sessId, battlesTotal, battlesWon, timeTaken, anp = None):
    path = "/api/sim/submitSimulation"

    requestData = {}
    requestData["deckId"] = deckId
    requestData["sessId"] = sessId
    requestData["battlesTotal"] = battlesTotal
    requestData["battlesWon"] = battlesWon
    requestData["timeTaken"] = timeTaken

    if(not anp is None):
        requestData["anp"] = anp

    return [path, requestData]

def handleSubmitSimulationErrors(code):
    if(code == 0):
        return code
    if(code > 900):
        return handleGenericErrors(code)

    message = "Unknown error"
    if(code == 1):
        message = "Empty sessId. Please try again."
    elif(code == 2):
        message = "Unknown sessId. Please try again. If you keep seeing these errors reduce the number of sims per deck."
    elif(code == 3):
        message = "Old sim version. You need to download the latest version of your sim."
    elif(code == 4):
        message = "Empty deckId. Please try again."
    elif(code == 5):
        message = "Unknown deckId. Please try again."
    elif(code == 6):
        message = "Wrong battlesTotal. Please report this error to the simulator's developer."
    elif(code == 7):
        message = "Wrong battlesWon. Please report this error to the simulator's developer."
    elif(code == 8):
        message = "Simulations count beyond allowed range. Only values between 50,000 and 10,000,000 are allowed."
    elif(code == 9):
        message = "timeTaken is invalid. Please try again."
    elif(code == 10):
        message = "anp is empty. Please try again."
    elif(code == 11):
        message = "anp is invalid. Please report this error to the simulator's developer."

    printError(code, message)
    return code
