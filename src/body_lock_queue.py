
def doData():
    for k,v in getServerStatus()["globalLock"]["currentQueue"].items():
        print(( str(k) + ".value " + str(v) ))

def doConfig():

    print("graph_title MongoDB global lock queue")
    print("graph_args --base 1024 -l 0 --vertical-label number")
    print("graph_category MongoDB")

    for k in getServerStatus()["globalLock"]["currentQueue"]:
        print(k + ".label " + k)
        print(k + ".min 0")
        print(k + ".draw LINE1")
