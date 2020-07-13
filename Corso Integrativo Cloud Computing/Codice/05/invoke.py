import boto3
import sys
import time
import base64

FUNCTION=sys.argv[1] if len(sys.argv) >= 2 else "helloWorld"
INPUTFILE_NAME="inputfile.txt"
N_CALLS=3

def invoke_function (fname):
    inputfile = open(INPUTFILE_NAME, "rb")

    t = time.time()

    response = client.invoke(
        FunctionName=fname,
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=inputfile,
    )

    duration = time.time()-t
    status_code = response['StatusCode']
    payload = response['Payload'].read().decode('utf-8')
    log_result = base64.b64decode(response['LogResult']).decode('utf-8')

    print("Elapsed time: {:.4f} ms".format(duration*1000))
    print("Status Code: {}".format(status_code))
    print("Payload:\n{}\n---".format(payload))
    print("Log:\n{}\n---".format(log_result))

client = boto3.client('lambda')
for i in range(N_CALLS):
    invoke_function(FUNCTION)
