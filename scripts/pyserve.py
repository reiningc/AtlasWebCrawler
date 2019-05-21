#! python3.6
import socket

import os
from kombu import Connection, Exchange, Queue, Consumer
import testfunc

crawl_queue = Queue('tasks')
print("pyserve: starting connection to cloudamqp ... ")
rabbit_url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')

def on_request(body, message):
    n = int(body)
    print("running testfunc")
    response = testfunc.add1(n)
    print("results: %d" + str(response))


with Connection(rabbit_url) as conn:
    with conn.Consumer(crawl_queue, callbacks=[on_request]) as consumer:
        # Process messages and handle events on all channels
        while True:
            conn.drain_events()




    
