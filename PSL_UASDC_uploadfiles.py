#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  FILE NAME    : PSL_UAS-DC_uploadfiles.py
#
#  AUTHOR       : Christopher J. Cox, NOAA/PSL
#  DATE         : 8 May 2024  
#
#  SUMMARY      :
#
#  USAGE        : Note that you cannot access AWS S3 while using PSL VPN.
#
#  DEPENDENCIES : Boto3 Python module supported for Python 3.8+ 



def upload_file(path,filename):
    breakpoint()  
    
    # # # # # MAIN # # # # 

    # Get your modules out
    import boto3, os
    from boto3 import client
    from access_info import access_info
    
    # this information is stored in a separate file, access_info.py
    username, aws_key, aws_secret_key, entry_bucket, product_bucket = access_info()
        
    # Filename
    fullfile = path+filename
    
    # We are using AWS S3
    print('    Accessing Amazon AWS S3.')
    s3 = boto3.resource('s3') 
    
    # Setauthentication credentials as environment variables
    os.environ['AWS_ACCESS_KEY_ID'] = aws_key
    os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_key
    

    
    # This does the upload
   ## with open(fullfile, 'rb') as data:
    #    s3.Bucket(entry_bucket).put_object(Key=args.station, Body=data)
        
      
    

    