#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  FILE NAME    : PSL_UAS-DC_check_attributes.py
#
#  AUTHOR       : Christopher J. Cox, NOAA/PSL
#  DATE         : 8 May 2024  
#
#  SUMMARY      : This code checks files for consistency with WMO format, as 
#                 here: https://github.com/synoptic/wmo-uasdc/tree/main/raw_uas_to_netCDF
#
#  USAGE        : 
#
#  DEPENDENCIES : 

import netCDF4 as nc
import os, argparse, shutil
from collections import OrderedDict



# These should be arguments passed
operatorID = 'nnn'
airframeID = 'nnn'
yyyymmddhhmmssz = '20240502023139Z'




# WMO requirements
global_atts = {
    'Conventions'                   :'CF-1.8, WMO-CF-1.0',
    'wmo__cf_profile'               :'FM 303-2024',
    'featureType'                   :'trajectory',
    'platform_name'                 :'airframeID', 
    'flight_id'                     :'JBCC_1500m_VP', 
    'site_terrain_elevation_height' :'3200m',
    'processing_level'              :'raw', 
}

wmo_atts = OrderedDict()

wmo_atts['time'] =                         {'varname__FillValue'  : 'NaN',
                                            'units'               : 'seconds since 1970-01-01T00:00:00',
                                            'long_name'           : 'Time',
                                            'processing_level'    : ''}

wmo_atts['lat'] =                          {'varname__FillValue'  : 'NaN',
                                            'units'               : 'degrees (-90 to 90)',
                                            'long_name'           : 'Latitude',
                                            'processing_level'    : ''}
    
wmo_atts['lon'] =                          {'varname__FillValue'  : 'NaN',
                                            'units'               : 'degrees (-180 to 180)',
                                            'long_name'           : 'Longitude',
                                            'processing_level'    : ''}

wmo_atts['altitude'] =                     {'varname__FillValue'  : 'NaN',
                                            'units'               : 'Meters Above Sea Level',
                                            'long_name'           : 'altitude (height)',
                                            'processing_level'    : ''}

wmo_atts['air_temperature'] =              {'varname__FillValue'  : 'NaN',
                                            'units'               : 'Kelvin',
                                            'long_name'           : 'Air Temperature',
                                            'processing_level'    : ''}

wmo_atts['dew_point_temperature'] =        {'varname__FillValue'  : 'NaN',
                                            'units'               : 'Kelvin',
                                            'long_name'           : 'Air Dewpoint Temperature',
                                            'processing_level'    : ''}

wmo_atts['wind_direction'] =               {'varname__FillValue'  : 'NaN',
                                            'units'               : 'degrees',
                                            'long_name'           : 'Wind Direction',
                                            'processing_level'    : ''}

wmo_atts['wind_speed'] =                   {'varname__FillValue'  : 'NaN',
                                            'units'               : 'm/s',
                                            'long_name'           : 'Wind Speed',
                                            'processing_level'    : ''}

wmo_atts['relative_humidity'] =            {'varname__FillValue'  : 'NaN',
                                            'units'               : '%',
                                            'long_name'           : 'Relative Humidity',
                                            'processing_level'    : ''}

wmo_atts['humidity_mixing_ratio'] =        {'varname__FillValue'  : 'NaN',
                                            'units'               : 'kg/kg',
                                            'long_name'           : 'Humidity Mixing Ratio',
                                            'processing_level'    : ''}

wmo_atts['turbulent_kinetic_energy'] =     {'varname__FillValue'  : 'NaN',
                                            'units'               : 'm2 s-2',
                                            'long_name'           : 'Turbulent Kinetic Energy',
                                            'processing_level'    : ''}

wmo_atts['eddy_dissipation_rate'] =        {'varname__FillValue'  : 'NaN',
                                            'units'               : 'm2/3 s-1',
                                            'long_name'           : 'Mean Turbulence Intensity Eddy Dissipation Rate',
                                            'processing_level'    : ''}

wmo_atts['air_pressure'] =                 {'varname__FillValue'  : 'NaN',
                                            'units'               : 'Pascals',
                                            'long_name'           : 'Air Pressure',
                                            'processing_level'    : ''}

wmo_atts['non_coordinate_geopotential'] =  {'varname__FillValue'  : 'NaN',
                                            'units'               : 'm2 s-2',
                                            'long_name'           : 'Geopotential',
                                            'processing_level'    : ''}

wmo_atts['geopotential_height'] =          {'varname__FillValue'  : 'NaN',
                                            'units'               : 'geopotential meters',
                                            'long_name'           : 'Geopotential Height',
                                            'processing_level'    : ''}



namelist = OrderedDict()

namelist['time'] = {'timestamp'}
namelist['lat'] = {'latitude'}
namelist['lon'] = {'longitude'}
namelist['altitude'] = {'alt'}
namelist['air_temperature'] = {'temp'}
namelist['dew_point_temperature'] = {'dew_point'}
namelist['wind_direction'] = {'wind_dir','wdir'}
namelist['wind_speed'] = {'wind_spd','wspd'}
namelist['relative_humidity'] = {'rel_hum','rh'}
namelist['humidity_mixing_ratio'] = {'mixing_ratio','mr'}
namelist['turbulent_kinetic_energy'] = {'tke'}
namelist['eddy_dissipation_rate'] = {'edr'}
namelist['air_pressure'] = {'air_press'}
namelist['non_coordinate_geopotential'] = {'gpt'}
namelist['geopotential_height'] = {'gph','gpt_height'}




# STEP 1. Create a copy of the file and rename.

path  = '/Users/ccox/Documents/Projects/2024/FireWeather/compare_files/'
fname = '20240501221756_Lat_47.5738578_Lon_9.0461255.nc'

# format: UASDC_operatorID_airframeID_YYYYMMDDHHMMSSZ.nc
nname = 'UASDC_'+operatorID+'_'+airframeID+'_'+yyyymmddhhmmssz+'.nc'


shutil.copyfile(path+fname, path+nname)

file = nc.Dataset(path+nname,'a')



# First rename the variable names
for wmo_var_name, wmo_var_atts in wmo_atts.items():
    
    # if the wmo variable name is not found in the file
    if wmo_var_name not in file.variables:
        
        # try to find a similar name
        for old_name in namelist[wmo_var_name]:
            
            if old_name in file.variables:
                # success! rename
                file.renameVariable(old_name,wmo_var_name)
                
file.close()        
        
        
        
        