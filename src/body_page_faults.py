
name = "page_faults"

def get():
    return getServerStatus()["extra_info"][name]


def doData():
    print((name + ".value " + str(get())))


def doConfig():

    print("graph_title MongoDB page faults")
    print("graph_args --base 1000 -l 0")
    print("graph_vlabel faults / ${graph_period}")
    print("graph_category MongoDB")
    print("graph_total total")

    print(name + ".label " + name)
    print(name + ".min 0")
    print(name + ".type COUNTER")
    print(name + ".max 10000")
    print(name + ".draw LINE1")
