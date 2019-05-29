#! python3.6
import pika, os
import threading
from urllib.parse import urlparse
# Parse CLODUAMQP_URL (fallback to localhost)
url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
url = urlparse(url_str)
params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
    credentials=pika.PlainCredentials(url.username, url.password))

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
channel.exchange_declare(exchange='crawl', exchange_type='direct', durable='true')
channel.queue_declare(queue='dtasks', durable='true') # Declare a queue
channel.queue_declare(queue='btasks', durable='true')
channel.queue_bind(exchange='crawl', queue='dtasks', routing_key='dfs')
channel.queue_bind(exchange='crawl', queue='btasks', routing_key='bfs')
# create a function which is called on incoming messages
def callback(ch, method, properties, body):
  print ("Received: " + body)

# set up subscription on the queue
channel.basic_consume(queue='dtasks', callback)

channel.start_consuming() # start consuming (blocks)






    
