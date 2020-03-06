#!/usr/bin/env python

import sys
import os
import subprocess
import pymongo
import re

def getModules():
    if 'HIVE_DB_URI' in os.environ:
        uri = os.environ['HIVE_DB_URI']
    c = pymongo.MongoClient(uri)
    proj = {"$project" : {"_id" : 1.0, "description" : "$description","name" : "$name"}}
    return c["hive"].get_collection("hiveavailablemodules").aggregate([proj])

def getModuleRequirements(ip):
    if 'HIVE_DB_URI' in os.environ:
        uri = os.environ['HIVE_DB_URI']
    c = pymongo.MongoClient(uri)

    rgx = re.compile(".*"+ip+".*")
    pipeline = [
        { "$match" : { "hostname" : rgx }}, 
        { "$project" : { "_id" : 1.0, "hostname" : 1.0, "name" : 1.0}}, 
        { "$lookup" : { 
            "from" : "hivemachines", 
            "let" : { "hostname" : "$hostname"}, 
            "pipeline" : [
              { "$match" : { "$expr" : {"$eq" : ["$$hostname", "$name"]}}}, 
              { "$project" : { 
                  "_id" : 0.0, 
                  "gpu_usage" : { "$cond" : [{ "$gt" : ["$hardware.gpu.usage", 0.0]}, 1, 0]}, 
                  "gpu_avail" : { "$cond" : [{ "$eq" : ["$hardware.gpu.usage", 0.0]}, 1, 0]}}}], 
            "as" : "machines"}}, 
        { "$unwind" : { 
            "path" : "$machines"}}, 
        { "$lookup" : { 
            "from" : "hiveavailablemodules", 
            "let" : { 
              "module_id" : "$_id", 
              "hostname" : "$hostname", 
              "name" : "$name", 
              "gpu_usage" : "$machines.gpu_usage", 
              "gpu_avail" : "$machines.gpu_avail"}, 
            "pipeline" : [
              { "$match" : { "$expr" : { "$eq" : [{ "$concat" : ["hive.", { "$substr" : ["$_id", 5.0, -1.0]}]}, "$$name"]}}}, 
              { "$project" : { 
                  "_id" : 0.0, 
                  "cpu_when_gpu" : { "$multiply" : ["$hardware.cpu_when_gpu_available", "$$gpu_avail"]}, 
                  "cpu" : { 
                    "$multiply" : [
                      {"$multiply" : ["$hardware.cpu", { "$subtract" : [1, "$$gpu_avail"]}]}, 
                      {"$subtract" : [1, { "$multiply" : ["$hardware.gpu", "$$gpu_usage"]}]}]}, 
                  "gpu" : { "$multiply" : ["$hardware.gpu", "$$gpu_usage"]}, 
                  "ram" : "$hardware.ram"}}], 
            "as" : "active_module"}}, 
        { "$unwind" : {"path" : "$active_module"}}, 
        { "$project" : { "name" : "$name", 
            "total_cpu" : { "$sum" : ["$active_module.cpu", "$active_module.cpu_when_gpu"]}, 
            "gpu" : "$active_module.gpu", 
            "ram" : "$active_module.ram"}}, 
        { "$group" : { "_id" : {"$concat" : ["hive_", {"$substr" : ["$name", 5.0, -1.0]}]}, 
            "cpu" : {"$sum" : "$total_cpu"}, 
            "ram" : {"$sum" : "$ram"}, 
            "gpu" : {"$sum" : "$gpu"}}}]

    return c["hive"].get_collection("hivemodules").aggregate(pipeline)

def get_ip():
    ip_command = "ip route get 1 | awk '{print $NF;exit}'"
    p = subprocess.Popen([ip_command], stdout=subprocess.PIPE, shell=True)
    output = p.stdout.read().decode('utf-8')
    ip = output.replace('.','-').strip()
    return ip

def doData():
    ip = get_ip()
    for k in getModuleRequirements(ip):
        print( k["_id"] + ".value " + str(k["gpu"]) )

def doConfig():
    print "graph_title GPU Hive Requirements"
    print "graph_args --base 1000 -l 0"
    print "graph_vlabel GPU Used (1) or Unused (0)"
    print "graph_category system"
    print "graph_total total"
    for k in getModules():
        kname = k["_id"]
        print(kname + ".label " + k["name"])
        print(kname + ".info " + k["description"])
        print kname + ".type GAUGE"
        print kname + ".min 0"
        print kname + ".draw AREASTACK"

if __name__ == "__main__":
    from os import environ
    if 'HIVE_DB_URI' in environ:
        uri = environ['HIVE_DB_URI']

    if len(sys.argv) > 1 and sys.argv[1] == "config":
        doConfig()
    else:
        doData()
