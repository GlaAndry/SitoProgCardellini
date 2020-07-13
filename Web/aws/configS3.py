import os

##stores lambda function
S3_LAMBDASTORE                   = 's3lamdafunctionstore'


##stores images
S3_BUCKET_RESIZE                 = 's3bucketresizefunction'
S3_BUCKET_BeW                    = 's3bucketblackwhitefunction'
S3_BUCKET_BRIGHTNESS             = ''
S3_BUCKET_SATURATION             = ''



##Tutti questi dati cambiano ogni nuova sessione, sono quindi da modificare ad ogni nuovo avvio
S3_KEY                    = '' 
S3_SECRET                 = ''
SESSION_TOKEN             = ''


#S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

#SECRET_KEY                = os.urandom(32)
#DEBUG                     = True
#PORT                      = 5000
