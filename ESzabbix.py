#!/usr/bin/env python

# Created by Aaron Mildenstein on 19 SEP 2012

from pyes import *
import sys

# Define the fail message
def zbx_fail():
    print "ZBX_NOTSUPPORTED"
    sys.exit(2)
    
searchkeys = ['query_total', 'fetch_time_in_millis', 'fetch_total', 'fetch_time', 'query_current', 'fetch_current', 'query_time_in_millis']
getkeys = ['missing_total', 'exists_total', 'current', 'time_in_millis', 'missing_time_in_millis', 'exists_time_in_millis', 'total']
docskeys = ['count', 'deleted']
indexingkeys = ['delete_time_in_millis', 'index_total', 'index_current', 'delete_total', 'index_time_in_millis', 'delete_current']
storekeys = ['size_in_bytes', 'throttle_time_in_millis']
cachekeys = ['field_size_in_bytes', 'field_evictions']
filerkeys = ['filter_size_in_bytes']
clusterkeys = searchkeys + getkeys + docskeys + indexingkeys + storekeys
returnval = None

# __main__

# We need to have two command-line args: 
# sys.argv[1]: The node name or "cluster"
# sys.argv[2]: The "key" (status, filter_size_in_bytes, etc)

if len(sys.argv) < 3:
    zbx_fail()

# Try to establish a connection to elasticsearch
try:
    conn = ES('localhost:9200',timeout=25,default_indices=[''])
except Exception, e:
    zbx_fail()

if sys.argv[1] == 'cluster':
    if sys.argv[2] in clusterkeys:
        # nodestats = conn.cluster.node_stats()
        nodestats = conn._send_request('GET', '_nodes/stats')
        subtotal = 0
        for nodename in nodestats['nodes']:
            if sys.argv[2] in indexingkeys:
                indexstats = nodestats['nodes'][nodename]['indices']['indexing']
            elif sys.argv[2] in storekeys:
                indexstats = nodestats['nodes'][nodename]['indices']['store']
            elif sys.argv[2] in getkeys:
                indexstats = nodestats['nodes'][nodename]['indices']['get']
            elif sys.argv[2] in docskeys:
                indexstats = nodestats['nodes'][nodename]['indices']['docs']
            elif sys.argv[2] in searchkeys:
                indexstats = nodestats['nodes'][nodename]['indices']['search']
            try:
                subtotal += indexstats[sys.argv[2]]
            except Exception, e:
                pass
        returnval = subtotal


    else:
        # Try to pull the managers object data
        try:
            escluster = managers.Cluster(conn)
        except Exception, e:
            zbx_fail()
        # Try to get a value to match the key provided
        try:
            returnval = escluster.health()[sys.argv[2]]
        except Exception, e:
            zbx_fail()
        # If the key is "status" then we need to map that to an integer
        if sys.argv[2] == 'status':
            if returnval == 'green':
                returnval = 0
            elif returnval == 'yellow':
                returnval = 1
            elif returnval == 'red':
                returnval = 2
            else:
                zbx_fail()

# Mod to check if ES service is up
elif sys.argv[1] == 'service':
    if sys.argv[2] == 'status':
        # returnval = 1 if conn.collect_info() else 0
        try:
            info = {}
            res = conn._send_request('GET', "/")
            info['server'] = {}
            info['server']['name'] = res['name']
            info['server']['version'] = res['version']
            info['allinfo'] = res
            info['status'] = self.indices.status()
            info['aliases'] = self.indices.aliases()
            conn.info = info
            returnval = 1
        except:
            conn.info = {}
            returnval = 0

else: # Not clusterwide, check the next arg

    # nodestats = conn.cluster.node_stats()
    nodestats = conn._send_request('GET', '_nodes/stats')
    print nodestats
    for nodename in nodestats['nodes']:
        if sys.argv[1] in nodestats['nodes'][nodename]['name']:
            # if sys.argv[2] in indexingkeys:
            #     stats = nodestats['nodes'][nodename]['indices']['indexing']
            # elif sys.argv[2] in storekeys:
            #     stats = nodestats['nodes'][nodename]['indices']['store']
            # elif sys.argv[2] in getkeys:
            #     stats = nodestats['nodes'][nodename]['indices']['get']
            # elif sys.argv[2] in docskeys:
            #     stats = nodestats['nodes'][nodename]['indices']['docs']
            # elif sys.argv[2] in searchkeys:
            #     stats = nodestats['nodes'][nodename]['indices']['search']
            # elif sys.argv[2] in cachekeys:
            #     stats = nodestats['nodes'][nodename]['indices']['fielddata']
            # elif sys.argv[2] in filerkeys:
            #     stats = nodestats['nodes'][nodename]['indices']['filter_cache']
            stats = nodestats['nodes'][nodename]['indices'][sys.argv[2]]
            try:
                returnval = stats[sys.argv[3]]
            except Exception, e:
                pass


# If we somehow did not get a value here, that's a problem.  Send back the standard 
# ZBX_NOTSUPPORTED
if returnval is None:
    zbx_fail()
else:
    print returnval

# End

