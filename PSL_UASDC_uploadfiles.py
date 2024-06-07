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



def upload_file(path,filename,operatorID,airframeID):

    # # # # # MAIN # # # # 

    # Get your modules out
    import boto3, os, sys
    from access_info import access_info
    
    # this information is stored in a separate file, access_info.py
    username, aws_key, aws_secret_key, entry_bucket, product_bucket = access_info()
        
    # Filename
    fullfile = path+filename

    if fullfile[-19:-16] != '_20':
        print('The file name does not end with _YYYYMMDDhhmmss.nc')
        sys.exit()
        
    # this is how the path to file looks like in the bucket            
    s3_filepath = operatorID+'/'+airframeID+'/'+fullfile[-18:-14]+'/'+fullfile[-14:-12]+'/'+filename

    
    # We are using AWS S3
    print('    Accessing Amazon AWS S3.')
    
    # Setauthentication credentials as environment variables
    os.environ['AWS_ACCESS_KEY_ID'] = aws_key
    os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_key
    
    # just in case
    s3 = boto3.client('s3', aws_access_key_id=aws_key, aws_secret_access_key=aws_secret_key)

    # Upload the file to the S3 bucket
    try:
        s3.upload_file(fullfile, entry_bucket, s3_filepath)
        print(f"File {fullfile} uploaded to {entry_bucket}/{s3_filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")