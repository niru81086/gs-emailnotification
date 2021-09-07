pip install kombu
pip install rabbitMQ

After run django application --
We can use this URL for publishing data in queue
http://HostName:PORTNo

Need to change below urls:
Change RabbitMQ URL which is in views.py If want
rabbit_url = "amqp://admin:admin123@10.43.13.19:5672"





