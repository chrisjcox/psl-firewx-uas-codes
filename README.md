# PSL FireWX UAS codes

In 2024, the NOAA Physical Sciences Laboratory (PSL) is developing uncrewed aircraft meteorolological observing capabilities to support forecasting pertaining to fire weather ("FireWX") through support from the Bipartisan Infrastructure Law. PSL's new capabilities will be demonstrated during the UAS Demonstration Campaign [(UASDC)] (https://community.wmo.int/en/uas-demonstration), under the auspices of the World Meteorological Organization (WMO), which will evaluate the potential for UAS to contribute to the Global Basic Observing Network with near-real-time data. The focus data are atmospheric profiles of basic meteorology, which are used as inputs to initialize weather forecasts globally.

Data management for UASDC will be hosted in Amazon Web Services (AWS) cloud (Amazon S3) where netCDF files will be archived and converted to WMO BUFR format automatically by services developed by Synoptic Data PBC. Participant data providers (e.g., PSL) will upload observations that meet pre-determined, standardized [format requirements] (https://github.com/synoptic/wmo-uasdc/tree/main/raw_uas_to_netCDF) specified by campaign organizers. The codes found in this repository support PSL's contribution to UASDC to upload near-real-time data from the field, specifically, (a) performing checks and corrections on file formats, (b) managing the AWS upload, and (c) providing feedback to the PSL UAS flight team of the status of the submitted data. Following UASDC, these codes will be further developed to support the general capability for near-real-time provision of PSL's UAS observations that are inclusive of but not exclusive to WMO/Global Telecommunications System standards.

## Getting started

1. Checkout the code form this repository, including
2. Read this README and the code documentation

## Code description: 

A general description of the steps to use the toolkit:

...

## Required software:

The following python packages are required:

~~~
python  ≥ 3.8
netCDF4 ≥ 1.3.0
boto3 ≥ ??
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
