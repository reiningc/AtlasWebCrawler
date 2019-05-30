#! python3.6
import pika, os
import threading
from urllib.parse import urlparse
import json
#import df_crawl
#import bf_crawl
# Parse CLODUAMQP_URL (fallback to localhost)
url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
url = urlparse(url_str)
params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
    credentials=pika.PlainCredentials(url.username, url.password))

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
channel.exchange_declare(exchange='crawl', exchange_type='direct', durable='true')
channel.queue_declare(queue='dfs', durable='true') # Declare a queue
channel.queue_declare(queue='bfs', durable='true')
channel.queue_bind(exchange='crawl', queue='dfs', routing_key='dfs')
channel.queue_bind(exchange='crawl', queue='bfs', routing_key='bfs')
# create a function which is called on incoming messages
def on_request(ch, method, properties, body):
  print (body)

# set up subscription on the queue
channel.basic_consume(queue='dfs', on_message_callback=on_request)


channel.start_consuming() # start consuming (blocks)






    
