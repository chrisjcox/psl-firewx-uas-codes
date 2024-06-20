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
#  USAGE        : python3 process_UASDC.py -o 007 -a AstonMartinDB5 -t 19641222000000 -d /Users/Connery/London/ -f goldfinger.nc
#                                             |      |                 |                 |
#                                             v      v                 v                 v
#                 arguments                   opID   airframeID        yyyymmddhhmmss    base directory
#
#                 Note that -a and -t are optional arguments. -o, -d, and -f are required. -a is needed if you want to change what is in the raw file. 
#                 The order arguments are entered does not matter.
#
#  PREP         : Create two folders, RAW and STAGE in the base directory,
#                 which is the directory you specify as an argument when
#                 executing the function. When you transfer a file from the 
#                 ground station, store in in RAW then ecexute this code.
# 
#  DEPENDENCIES : netCDF4 1.6.2+, Boto3 Python module supported for Python 3.8+ 

#python3 process_UASDC.py -o 007 -a AstonMartinDB5 -t 19641222000000 -d /Users/ccox/Documents/Projects/2024/FireWeather/compare_files/ -f 20240501221756_Lat_47.5738578_Lon_9.0461255.nc

# Prologue    
import argparse, shutil, sys, os
import netCDF4 as nc
from PSL_UASDC_check_attributes import check_vars_atts
from PSL_UASDC_uploadfiles import upload_file

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--operatorID', metavar='str', help='Operator ID')
parser.add_argument('-a', '--airframeID', metavar='str', help='Airframe ID')
parser.add_argument('-t', '--flighttime', metavar='str', help='Flight time yyyymmddhhmmss')
parser.add_argument('-d', '--basedir', metavar='str', help='Parent directory of RAW and STAGE')
parser.add_argument('-f', '--filename', metavar='str', help='File to process')
args = parser.parse_args()

if args.operatorID: operatorID = args.operatorID
if args.basedir:    base_dir = args.basedir
if args.filename:   fname = args.filename

# check basedir for format
if base_dir[-1] != '/':
    base_dir = base_dir+'/'


# try to get the flight time from the file name if not passed as arg. if that 
# fails, tell user to manually supply it.
if args.flighttime: 
    flighttime = args.flighttime
    if flighttime[-1] != 'Z':
        flighttime = flighttime+'Z'
else:
    flighttime = fname[0:14]
    if not flighttime.isdigit():
        print('')
        print('    Exiting. Filename unexpected format. Please supply flighttime as argument; i.e., -t yyyymmddhhmmss')
        print('')
        sys.exit()        
    flighttime = flighttime+'Z'

# try to get the platform ID (airframe ID) from the globals if not provided
if args.airframeID: 
    airframeID = args.airframeID
else:
    file = nc.Dataset(base_dir+'RAW/'+fname,'r')
    try:
        airframeID = file.getncattr('platform_name')
    except:       
        print('')
        print('    Exiting. platform_name not found in global atts. Please supply it as airframeID argument; i.e., -a name')
        print('')
    


# # # STEP 1. Move and rename the file  # # #

# format: UASDC_operatorID_airframeID_YYYYMMDDHHMMSSZ.nc
new_fname = 'UASDC_'+operatorID+'_'+airframeID+'_'+flighttime+'.nc'


if os.path.exists(base_dir+'STAGE/'+new_fname):
    
    print('')
    proceed = input('    The file already exists in STAGE. Do you want to overwrite it? enter y or n: ')
    print('')
    
    if proceed != 'y':
        print('    Exiting. Nothing was accomplished.')
        print('')
        sys.exit()

# copy file from RAW to STAGE, renaming as we go
shutil.copyfile(base_dir+'RAW/'+fname, base_dir+'STAGE/'+new_fname)


# # # STEP 2. Check vars and atts # # #

check_vars_atts(base_dir+'STAGE/',new_fname,airframeID)


# # # STEP 3. Upload # # #

print('')
proceed = input('    Your file is ready to upload to the bucket. Would you like to proceed? enter y or n: ')
print('')

if proceed != 'y':
    print('    Exiting without upload to bucket.')
    sys.exit()
else:
    upload_file(base_dir+'STAGE/',new_fname,operatorID,airframeID)
    





