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

channel.queue_declare(queue='dfs', durable='true') # Declare a queue
channel.queue_declare(queue='bfs', durable='true')
# create a function which is called on incoming messages
def on_request(ch, method, properties, body):
  print (body)
  args = json.loads(body)
  site = args["website"]
  dep = args["depth"]
  results = df_crawl.df_crawl(site, dep)
  ch.basic_publish(exchange='', routing_key=properties.reply_to, body=results)
    

# set up subscription on the queue
channel.basic_consume(queue='dfs', on_message_callback=on_request)


channel.start_consuming() # start consuming (blocks)






    
