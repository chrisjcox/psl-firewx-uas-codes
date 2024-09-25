#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  FILE NAME    : quicklooks.py
#
#  AUTHOR       : Christopher J. Cox, NOAA/PSL
#  DATE         : 21 June 2024  
#
#  SUMMARY      :
#
#  USAGE        : python3 quicklooks.py -f file_prefix -p /path/to/RAW/
#
#  DEPENDENCIES : netCDF4, metpy

print('')
print('    Getting Ready.')
print('')
import argparse
import netCDF4 as nc
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os


# OPTIONS
wind_barbs_dz = 10 # vertical spacing (in meters) between plotted wind barbs
paths_dz = 10 # vertical spacing (in meters) between plotted dots for path of the drone


# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--filepath', metavar='str', help='Path to file')
parser.add_argument('-f', '--filename', metavar='str', help='Filename')
args = parser.parse_args()

if args.filepath:   path = args.filepath
if args.filename:   fname = args.filename


# Load files 
print('    Loading files.')
print('')

file_list = sorted(os.listdir(path))
netcdf_files = [f for f in file_list if f.startswith(fname) and f.endswith('.nc')]

datasets = [xr.open_dataset(path+f) for f in netcdf_files]


# Regrid
print('    Regridding data.')
print('')
# Figure out the maximum height above surface
maxHt = []
times = []
for f in datasets: 
    maxHt.append(np.array(f.altitude.max())-np.array(f.altitude[0]))
    times.append(f.time[0].values)
maxHt = np.ceil(maxHt)

# Make a common height grid with 1 m resolution
# Note that the meteodrone data is reported closer to 3-4 m
hts = np.arange(int(max(maxHt))+1)
hts2d = np.transpose(np.tile(hts,(len(times),1)))

# Define some flight_n x ht arrays
wind_v = np.full((len(hts),len(datasets)), np.nan) 
wind_u = np.full((len(hts),len(datasets)), np.nan) 
wind_w = np.full((len(hts),len(datasets)), np.nan) 
temp = np.full((len(hts),len(datasets)), np.nan)
rh = np.full((len(hts),len(datasets)), np.nan)
pr = np.full((len(hts),len(datasets)), np.nan)
thet = np.full((len(hts),len(datasets)), np.nan)
times2d = np.full((len(hts),len(datasets)), np.nan)

# Now loop back through the datasets and interpolate onto the regular grid
counter = 0 
for f in datasets: 
    alts = np.array(f.altitude)-np.array(f.altitude[0])
    wind_u[:,counter] = np.interp(hts,alts,f.wind_u) 
    wind_v[:,counter] = np.interp(hts,alts,f.wind_v) 
    wind_w[:,counter] = np.interp(hts,alts,f.wind_w) 
    temp[:,counter] = np.interp(hts,alts,f.temp)
    rh[:,counter] = np.interp(hts,alts,f.rel_hum) 
    pr[:,counter] = np.interp(hts,alts,f.air_press) 
    thet[:,counter] = np.interp(hts,alts,f.potential_temp)
    times2d[:,counter] = np.interp(hts,alts,f.time.astype('datetime64[ns]').astype('float64'))
    counter = counter + 1
    
times2d=times2d.astype('datetime64[ns]')

wspd = np.sqrt(wind_u**2+wind_v**2+wind_w**2)
wdir = np.mod(180/np.pi * np.arctan2(-wind_u,-wind_v),360)


# Make some plots
print('    Making plots.')
print('')
# Define the figure object and primary axes
plt.rc('font', size=14) 

# Plot RH using contourf
fig = plt.figure(1, figsize=(16., 9.))
ax = plt.axes()
contour1 = ax.contour(times2d, hts2d, rh,levels=np.arange(0, 101, 2), colors='k', linewidths=0.2)
contour2 = ax.contourf(times2d, hts2d, rh,levels=np.arange(0, 101, 2), cmap='YlGnBu')
ax.scatter(times2d[1::paths_dz,:].reshape((len(times)*len(hts[1::paths_dz]),1)), hts2d[1::paths_dz,:].reshape((len(times)*len(hts[1::paths_dz]),1)), color='black', s=1, marker='.')
cbar = rh_colorbar = fig.colorbar(contour2,ticks=np.arange(0,101,10))
cbar.ax.set_ylabel('RH [%]')
myFmt = mdates.DateFormatter('%b%d %H:%M')
ax.xaxis.set_major_formatter(myFmt)
ax.tick_params(axis='x', labelrotation=30)
ax.set_title('Relative Humidity')
ax.set_ylabel('Height AGL [m]')
fig.savefig(path+'rh_'+fname+'.png')
fig.clear()


# Plot temp using contourf
fig = plt.figure(1, figsize=(16., 9.))
ax = plt.axes()
contour1 = ax.contour(times2d, hts2d, temp,levels=np.arange(np.floor(np.min(temp)),np.ceil(np.max(temp)), 0.25), colors='k', linewidths=0.2)
contour2 = ax.contourf(times2d, hts2d, temp,levels=np.arange(np.floor(np.min(temp)),np.ceil(np.max(temp)), 0.25), cmap='YlOrRd')
ax.scatter(times2d[1::paths_dz,:].reshape((len(times)*len(hts[1::paths_dz]),1)), hts2d[1::paths_dz,:].reshape((len(times)*len(hts[1::paths_dz]),1)), color='black', s=1, marker='.')
cbar = rh_colorbar = fig.colorbar(contour2,ticks=np.arange(np.floor(np.min(temp)),np.ceil(np.max(temp))+1, 1))
cbar.ax.set_ylabel('Temperature [K]')
myFmt = mdates.DateFormatter('%b%d %H:%M')
ax.xaxis.set_major_formatter(myFmt)
ax.tick_params(axis='x', labelrotation=30)
ax.set_title('Air Temperature')
ax.set_ylabel('Height AGL [m]')
fig.savefig(path+'temp_'+fname+'.png')
fig.clear()


# Plot wind speed using contourf
fig = plt.figure(1, figsize=(16., 9.))
ax = plt.axes()
contour1 = ax.contour(times2d, hts2d, wspd,levels=np.arange(0,np.ceil(np.max(wspd))+1, 0.5), colors='k', linewidths=0.2)
contour2 = ax.contourf(times2d, hts2d, wspd,levels=np.arange(0,np.ceil(np.max(wspd))+1, 0.5), cmap='YlOrRd')
ax.scatter(times2d[1::paths_dz,:].reshape((len(times)*len(hts[1::paths_dz]),1)), hts2d[1::paths_dz,:].reshape((len(times)*len(hts[1::paths_dz]),1)), color='black', s=1, marker='.')
cbar = rh_colorbar = fig.colorbar(contour2,ticks=np.arange(0,15, 1))
cbar.ax.set_ylabel('Wind Velocity [m/s]')
myFmt = mdates.DateFormatter('%b%d %H:%M')
ax.xaxis.set_major_formatter(myFmt)
ax.tick_params(axis='x', labelrotation=30)
ax.set_title('Wind Velocity')
ax.set_ylabel('Height AGL [m]')
fig.savefig(path+'wspd_'+fname+'.png')
fig.clear()


# Plot Theta using contourf
fig = plt.figure(1, figsize=(16., 9.))
ax = plt.axes()
contour1 = ax.contour(times2d, hts2d, thet,levels=np.arange(np.floor(np.min(thet)),np.ceil(np.max(thet)), 0.25), colors='k', linewidths=0.2)
contour2 = ax.contourf(times2d, hts2d, thet,levels=np.arange(np.floor(np.min(thet)),np.ceil(np.max(thet)), 0.25), cmap='YlOrRd')
ax.scatter(times2d[1::paths_dz,:].reshape((len(times)*len(hts[1::paths_dz]),1)), hts2d[1::paths_dz,:].reshape((len(times)*len(hts[1::paths_dz]),1)), color='black', s=1, marker='.')
cbar = rh_colorbar = fig.colorbar(contour2,ticks=np.arange(np.floor(np.min(thet)),np.ceil(np.max(thet))+1, 1))
cbar.ax.set_ylabel('$\Theta$ [K]')
myFmt = mdates.DateFormatter('%b%d %H:%M')
ax.xaxis.set_major_formatter(myFmt)
ax.tick_params(axis='x', labelrotation=30)
ax.set_title('Potential Temperature')
ax.set_ylabel('Height AGL [m]')
fig.savefig(path+'theta_'+fname+'.png')
fig.clear()

# Plot temp with wind barbs
fig.clear()
fig = plt.figure(1, figsize=(16., 9.))
ax = plt.axes()
contour1 = ax.contour(times2d, hts2d, temp,levels=np.arange(np.floor(np.min(temp)),np.ceil(np.max(temp)), 0.25), colors='k', linewidths=0.2)
contour2 = ax.contourf(times2d, hts2d, temp,levels=np.arange(np.floor(np.min(temp)),np.ceil(np.max(temp)), 0.25), cmap='YlOrRd')
ax.scatter(times2d[1::paths_dz,:].reshape((len(times)*len(hts[1::paths_dz]),1)), hts2d[1::paths_dz,:].reshape((len(times)*len(hts[1::paths_dz]),1)), color='black', s=1, marker='.')
cbar = rh_colorbar = fig.colorbar(contour2,ticks=np.arange(np.floor(np.min(temp)),np.ceil(np.max(temp))+1, 1))
cbar.ax.set_ylabel('Temperature [K]')
wind_slc_vert = np.arange(1,int(max(maxHt))+1,wind_barbs_dz)
ax.barbs(times2d[wind_slc_vert,:], hts2d[wind_slc_vert,:], wind_u[wind_slc_vert, :], wind_v[wind_slc_vert, :], color='k', barb_increments=dict(half=1, full=5, flag=10),clip_on=False)
myFmt = mdates.DateFormatter('%b%d %H:%M')
ax.xaxis.set_major_formatter(myFmt)
ax.tick_params(axis='x', labelrotation=30)
ax.set_title('Air Temperature & Winds')
ax.set_ylabel('Height AGL [m]')
fig.savefig(path+'temp_wind_'+fname+'.png')
fig.clear()


# Plot theta with wind barbs
fig.clear()
fig = plt.figure(1, figsize=(16., 9.))
ax = plt.axes()
contour1 = ax.contour(times2d, hts2d, thet,levels=np.arange(np.floor(np.min(thet)),np.ceil(np.max(thet)), 0.25), colors='k', linewidths=0.2)
contour2 = ax.contourf(times2d, hts2d, thet,levels=np.arange(np.floor(np.min(thet)),np.ceil(np.max(thet)), 0.25), cmap='YlOrRd')
ax.scatter(times2d[1::paths_dz,:].reshape((len(times)*len(hts[1::paths_dz]),1)), hts2d[1::paths_dz,:].reshape((len(times)*len(hts[1::paths_dz]),1)), color='black', s=1, marker='.')
cbar = rh_colorbar = fig.colorbar(contour2,ticks=np.arange(np.floor(np.min(thet)),np.ceil(np.max(thet))+1, 1))
cbar.ax.set_ylabel('$\Theta$ [K]')
wind_slc_vert = np.arange(1,int(max(maxHt))+1,wind_barbs_dz)
ax.barbs(times2d[wind_slc_vert,:], hts2d[wind_slc_vert,:], wind_u[wind_slc_vert, :], wind_v[wind_slc_vert, :], color='k', barb_increments=dict(half=1, full=5, flag=10),clip_on=False)
myFmt = mdates.DateFormatter('%b%d %H:%M')
ax.xaxis.set_major_formatter(myFmt)
ax.tick_params(axis='x', labelrotation=30)
ax.set_title('Potential Temperature')
ax.set_ylabel('Height AGL [m]')
fig.savefig(path+'theta_wind_'+fname+'.png')
fig.clear()
