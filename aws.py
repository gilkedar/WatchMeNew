from boto3.session import Session
import time
import cv2


ACCESS_KEY = "AKIAJ3RA6DBYVN4CP6NA"
SECRET_KEY = "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"
REGION ="us-east-1"
BUCKET = "movies111"

FILEPATH = "C:\Users\gilke\My Shows\Family Guy\Family.Guy.S15E15.720P - Avs.mkv"

session = Session(aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY,
                  region_name=REGION)
s3 = session.resource("s3")
start = time.time()
s3.Bucket(BUCKET).Object('fgmovie').upload_file(FILEPATH)
end = time.time()
print end-start
