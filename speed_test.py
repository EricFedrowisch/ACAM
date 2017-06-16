from random import seed, randint
from string import ascii_lowercase
from datetime import datetime
from ddict import DDict as d
from time import time


letters = list(ascii_lowercase) # Make list of lowercase letters
def createRandomString():
    s = ''
    for l in range(randint(1,20)):
        s = s + letters[randint(0,len(letters)-1)]
    return s
def t():
    return str(datetime.now())

def elapsed(function):
    def wrapper(*args):
        t1 = time()
        function(*args)
        t2 = time()
        return (t2 - t1)
    return wrapper

@elapsed
def appendTest(toAppend):
    for i in range(0,len(testStrings)):
        toAppend.append(testStrings[i])

@elapsed
def accessTest(toAccess, nAccessTimes):
    for i in xrange(0,nAccessTimes):
        x = toAccess[i]


if __name__ == '__main__':
    s = seed('hashthis') #Use same seed for each test run
    print "Setup Start => " + t()
    print "Creating List of 'random' strings values."
    n = 100000 # Number of items in testStrings
    nAccess = 10000 # Number of times to Access
    testStrings = []
    for i in xrange(n):
        testStrings.append(createRandomString())
    print "Setup Done => " + t()

    print "\n###############################"
    # Test append speeds
    # list
    print "Start Python List Append " + str(n) + " elements => " + t()
    testlist = []
    listAppendSpeed = appendTest(testlist)
    print "Elapsed time: " + str(listAppendSpeed)
    print "Time/Element:" + str(listAppendSpeed/n)
    print "End   Python List Append " + str(n) + " elements => " + t()
    # ddict
    print "Start DDict Append " + str(n) + " elements => " + t()
    testDDict = d()
    ddictAppendSpeed = appendTest(testDDict)
    print "Elapsed time: " + str(ddictAppendSpeed)
    print "Time/Element:" + str(ddictAppendSpeed/n)
    print "End   DDict Append " + str(n) + " elements => " + t()


    print "\n###############################"
    # Test access speeds
    print "Start Python List Access " + str(n) + " elements => " + t()
    listAccessSpeed = accessTest(testlist, nAccess)
    print "Elapsed time: " + str(listAccessSpeed)
    print "Time/Element:" + str(listAccessSpeed/nAccess)
    print "End   Python List Access " + str(n) + " elements => " + t()
    # ddict append speed test
    print "Start DDict Access " + str(n) + " elements => " + t()
    ddictAccessSpeed = accessTest(testDDict, nAccess)
    print "Elapsed time: " + str(ddictAccessSpeed)
    print "Time/Element:"  + str(ddictAccessSpeed/nAccess)
    print "End   DDict Access " + str(n) + " elements => " + t()

    # Test search speeds
    # Test insert speeds
    # Test pop speeds
    # Test sort speeds
    # Test unique value counting speeds
    # Test count
