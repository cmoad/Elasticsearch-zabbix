#!/bin/bash

if [[ ! $(find /usr/local/lib/python*/dist-packages/ -name pyes -type d) ]]
then
	echo "Please install pyes first: git clone https://github.com/fneyron/pyes.git"
	exit 1
fi

if [ -d /etc/zabbix/zabbix_agentd.conf.d ]
then 
	cp $PWD/ESzabbix.userparm /etc/zabbix/zabbix_agentd.conf.d/
	if [ ! -d /etc/zabbix/zabbix_externalscripts ]
	then
		mkdir /etc/zabbix/zabbix_externalscripts
	fi
	cp $PWD/ESzabbix.py /etc/zabbix/zabbix_externalscripts/
else
	echo "zabbix agent directory not found please install: /etc/zabbix/zabbix_agentd.conf.d/"
fi

sudo service zabbix-agent restart
 
	
