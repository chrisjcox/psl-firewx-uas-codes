#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  FILE NAME    : PSL_UAS-DC_uploadfiles.py
#
#  AUTHOR       : Christopher J. Cox, NOAA/PSL
#  DATE         : 8 May 2024  
#
#  SUMMARY      :
#
#  USAGE        : 
#
#  DEPENDENCIES : Boto3 Python module supported for Python 3.8+ 



def upload_file(path,filename):
    
    # CONFIG OPTIONS
    #   Instead of using a config file, we will keep it self-contained and relay 
    #   authentication credentials to AWS/boto3 through environmental variables. 
    #   Hopefully this keeps things portable and less prone to premissions issues.
    #
    #
    # Config data provided by J. Intrieri 8 May 2024
    username        = 'WMO-UASDC-Participant'
    aws_key         = ***REMOVED***
    aws_secret_key  = ***REMOVED***
    entry_bucket    = ***REMOVED***
    product_bucket  = ***REMOVED***
    
    
    # # # # # MAIN # # # # 
    
    # Get your modules out
    import boto3, os
        
    # Filename
    fullfile = path+filename
    
    # We are using AWS S3
    s3 = boto3.resource('s3') 
    
    # Setauthentication credentials as environment variables
    os.environ['AWS_ACCESS_KEY_ID'] = aws_key
    os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_key
    
    # This is not needed, but FYI, these are the buckets we have access to
    for bucket in s3.buckets.all(): print(bucket.name)
    
    # This does the upload
    with open(fullfile, 'rb') as data:
        s3.Bucket(entry_bucket).put_object(Key=args.station, Body=data)
        
      
        
      # list data
        
        from boto3 import client
    
    conn = client('s3')  # again assumes boto.cfg setup, assume AWS S3
    for key in conn.list_objects(Bucket=***REMOVED***)['Contents']: print(key['Key'])
        
    for key in conn.list_objects(Bucket=***REMOVED***)['Contents']: print(key['Key'])    
    
    