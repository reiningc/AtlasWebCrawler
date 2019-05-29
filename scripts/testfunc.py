#! python3.6
import socket
import json
import os
from kombu import Connection, Exchange, Queue, Consumer, Producer
from kombu.mixins import ConsumerMixin
import df_crawl

print("pyserve: starting connection to cloudamqp ... ")
rabbit_url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')

def on_request(body, message):
    print("running df_crawl")
    print(body)
    args = json.loads(body)
    site = args["website"]
    dep = args["depth"]
    df_crawl.df_crawl(site, dep)
    

class Worker(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues
    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_request])]
    def on_message(self, body, message):
        print('Got message: {0}'.format(body))
        message.ack()


exch = Exchange("crawl", type="direct")
queues = [Queue("dtasks", exch, routing_key="dfs"), Q("btasks", exch, routing_key="bfs")]
with Connection(rabbit_url) as conn:
        worker = Worker(conn, queues)
        worker.run()
