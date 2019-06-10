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

channel.queue_declare(queue='search', durable='false') # Declare a queue
# create a function which is called on incoming messages
def on_request(ch, method, properties, body):
  print ('pyserve.py received request body: ',body)
  args = json.loads(body)
  crawl = args["searchType"]
  site = args["website"]
  dep = args["depth"]
  keyword = None
  results = None
  
  # Check if keyword has been provided
  if args["keyword"] != "":
    keyword = args["keyword"]
    print('keyword: ', keyword)

  # Acknowledges receipt of crawl request from queue
  ch.basic_ack(delivery_tag=method.delivery_tag)

  # Run selected crawl
  if crawl == "bfs":
    results = bf_crawl.bf_crawl(site,dep,keyword)
  else:
    results = df_crawl.df_crawl(site,dep,keyword)

  ch.basic_publish(exchange='', routing_key=properties.reply_to, body=results)

    

# set up subscription on the queue
channel.basic_consume(queue='search', on_message_callback=on_request)

print('pyserve.py starts consuming')
channel.start_consuming() # start consuming (blocks)
print('pyserve.py finished consuming')





    
