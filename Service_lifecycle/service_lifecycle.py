from time import sleep
from json import dumps
import json
import threading

from algorith_binder import *

import sys
sys.path.insert(0, "../communication_module")

import communication_module as cm


def get_scheduler_msg():

	f = open('scheduler_msg.json',) 
	data = json.load(f)
	print("Service to schedule",data)
	send_request_serverLC(data)
	service_data=bind_algo(data)

	server=recieved_server_details()
	print("\nRecieved Server details:- ",server)
	service_data['server']=server[service_data['reqid']]

	print("\nSending Service details to Deployment Manager\n",service_data)

	send_service_to_deployment(service_data)

	return data

def handle_scheduler_msg(msg):
	
	print("recivie schedule msg",msg)
	send_request_serverLC(msg)

	# recieved_server_details(msg)


def handle_serverLC_msg(msg):
	print("Server LC respond",msg)
	service_data=bind_algo(msg)
	print("Algo binded", service_data)
	send_service_to_deployment(service_data)


def send_service_to_deployment(msg):
	cm.ServiceLifeCycle_to_DeployManager_Producer_interface(msg)


def send_request_serverLC(msg):
	cm.ServiceLifeCycle_to_ServerLifeCycle_Producer_interface(msg)


def recieved_server_details(msg):
	print("\nrecived msg from service \n")
	msg["server_id"]="s1"
	msg["ip"]='127.0.0.1'
	msg["port"]=8090
	cm.ServerLifeCycle_to_ServiceLifeCycle_Producer_interface(msg)
	
th=threading.Thread(target=cm.ServerLifeCycle_to_ServiceLifeCycle_interface,kwargs={'func_name':handle_serverLC_msg})
th.start()


th=threading.Thread(target=cm.Schedular_to_ServiceLifeCycle_interface,kwargs={'func_name':handle_scheduler_msg})
th.start()

# th=threading.Thread(target=cm.ServiceLifeCycle_to_ServerLifeCycle_interface,kwargs={'func_name':recieved_server_details})
# th.start()

#cm.Schedular_to_ServiceLifeCycle_interface(handle_scheduler_msg)

