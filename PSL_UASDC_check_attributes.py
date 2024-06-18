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
#  DEPENDENCIES : netCDF4 1.6.2+ 

def check_vars_atts(path,fname):
    
    import os, sys
    import netCDF4 as nc
    from wmo_definitions import define_wmo_globals, define_wmo_atts, define_alt_names
    from datetime import datetime

    # assign wmo_definitions
    global_atts = define_wmo_globals()
    wmo_atts = define_wmo_atts()
    namelist = define_alt_names()
    
    print('    Checking and correcting UASDC formatting')   
    print('')
    
    
    # open the file
    file = nc.Dataset(path+fname,'a')
    
    
    # # # STEP 1. Change the time stamp from seconds since flight to epoch # # #
    
    # We need to change the values of the time stamp, which are in seconds 
    # since flight time, but need to be seconds since epoch
    time_var = file.variables['time']
    epoch = datetime(1970, 1, 1)
    add_offset = (datetime.strptime(fname[-18:-4], '%Y%m%d%H%M%S') - epoch).total_seconds()
    # check to make sure there isn't already epoch formatting
    if max(time_var) < 86400:
        time_var[:] = time_var[:]+add_offset
     

    # # # STEP 2. Rename the variable names # # # 
    
    for wmo_var_name, wmo_var_atts in wmo_atts.items():
    
        # if the wmo variable name is not found in the file
        if wmo_var_name not in file.variables:
    
            # try to find a similar name
            for old_name in namelist[wmo_var_name]:
    
                if old_name in file.variables:
                    # success! rename
                    file.renameVariable(old_name,wmo_var_name)
    
    
    
    # # # STEP 3. Check the attributes # # # 
    
    for file_var_name, file_var_atts in file.variables.items():
        
        # if the variable in the file is not requried by WMO, we will still update 
        # the attributes to be consistent
        if file_var_name not in wmo_atts:
            
            # make a dictionary of all attributes and delete the att
            attdict = dict()        
            for att in file.variables[file_var_name].ncattrs():
                attdict.update({att:file.variables[file_var_name].getncattr(att)})
                file.variables[file_var_name].delncattr(att)
    
            # the first att will be fill value
            file.variables[file_var_name].setncattr(file_var_name+'__FillValue','NaN')
           
            for att in attdict.items():
                
                if att[0] == 'standard_name':
                    file.variables[file_var_name].setncattr('long_name',att[1])
                else:
                    file.variables[file_var_name].setncattr(att[0],att[1])
            
        # if the variable is a wmo requirement
        elif file_var_name in wmo_atts:
            
            # make a dictionary of all attributes and delete the att
            attdict = dict()        
            for att in file.variables[file_var_name].ncattrs():
                attdict.update({att:file.variables[file_var_name].getncattr(att)})
                file.variables[file_var_name].delncattr(att)
    
            # write wmo atts
            for att in wmo_atts[file_var_name].items():    
                if att[0] == 'varname__FillValue':
                    file.variables[file_var_name].setncattr(file_var_name+'__FillValue','NaN')
                else:
                    file.variables[file_var_name].setncattr(att[0], att[1])
                
            # write any extra atts that remain    
            for att in attdict.items():  
                if att not in file.variables[file_var_name].ncattrs():
                    if att[0] != 'standard_name':
                        file.variables[file_var_name].setncattr(att[0],att[1])
    
    
    
    # # # STEP 4. Check global attributes # # # 
    
    # make a dictionary of all attributes and delete the att
    attdict = dict()        
    for att in file.ncattrs():
        attdict.update({att:file.getncattr(att)})
        file.delncattr(att)
    
    # write the globals wmo expects                    
    for att in global_atts.items():
     
        if att[0] not in attdict: 
            print('    Warning: '+att[0]+' not found in file global attributes')    
    
        if att[0] == 'platform_name':
            file.setncattr('platform_name',attdict['platform_name'])
        elif att[0] == 'flight_id':
            file.setncattr('flight_id',attdict['flight_id'])   
        elif att[0] == 'processing_level':
            file.setncattr('processing_level','raw') 
            print('    Assigning processing level to raw.')
        else:
            file.setncattr(att[0],att[1]) 
        
        if att[0] in attdict:
            del attdict[att[0]]
    
     # write extra globals
    for att in attdict.items():
        file.setncattr(att[0],att[1]) 
            
    file.close()

        
        
        
        