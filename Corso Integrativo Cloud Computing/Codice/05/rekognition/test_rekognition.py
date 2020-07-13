import boto3

rekognition_client=boto3.client('rekognition')
s3_bucket = "sdcchandsontest"

image_name = "panda.png"
image_s3 = {
  'S3Object': {
    'Bucket': s3_bucket, 'Name': image_name
  }
}
response = rekognition_client.detect_labels(
  Image=image_s3,
  MaxLabels=10
)
labels = response["Labels"]
for l in labels:
    print(l)
