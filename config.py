import logging
##########################################################################
# You must install MySQL server, because without it script does not work #
##########################################################################

# MySQL database configuration block
# create database MySQL and enter here your options
user = 'root'
password = '159951'
db_name = 'integral'
host = '127.0.0.1'
##########################################################################

# telegram settings block
TELEGRAM_TOKEN = ''
PROXY = '91.187.75.48:39668'
##########################################################################

# logging settings block
logging.basicConfig(filename='log.txt', level=logging.INFO)
log = logging.getLogger('MAIN')
##########################################################################





