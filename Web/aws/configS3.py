import os

##stores lambda function
S3_LAMBDASTORE                   = 's3lamdafunctionstore'


##stores images
S3_BUCKET_RESIZE                 = 's3bucketresizefunction'
S3_BUCKET_BeW                    = 's3bucketblackwhitefunction'
S3_BUCKET_BRIGHTNESS             = 's3brightnessbucket'
S3_BUCKET_SATURATION             = 's3saturationbucket'

#after-bucket images
S3_BUCKET_RESIZE_AFTER                 = 's3bucketresizefunction-resized'
S3_BUCKET_BeW_AFTER                    = 's3bucketblackwhitefunction-after'
S3_BUCKET_BRIGHTNESS_AFTER             = 's3brightnessbucket-after'
S3_BUCKET_SATURATION_AFTER             = 's3saturationbucket-after'



##Tutti questi dati cambiano ogni nuova sessione, sono quindi da modificare ad ogni nuovo avvio
S3_KEY                    = '' 
S3_SECRET                 = ''
SESSION_TOKEN             = ''

LOCATION                  = 'us-east-1'

#S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

#SECRET_KEY                = os.urandom(32)
#DEBUG                     = True
#PORT                      = 5000


####COGNITO

CLIENTID                   = '3tc8id07k4id807almsi6orhme'
IDENTITYIDPOOL             = 'us-east-1_itDQgZIS5'