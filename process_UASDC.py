#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  FILE NAME    : process_UASDC.py
#
#  AUTHOR       : Christopher J. Cox, NOAA/PSL
#  DATE         : 7 June 2024  
#
#  SUMMARY      : This is the only function the flight crew needs to use.
#                 Driver for processing routines for PSL's UASDC participation.
#                 Once the netCDF produced by the drone is transferred to the 
#                 STAGE directory (see below), the following will happen:
#    
#                 1) File will be copied to the UPLOAD directory and renamed
#                    according to UASDC specificiations.
#                 2) File variable names and attributes will be checked for
#                    conformity with UASDC specifications and corrected 
#                    as necessary.
#                 3) File will be uploaded to the AWS Bucket.
#                 4) Status of upload will be provided and user will be
#                    prompted for monitoring of UASDC Data Pipeline for
#                    successful deposit to product bucket.                     
#
#  USAGE        : python3 process_UASDC -o 007 -a AstonMartinDB5 -t 19641222000000
#                                          |      |                 | 
#                                          v      v                 v
#                                          opID   airframeID        yyyymmddhhmmss
# 
#  DEPENDENCIES : netCDF4 1.6.2+, Boto3 Python module supported for Python 3.8+ 

    
import argparse

# arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--operatorID', metavar='str', help='Operator ID')
parser.add_argument('-a', '--airframeID', metavar='str', help='Airframe ID')
parser.add_argument('-t', '--flighttime', metavar='str', help='Flight time yyyymmddhhmmss')
args = parser.parse_args()












