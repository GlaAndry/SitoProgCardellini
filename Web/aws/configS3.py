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
S3_KEY                    = 'ASIAYEAFIJNSNZDHJZEA' 
S3_SECRET                 = 'P49zH/NwDyuXjaIXSZWg3GlZYiluuzsjjFLyk+X0'
SESSION_TOKEN             = 'FwoGZXIvYXdzECoaDHmP3xYHYQD9FRUQdyLLAdRSW0H4uS0hppMtXaoeeTRd2vW++NVlgEckm5+BQF1iXVpJhcut+s/v+FGK8chnpm9MRHiCr7GGQT/uIeX7Kortdv9Sd2Jt/4c22dcRAN8ifL+JBN4HlQ7YIDa64KZphqIA8VSuUT+AqB0bhkzwKpJo8QqZ4f2ESogzLJeAAAzZjTZVozrw/Xi9U7elCO5pMZl1rmXz1aw6lCXSYJ5IYCFtam6n+1pMhO137M49v8trDR+aYoBy8VrjTMhrWl24BrsrkUsa35x/dUgwKK6AwvgFMi1e6DWB30tqbX8u1fsQkqzuJYWe5H5H5QXRTuRa+1rGZnw6lTmJ+y5G3zatFLo='

LOCATION                  = 'us-east-1'

#S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

#SECRET_KEY                = os.urandom(32)
#DEBUG                     = True
#PORT                      = 5000


####COGNITO

CLIENTID                   = '3tc8id07k4id807almsi6orhme'
IDENTITYIDPOOL             = 'us-east-1_itDQgZIS5'