import os

##stores lambda function
S3_LAMBDASTORE                   = 's3lamdafunctionstore'


##stores images
S3_BUCKET_RESIZE                 = 's3bucketresizefunction'
S3_BUCKET_BeW                    = 's3bucketblackwhitefunction'
S3_BUCKET_BRIGHTNESS             = ''
S3_BUCKET_SATURATION             = ''



##Tutti questi dati cambiano ogni nuova sessione, sono quindi da modificare ad ogni nuovo avvio
S3_KEY                    = 'ASIAYEAFIJNSNPF54VVO' 
S3_SECRET                 = 'MwkjAiRxTnNfJCP9OEHg/vBPpIOr2+if2QbMgpGB'
SESSION_TOKEN             = 'FwoGZXIvYXdzEOX//////////wEaDHI+CkLzgjRIXYjI4iLLAQ9jF7XXNNMYBgxzBS8+Z0bBDR6SE3MfUiHZHRKVNqph4O3fbuaj7nfhkgR4Mh3X+Y2yA+UrhH48nBJl8O7wsc68hU0812kaJGPBglQ/eO/nfdl4GBO7QinMZjMbUsbjcj7Db5thja2dIX82jamH5HDTtP+S5WB7wRY5VM/WjaPgGrR4KylGeUYPTskIMJLQFO92qVBz4IHJ2pWM6dybWWH/y55/eQKtZaayqJ3bINyKywxWj7n8F2M5DVpdx3XxWzFCxOKUYB2jhsOaKIfpsvgFMi1vyDi1jKEcwKm6DQuMR8CAnnEH299oEkeN8NLlGZ7g7z6ZqOL+UYNffZtgqjM='


#S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

#SECRET_KEY                = os.urandom(32)
#DEBUG                     = True
#PORT                      = 5000