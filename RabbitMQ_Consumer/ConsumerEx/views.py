import datetime
import time


from kombu import Connection, Exchange
import imghdr
import smtplib
from email.message import EmailMessage
import os
from .readconfig  import ReadConfig
from django.http import HttpResponse
def SimpleConsumer():

    rabbit_url = "amqp://guest:guest@rabbitmq:5672"
    #rabbit_url = "amqp://localhost:5672"
    exchange = Exchange("test_exchange", type="direct")
    with Connection(rabbit_url) as conn:
        with conn.SimpleQueue("simplequeue") as queue:
            queue.exchange_opts = exchange
            queue.no_ack = True
            try:
                # print("call notify", datetime.datetime.now())
                obj = queue.get(block=False)
                data = obj.payload
                print(data)
                sendEmail(data)
            except Exception as ex:
                pass

def SendEmail_QAAutomation():
    rabbit_url = "amqp://guest:guest@rabbitmq:5672"
    #rabbit_url = "amqp://localhost:5672"
    exchange = Exchange("test_exchange", type="direct")
    with Connection(rabbit_url) as conn:
        with conn.SimpleQueue("QA_Automation_Queue") as queue:
            queue.exchange_opts = exchange
            queue.no_ack = True
            try:
                # print("call notify1", datetime.datetime.now())
                obj = queue.get(block=False)
                data = obj.payload
                sendEmail(data)
                # return data
            except Exception as ex:
                pass

def sendEmail(data):
    try:
        senderemail = ReadConfig.getsenderemail()
        senderpass = ReadConfig.getsenderpassword()
        receiveremail = ReadConfig.getreceivermail()
        msg = EmailMessage()
        msg['Subject'] = 'This is Subject'
        msg['From'] = senderemail
        msg['To'] = receiveremail
        msg.set_content(data)
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        filePath = str(BASE_DIR)
        with open(filePath + '/ConsumerEx/test.png', 'rb') as f:

            image_data = f.read()
            image_type = imghdr.what(f.name)
            image_name = f.name
        msg.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

        # for pdf attachment following code :
        '''files = ['LargeElementArray.pdf']
        for file in files:
            with open(file, 'rb') as f:
                file_data = f.read()
                file_name = f.name
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)'''

        smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # smtpObj = smtplib.SMTP('localhost',1025)
        smtpObj.login(senderemail, senderpass)
        smtpObj.send_message(msg)
        smtpObj.quit()

        print("email send successfully")
    except Exception as ex:
        print("Something Went Wrong", ex)

def ConsumerView():
    print("funtion called")
    while True:
        SendEmail_QAAutomation()
        SimpleConsumer()

    #return HttpResponse(200)
