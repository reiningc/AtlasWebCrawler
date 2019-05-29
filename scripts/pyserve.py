#! python3.6
import pika, os
from urllib.parse import urlparse
# Parse CLODUAMQP_URL (fallback to localhost)
url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
url = urlparse.urlparse(url_str)
params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
    credentials=pika.PlainCredentials(url.username, url.password))

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
channel.queue_declare(queue='dtasks') # Declare a queue

# create a function which is called on incoming messages
def callback(ch, method, properties, body):
  print ("Received: " + body)

# set up subscription on the queue
channel.basic_consume(callback,
    queue='dtasks',
    no_ack=True)

channel.start_consuming() # start consuming (blocks)

connection.close()




    
