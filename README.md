# rundeck-failover
This project helps to setup rundeck failover Setup. Use the script at your own Risk

# Assumption
Rundeck 2.6.x. The mentioned approach tested on 2.6.8.

# To Do
1. Copy the script on the rundeck Failover Server and name it as rundeck-failover.py
2. Replace the following items with Appropriate values.

  PROJECT_FOLDER=YOUR PROJECT FOLDER

  LOG_FOLDER=RUNDECK LOG FOLDER

  EXECUTION_LOGS=RUNDECK EXECUTION LOGS FOLDER

  MASTER_IP_ADDRESS=MASTER-IP-ADDRESS

  FAILOVER_IP_ADDRESS=FAILOVER-IP_ADDRESS 

  RUNDECK_PORT=RUNDECK PORT

  sender_mail = 'your-email-account@domain.tld'

3. Add the script on crontab 
*/15 * * * * scriptpath/rundeck-failover.py

# More Information refer below URL
http://blog.pheonixsolutions.com/rundeck-failover-setup/
