import boto3

# Get the service resource
sqs = boto3.resource('sqs')

try:
    queue = sqs.create_queue(QueueName='handson')
except:
    # Get the queue. This returns an SQS.Queue instance
    queue = sqs.get_queue_by_name(QueueName='handson')


queue.send_message(MessageBody='Example', MessageAttributes={
    'Author': {
        'StringValue': 'Gabriele',
        'DataType': 'String'
    }
})

