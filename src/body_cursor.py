
def doData():
    for k,v in getServerStatus()["wiredTiger"]["cursor"].items():
        print(( str(k).replace(" ", "_") + ".value " + str(v) ))

def doConfig():

    print("graph_title MongoDB cursor")
    print("graph_args --base 1024 -l 0 --vertical-label number")
    print("graph_category MongoDB")

    for k in getServerStatus()["wiredTiger"]["cursor"]:
        print(k.replace(" ", "_") + ".label " + k)
        print(k.replace(" ", "_") + ".min 0")
        print(k.replace(" ", "_") + ".type COUNTER")
        print(k.replace(" ", "_") + ".draw LINE1")
