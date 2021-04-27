
def doData():
    for k,v in getServerStatus()["opLatencies"].items():
        if v["ops"] != 0:
            print(( str(k) + ".value " + str(v["latency"]/v["ops"] ) ))
        else:
            print(( str(k) + ".value " + str(v["latency"] ) ))

def doConfig():

    print("graph_title MongoDB mean ops latencies")
    print("graph_args --base 1000 -l 0")
    print("graph_vlabel microseconds/op")
    print("graph_category MongoDB")

    for k in getServerStatus()["opLatencies"]:
        print(k + ".label " + k)
        print(k + ".draw LINE1")
