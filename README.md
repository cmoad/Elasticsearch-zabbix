Elasticsearch-zabbix
====================

Elasticsearch template and script for zabbix 2.0

This project is a fork of Elasticsearch template from zabbix-grab-bag

https://github.com/untergeek/zabbix-grab-bag

These are made available by me under an Apache 2.0 license.

http://www.apache.org/licenses/LICENSE-2.0.html


How it works
=============

- Clone git repo https://github.com/fneyron/Elasticsearch-zabbix.git and https://github.com/fneyron/pyes.git
- Install pyes : `sudo python setup.py install`
- Install ES zabbix scripts: `sudo ./setup.sh`
- Create a Value Map in Zabbix Administration -> General -> Value Maping (in right dropdown menu):

		ES Cluster State	
		0 ⇒ Green
		1 ⇒ Yellow
		2 ⇒ Red
- Import ESzabbix_templates.xml to zabbix server

IF you have problems try this command: 

		/etc/zabbix/zabbix_externalscripts/ESzabbix.py <hostname> status

It should gave an array with a lot of values about ES cluster

Specs
=====


The items here are for monitoring Elasticsearch (presumably for logstash).

The template xml file actually contains three templates:

1. Elasticsearch Node & Cache (which is for node-level monitoring)

2. Elasticsearch Cluster (cluster state, shard-level monitoring, record count, storage sizes, etc.)

3. Elasticsearch Service (ES service status)

The node name is expected as a host-level macro {$NODENAME}

There are triggers assigned for the cluster state:

0 = Green (OK)

1 = Yellow (Average, depends on "red")

2 = Red (High)


You will likely want to assign a value mapping for the ElasticSearch Cluster Status item.

In any event, the current list of included items is:

* ES Cluster (11 Items)
	- Cluster-wide records indexed per second
	- Cluster-wide storage size
	- ElasticSearch Cluster Status
	- Number of active primary shards
	- Number of active shards
	- Number of data nodes
	- Number of initializing shards
	- Number of nodes
	- Number of relocating shards
	- Number of unassigned shards
	- Total number of records
* ES Cache (2 Items)
	- Node Field Cache Size
	- Node Filter Cache Size
* ES Node (2 Items)
	- Node Storage Size
	- Records indexed per second
* ES Service (1 Item)
	- Elasticsearch service status
