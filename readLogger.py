#!usr/bin/env python
import json
import os

log_file = os.environ.get(
    'pylogger_file',
    os.path.expanduser('~/Desktop/logi.json')
)
listOfFrequncy = []
def getValueBytime(startDate,startTime, endDate, endTime):
    valuesList = []
    with open(log_file) as f:
        data = json.load(f)
    for tm in data:
        if tm["Date"] >= startDate and tm["Date"] <= endDate:
            if (tm["Time"] >= startTime and tm["Date"] < endDate) or (tm["Time"] <= endTime and tm["Date"] > startDate):
                print ("{0} {1} {2}".format(tm["Value"],tm["Date"],tm["Time"]))
                s = ("{0} {1} {2}".format(tm["Value"],tm["Date"],tm["Time"]))
                valuesList.append(s)
        if tm["Date"] == startDate == endDate and tm["Time"] >= startTime and tm["Time"] <= endTime:
            print("{0} {1} {2}".format(tm["Value"], tm["Date"], tm["Time"]))
            s = ("{0} {1} {2}".format(tm["Value"], tm["Date"], tm["Time"]))
            valuesList.append(s)
    if not valuesList:
        s = "There are no values in the log between the given times"
        valuesList.append(s)
    print()
    return valuesList

def getValueFrequency(valu):
    with open(log_file) as f:
        data = json.load(f)
    count = 0
    listOfFrequncy = []
    for tm in data:
        if tm["Value"] == valu :
            count += 1
            s = "{0} {1} {2}".format(tm["Value"],tm["Date"],tm["Time"])
            listOfFrequncy.append(s)
    if count != 0 :
        s = ("\"{0}\" appears {1} times in the key logger \n".format(valu,count))
        listOfFrequncy.append(s)
    else :
        s = ("The given value \"{0}\" is not in the key logger \n".format(valu))
        listOfFrequncy.append(s)
    return listOfFrequncy

def isWordExist(word):
    startTime = ""
    startDate = ""
    i=0
    listOfFrequncy = []
    count = 0
    with open(log_file) as f:
        data = json.load(f)
    for tm in data:

        if tm["Value"] == word[i]:
            if i == 0:
                startTime = tm["Time"]
                startDate = tm["Date"]
            i += 1
        else :
            i = 0
        if i >= len(word):
             if not listOfFrequncy:
                s = "The first time the word \"{0}\" appeared in the key logger was: {1} {2}".format(word,startDate,startTime)
             else:
                 s = "Another time that the word \"{0}\" appeared in the key logger was: {1} {2}".format(word, startDate,startTime)
             count += 1
             listOfFrequncy.append(s)
             i = 0

    if not listOfFrequncy:
        s = "The given word \"{0}\" is not in the key logger".format(word)
        listOfFrequncy.append(s)
    else:
        s = ("\"{0}\" appears {1} times in the key logger".format(word, count))
        listOfFrequncy.append(s)
    return listOfFrequncy


#getValueBytime("22/07/19","01:32:00","24/07/19","12:00:46")
#getValueFrequency("f")
#t = isWordExist("ppp")
#for i in t:
#    print(i)

