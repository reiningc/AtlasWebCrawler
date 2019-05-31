#! python3.6
import pika, os
import threading
from urllib.parse import urlparse
import json
import df_crawl
import bf_crawl
# Parse CLODUAMQP_URL (fallback to localhost)
url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
url = urlparse(url_str)
params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
    credentials=pika.PlainCredentials(url.username, url.password))

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel

channel.queue_declare(queue='search', durable='true') # Declare a queue
# create a function which is called on incoming messages
def on_request(ch, method, properties, body):
  print ('pyserve.py received request body: ',body)
  args = json.loads(body)
  site = args["website"]
  dep = args["depth"]
  results = df_crawl.df_crawl(site, dep)
  ch.basic_publish(exchange='', routing_key=properties.reply_to, body=results)
  ch.basic_ack(delivery_tag=method.delivery_tag)
    

# set up subscription on the queue
channel.basic_consume(queue='search', on_message_callback=on_request)

print('pyserve.py starts consuming')
channel.start_consuming() # start consuming (blocks)
print('pyserve.py finished consuming')





    
