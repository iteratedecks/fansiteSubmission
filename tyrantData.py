import hashlib
import httplib
import os

def getCheck(dataDirectory = ""):
    check = {}

    files = ["achievements", "cards", "missions", "quests", "raids"]

    for file in files:
        path = dataDirectory + file + ".xml"
        hash = None
        if(os.path.exists(path)):
            contents = None
            f = None
            try:
                f = open(path, 'rb')
                contents = f.read()
            finally:
                f.close()
            hash = hashlib.md5(contents).hexdigest()
            check[file] = hash
    return check

def updateDataFiles(source = "kg.tyrantonline.com", dataDirectory = "", files = ["achievements", "cards", "missions", "quests", "raids"]):
    print("Getting data from " + source)

    files = ["achievements"]

    for file in files:

        fileSource = "/assets/" + file + ".xml"
        fileDest = dataDirectory + file + ".xml"
        http = httplib.HTTPConnection(source, 80, timeout=10)
        http.request("GET", fileSource)

        print("Getting http://" + source + fileSource + " ...")
        resp = http.getresponse()
        contents = resp.read()
        # = contents.replace("\r", "X")

        print("Saving " + fileDest + " ...")
        f = None
        try:
            f = open(fileDest, 'wb')
            f.write(contents)
        finally:
            f.close()
