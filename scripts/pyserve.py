#! python3.6
import socket
import json
import os
from kombu import Connection, Exchange, Queue, Consumer
import df_crawl

exch = Exchange("crawl", type="direct")
crawl_queue = Queue(name='dtasks', exchange=exch, routing_key='dfs')

print("pyserve: starting connection to cloudamqp ... ")
rabbit_url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')

def on_request(body, message):
    print("running df_crawl")
    print(body)
    args = json.loads(body)
    site = args["website"]
    dep = args["depth"]
    df_crawl.df_crawl(site, dep)
    
    
with Connection(rabbit_url) as conn:
    with conn.Consumer(crawl_queue, callbacks=[on_request]) as consumer:
        # Process messages and handle events on all channels
        while True:
            conn.drain_events()




    
