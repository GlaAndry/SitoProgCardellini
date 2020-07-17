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
S3_KEY                    = 'ASIAYEAFIJNSNY7JEPJF' 
S3_SECRET                 = 'qnz6u78wPPbWP3wCA9JtrQ5OysZP+OnSgJnQ8AUB'
SESSION_TOKEN             = 'FwoGZXIvYXdzEDsaDACIffh6m8KYrj0ofyLLAWtldAKpy+jbsRCluDNe/JZLHnEWopUKDbtwHlEGdOnuIoYisYb1zD57ri/Pu9gk1MCTAwlK5TQU/M2Lbg9DuN9i84mWlZ1ptJMEXwndCWL1xEEQuwEylNkEzQPlaGefcUbiePkFAZlFUNlPUdRVRjPQxTMwCi1clqagVVaNoiCkHHc0qaiDGdTBcYBmyOGTqig4ClXgZdMs8hk+sK7GYT2HpdcwYQlahncddn/NP0flunFWhYwPStI+hR2PoUYw7Cd6WV/PD2k//XKsKLTaxfgFMi3H4O1WNFc7ods8jS2yo7ZqfVV1v19OJO03NJix4cbhei6mKdGy50Cqq0IePT4='

LOCATION                  = 'us-east-1'

#S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

#SECRET_KEY                = os.urandom(32)
#DEBUG                     = True
#PORT                      = 5000


####COGNITO

CLIENTID                   = '3tc8id07k4id807almsi6orhme'
IDENTITYIDPOOL             = 'us-east-1_itDQgZIS5'