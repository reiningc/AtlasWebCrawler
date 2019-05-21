#! python3.6
import socket
import os
from kombu import Connection, Queue, Consumer
import testfunc
print("pyserve: starting connection to cloudamqp ... ")
rabbit_url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
conn = Connection(rabbit_url)
queue = Queue(name=”tasks”)


def on_request(ch, method, props, body):
    n = int(body)

    print("running testfunc")
    response = testfunc.add1(n)
    print("results: %d" + str(response))
    
with Consumer(conn, queues=queue, callbacks=[on_request], accept=["text/plain"]): 
  while True:
  try:
    conn.drain_events(timeout=2)
  except socket.timeout:
    pass # This will do for now