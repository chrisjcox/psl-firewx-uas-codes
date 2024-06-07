#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  FILE NAME    : openS3.py
#
#  AUTHOR       : Christopher J. Cox, NOAA/PSL
#  DATE         : 8 May 2024  
#
#  SUMMARY      : This is a set of tools that can be used to open the AWS S3
#                 bucket and display what is inside.
#
#  USAGE        : Note that you cannot access AWS S3 while using PSL VPN.
#                 This would show the buckets available to us:
#                   python3 openS3.py -t product
#                 This would show contents of the UASDC entry bucket:
#                   python3 openS3.py -t entry   
#                 This would show contents of the UASDC product bucket:
#                   python3 openS3.py -t product
#
#  DEPENDENCIES : Boto3 Python module supported for Python 3.8+ 



# Get your modules out
import boto3, os, argparse
from boto3 import client
from access_info import access_info

# entry if you want to see the entry bucket, product if you want to see the product bucket, buckets if you want a list of available buckets.
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--task', metavar='str', help='Operator ID')
args = parser.parse_args()
if args.task: task = args.task

# this information is stored in a separate file, access_info.py
username, aws_key, aws_secret_key, entry_bucket, product_bucket = access_info()

# We are using AWS S3
print('')
print('    Accessing Amazon AWS S3.')
print('')

# Setauthentication credentials as environment variables
os.environ['AWS_ACCESS_KEY_ID'] = aws_key
os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_key

# Also, set directly, just in case
s3 = boto3.resource('s3',aws_access_key_id=aws_key,aws_secret_access_key= aws_secret_key)



if task == 'entry':

    print('    Printing contents of UASDC entry bucket:')
    print('')
    conn = client('s3')  # again assumes boto.cfg setup, assume AWS S3
    for key in conn.list_objects(Bucket=***REMOVED***)['Contents']: print(key['Key'])    
    print('')

elif task == 'product':
 
    print('    Printing contents of UASDC product bucket:')
    print('')
    conn = client('s3')  # again assumes boto.cfg setup, assume AWS S3
    for key in conn.list_objects(Bucket=***REMOVED***)['Contents']: print(key['Key'])
    print('')

elif task == 'buckets':

    print('    Printing UASDC S3 buckets list:')
    print('')
    
    for bucket in s3.buckets.all(): 
        try: 
            print(bucket.name) 
        except:
            print('no access')

    print('')