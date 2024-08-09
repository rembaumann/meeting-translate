import boto3
import os
import uuid
from urllib.parse import unquote_plus
import re
import json

def lambda_handler(event, context):
    # Retrieve the S3 bucket and object information from the event
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_key_enc = event['Records'][0]['s3']['object']['key']
    s3_key = unquote_plus(s3_key_enc)
    
    cleanstring = re.sub('\W+','', s3_key )
    
    print(f"{s3_key} and {s3_bucket}")
    # Generate a unique job name and output file name
    job_name = str(uuid.uuid4())
    
    output_file_name = cleanstring[:20] + "-" + job_name[:4] + ".json"
    
    print(event)
    print(s3_bucket)
    print(s3_key)
    
    # Create an Amazon Transcribe client
    transcribe_client = boto3.client('transcribe')
    
    # Set the S3 URI for the input audio file
    #s3_uri = f"https://s3-us-east-1.amazonaws.com/{s3_bucket}/{s3_key}"
    s3_uri = "s3://" + s3_bucket + "/" + s3_key
    
    print(s3_uri)
    
    # Start the transcription job
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode='en-US',  # Set the language code if different

        Media={
            'MediaFileUri': s3_uri
        },
        Settings={
         'ShowSpeakerLabels': True,
         'MaxSpeakerLabels': 10,
         'VocabularyName': 'aws-finops'
         },
        OutputBucketName='transcribe-output-06132024',
        OutputKey=output_file_name
    )
    
    print(f"Transcription job started with name: {job_name}")
    
    print (json.dumps(response, default=str))
    
    return {
        'TranscriptionJobName': response['TranscriptionJob']['TranscriptionJobName']
    }
