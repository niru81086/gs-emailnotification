import time

from django.shortcuts import render
from kombu import Connection, Exchange, Producer, Queue
import json
from django.views import View
from django.http import HttpResponse

# Create your views here.
# class ProducerView(View):

def ProducerView(request):
    #rabbit_url = "amqp://localhost:5672/"
    rabbit_url = "amqp://guest:guest@rabbitmq:5672"
    conn = Connection(rabbit_url)
    channel = conn.channel()
    exchange = Exchange("test_exchange", type="direct")
    producer = Producer(exchange=exchange, channel=channel)
    queue = Queue(name="simplequeue", exchange=exchange, routing_key="simplequeue")
    queue.maybe_bind(conn)
    queue.declare()

    queue = Queue(name="QA_Automation_Queue", exchange=exchange, routing_key="QA_Automation_Queue")
    queue.maybe_bind(conn)
    queue.declare()
    # while True:
    jsonData = {"Message": "Hello World"}
    producer.publish(json.dumps(jsonData), expiration=30, routing_key="simplequeue")  # Queue will empty after 30 second and again it will publish data


    jsonData2 = {"Message": "QA Automation"}
    producer.publish(json.dumps(jsonData2), expiration=30, routing_key="QA_Automation_Queue")  # Queue will empty after 30 second and again it will publish data
    #
    #
    return HttpResponse(200)



