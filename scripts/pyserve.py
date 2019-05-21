#! python3.6

import os
from kombu import connection
import testfunc
print("pyserve: starting connection to cloudamqp ... ")
rabbit_url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
conn = Connection(rabbit_url)
channel = conn.channel()
channel.queue_declare(queue='tasks')


def on_request(ch, method, props, body):
    n = int(body)

    print("running testfunc")
    response = testfunc.add1(n)
    print("results: %d" + str(response))
    

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='tasks', on_message_callback=on_request, no_ack=True)

print(" [x] Awaiting RPC requests")
channel.start_consuming()