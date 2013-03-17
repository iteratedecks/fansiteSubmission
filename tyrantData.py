import hashlib
import httplib
import os

def getCheck(dataDirectory = ""):
    check = {}
    files = ["achievements", "cards", "missions", "quests", "raids"]
    for filename in files:
        path = os.path.join(dataDirectory, filename + ".xml")
        if os.path.exists(path):
            with open(path, 'rb') as f:
                contents = f.read()
            md5hash = hashlib.md5(contents).hexdigest()
            check[filename] = md5hash
    return check

def updateDataFiles(source = "kg.tyrantonline.com", dataDirectory = "", files = ["achievements", "cards", "missions", "quests", "raids"]):
    print("Getting data from " + source)
    for filename in files:
        fileSource = "/assets/" + filename + ".xml"
        fileDest = dataDirectory + filename + ".xml"
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
