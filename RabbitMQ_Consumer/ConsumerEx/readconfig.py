# baseURL = https://opensource-demo.orangehrmlive.com
# username = Admin
# password = admin123
#
# Sender_email_id =  shabnam.mulla@gmail.com
# Sender_password = **********
# Receiver_email_id = shabnam.mulla@gslab.com
#
#
# This is coding about config file read property
import configparser
import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
config = configparser.RawConfigParser()
test=str(BASE_DIR)
print("#############")
print(test)
config.read(test + "/ConsumerEx/config.ini")

class ReadConfig():

    @staticmethod
    def getsenderemail():
        senderemail = config.get('common info', 'Sender_email_id')
        return senderemail

    @staticmethod
    def getsenderpassword():
        senderepassword = config.get('common info', 'Sender_password')
        return senderepassword

    @staticmethod
    def getreceivermail():
        receivermail = config.get('common info', 'Receiver_email_id')
        return receivermail