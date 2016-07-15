#!/usr/bin/python
#Author:support@pheonixsolutions.com
#Description: Script to setup Failover
#Schedule this script on cron to run every 15 minutes
#Love to do in Python
#Version:1.0
import os,sys,socket
import xml.etree.ElementTree
import smtplib
import email
import email.mime.text
import string
# Required Variables
PROJECT_FOLDER='/var/rundeck/projects'
LOG_FOLDER='/var/log/rundeck'
EXECUTION_LOGS='/var/lib/rundeck/logs'
MASTER_IP_ADDRESS='<MASTER-IP-ADDRESS>'
FAILOVER_IP_ADDRESS='<FAILOVER-IP_ADDRESS>' 
RUNDECK_PORT=8000 
sender_mail = 'rundeck-failover@domain.tld' # Mention FROM email address recipients =['email1@domain.tld','email2@domain.tld']#Separated by Comma API_TOKEN='YOUR API TOKEN' print "Checking whether Rundeck Master server is responding.." check_socket=socket.socket() try: check_socket.connect((MASTER_IP_ADDRESS,RUNDECK_PORT)); #print "Connected to %s on port %s" % (MASTER_IP_ADDRESS, RUNDECK_PORT) # "Syncing data from Master to Slave" os.system('rsync -ratlz root@'+MASTER_IP_ADDRESS+':'+PROJECT_FOLDER+'/* ' +PROJECT_FOLDER+'/') os.system('rsync -ratlz root@'+MASTER_IP_ADDRESS+':'+LOG_FOLDER+'/* ' +LOG_FOLDER+'/') os.system('rsync -ratlz root@'+MASTER_IP_ADDRESS+':'+EXECUTION_LOGS+'/* ' +EXECUTION_LOGS+'/') os.system("curl -H 'X-Rundeck-Auth-Token:"+API_TOKEN+"' http://"+FAILOVER_IP_ADDRESS+":"+str(RUNDECK_PORT)+"/api/2/system/info>/tmp/output_failover.xml");
	e = xml.etree.ElementTree.parse('/tmp/output_failover.xml').getroot()
	for all_elements in e:
		for executions in all_elements:
			if(executions.tag =='executions'):
				#Checking whether Failover server is active or passive
				if(executions.get('executionMode') == 'active'):
					os.system('curl -H "X-Rundeck-Auth-Token:'+API_TOKEN+'" -X POST http://'+FAILOVER_IP_ADDRESS+':'+str(RUNDECK_PORT)+'/api/14/system/executions/disable');
					#Sending Notifications
					body="Master Server %s is up. Fail Over Server Execution Mode is Active. Disabling Active Mode on %s\n" %(MASTER_IP_ADDRESS,FAILOVER_IP_ADDRESS)
					body_of_the_message= email.mime.text.MIMEText(body,'html');
					message      = email.MIMEMultipart.MIMEMultipart('alternative')
					message['Subject'] ="Rundeck Fail Over Alert"
					message['From']    = sender_mail
					message.attach(body_of_the_message);
					message['To']=",".join(recipients)
					server = smtplib.SMTP('localhost')
					server.sendmail(message['From'],recipients,message.as_string())
					server.quit()
				elif(executions.get('executionMode') == 'passive'):
					print "Fail Over Server Execution Mode is Passive. Do Nothing..";
				else:
					print "Something is wrong. Please check Fail Over Server %s." %(FAILOVER_IP_ADDRESS)
					body="Rundeck Fail Over Alert: Something is Wrong on %s" %(FAILOVER_IP_ADDRESS)
					body_of_the_message= email.mime.text.MIMEText(body,'html');
					message      = email.MIMEMultipart.MIMEMultipart('alternative')
					message['Subject'] ="Urgent:Rundeck Fail Over Alert. Something is wrong on Failover Server"
					message['From']    = sender_mail
					message['To']=",".join(recipients)
					message.attach(body_of_the_message);
					server = smtplib.SMTP('localhost')
					server.sendmail(message['From'],recipients,message.as_string())
					server.quit()
#If the Master server doesn't Responds, switch the connection
except socket.error, e:
	print "Connection Failed. Master Rundeck server failed %s" %(MASTER_IP_ADDRESS);
	print "Starting Failover Server"
	os.system('curl -H "X-Rundeck-Auth-Token:'+API_TOKEN+'" -X POST http://'+FAILOVER_IP_ADDRESS+':'+str(RUNDECK_PORT)+'/api/14/system/executions/enable');
	body="Rundeck Fail Over Alert: Rundeck Master is Down %s. Failover Completed on %s. Please check " %(MASTER_IP_ADDRESS,FAILOVER_IP_ADDRESS)
	body_of_the_message= email.mime.text.MIMEText(body,'html');
	message      = email.MIMEMultipart.MIMEMultipart('alternative')
	message['From']    = sender_mail
	message['Subject'] ="Urgent: Rundeck Master Server %s is Down. Please check " %(MASTER_IP_ADDRESS)
	message.attach(body_of_the_message);
	message['To']=",".join(recipients)
	server = smtplib.SMTP('localhost')
	server.sendmail(message['From'],recipients,message.as_string())
	server.quit()

