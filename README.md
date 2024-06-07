# PSL FireWX UAS codes

In 2024, the NOAA Physical Sciences Laboratory (PSL) is developing uncrewed aircraft meteorolological observing capabilities to support forecasting pertaining to fire weather ("FireWX") through support from the Bipartisan Infrastructure Law. PSL's new capabilities will be demonstrated during the UAS Demonstration Campaign [(UASDC)] (https://community.wmo.int/en/uas-demonstration), under the auspices of the World Meteorological Organization (WMO), which will evaluate the potential for UAS to contribute to the Global Basic Observing Network with near-real-time data. The focus data are atmospheric profiles of basic meteorology, which are used as inputs to initialize weather forecasts globally.

Data management for UASDC will be hosted in Amazon Web Services (AWS) cloud (Amazon S3) where netCDF files will be archived and converted to WMO BUFR format automatically by services developed by Synoptic Data PBC. Participant data providers (e.g., PSL) will upload observations that meet pre-determined, standardized [format requirements] (https://github.com/synoptic/wmo-uasdc/tree/main/raw_uas_to_netCDF) specified by campaign organizers. The codes found in this repository support PSL's contribution to UASDC to upload near-real-time data from the field, specifically, (a) performing checks and corrections on file formats, (b) managing the AWS upload, and (c) providing feedback to the PSL UAS flight team of the status of the submitted data. Following UASDC, these codes will be further developed to support the general capability for near-real-time provision of PSL's UAS observations that are inclusive of but not exclusive to WMO/Global Telecommunications System standards.

## Getting started

1. Checkout the code form this repository, including
2. Read this README and the code documentation

## Code description: 

A general description of the steps to use the toolkit:

Most important for the user:

- access_info.py: Access information for the AWS S3 cloud. **This file contains sensitive information, thus this repo is not visible outside the research team.**

- openS3.py: This is a tool to query the contents of the AWS S3 cloud

      SUMMARY      : This is a set of tools that can be used to open the AWS S3
                    bucket and display what is inside.
    
      USAGE        : Note that you cannot access AWS S3 while using PSL VPN.
                    This would show the buckets available to us:
                      python3 openS3.py -t product
                    This would show contents of the UASDC entry bucket:
                      python3 openS3.py -t entry   
                    This would show contents of the UASDC product bucket:
                      python3 openS3.py -t product

- process_UASDC.py: This is your main code. 

      SUMMARY      : This is the only function the flight crew needs to use.
                    Driver for processing routines for PSL's UASDC participation.
                    Once the netCDF produced by the drone is transferred to the 
                    STAGE directory (see below), the following will happen:
        
                    1) File will be copied to the UPLOAD directory and renamed
                        according to UASDC specificiations.
                    2) File variable names and attributes will be checked for
                        conformity with UASDC specifications and corrected 
                        as necessary.
                    3) File will be uploaded to the AWS Bucket.
                    4) Status of upload will be provided and user will be
                        prompted for monitoring of UASDC Data Pipeline for
                        successful deposit to product bucket.                     
    
      USAGE        : python3 process_UASDC.py -o 007 -a AstonMartinDB5 -t 19641222000000 -d /Users/Connery/London/ -f goldfinger.nc
                                                |      |                 |                 |
                                                v      v                 v                 v
                    arguments                   opID   airframeID        yyyymmddhhmmss    base directory
    
      PREP         : Create two folders, RAW and STAGE in the base directory,
                    which is the directory you specify as an argument when
                    executing the function. When you transfer a file from the 
                    ground station, store in in RAW then ecexute this code.

Sort of important for the user:
- wmo_definitions.py: This is just a series of dictionaries containing information about the WMO requirement formats and some expectations for the netCDFS we will process. If new aircraft or updates to aircraft firmware are made (i.e., changes to aircraft netCDFs) may need to update this.
 

User doesn't need to worry much about it:

- PSL_UASDC_check_attributes.py: Sub that does the check atts.
- PSD_UASDC_uploadfiles.py: Sub that does the uploading.

## Required software:

The following python packages are required:

~~~
python  ≥ 3.8
netCDF4 ≥ 1.3.0
boto3 ≥ Boto3 (1.28.64?) Python module supported for Python 3.8+ 
~~~

## Authors and acknowledgment

Project PI:
* Janet Intrieri (NOAA/PSL) - <janet.intrieri@noaa.gov>

Project Team:
* Gijs de Boer (CIRES, NOAA/PSL) - <gijs.deboer@noaa.gov>
* Jackson Osborn (NOAA/PSL) - <jackson.osborn@noaa.gov>
* Christopher J. Cox (NOAA/PSL) - <christopher.j.cox@noaa.gov>

Code contributors:
* Christopher J. Cox (NOAA/PSL) - <christopher.j.cox@noaa.gov>


## License

TBD

## Project status
This project is currently a non-public collaborative development space for the PSL team.
