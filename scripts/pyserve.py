#! python3

import pika, os, urlparse
import testfunc

url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
url = urlparse.urlparse(url_str)
params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
    credentials=pika.PlainCredentials(url.username, url.password))

connection = pika.BlockingConnection(params) # Connect to CloudAMQP

channel = connection.channel()

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