#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 13:16:13 2025

@author: mathilde
"""
import os
import argparse
from obspy import UTCDateTime
from obspy.clients.fdsn import Client

parser = argparse.ArgumentParser(
    description="Download seismic waveforms for a given event from the NFO TABOO. The script downloads channels BH, HH, and EH."
)

parser.add_argument(
    "eq_time",
    help="Date and time of the earthquake. String with the following structure: YYYY,MM,DD,HH,MM,SS.S. E.g: '2023,3,9,19,8,6.0'",
)

parser.add_argument(
    "output_folder",
    help="name of the folder in which the waveforms will be stored",
)

parser.add_argument(
    "duration",
    type=int,
    help="duration of the time serie after eq_time (in second)",
)

args = parser.parse_args()


def get_TABOO_waveforms(eq_time,obsdir,dt=100):
    """Download waveforms from TABOO Near Fault Observatory"""
    # Define the start and end time
    eq_time = [int(x) if x.isdigit() else float(x) for x in eq_time.split(',')]
    eq_time = UTCDateTime(eq_time[0], eq_time[1], eq_time[2], eq_time[3], eq_time[4], eq_time[5])
        
    starttime = eq_time - 10 # download also the 10 seconds before the eq.
    endtime = eq_time + dt
    duration = 10 + dt

    # Create output directory
    os.makedirs(obsdir, exist_ok=True)
    
    print("Downloading TABOO seismic data from INGV webservices...")  
    print(f"Start time: {starttime}")   
    print(f"End time: {endtime}") 
    
    # Define FDSN client (INGV EIDA)
    client = Client("https://webservices.ingv.it")

    # Define parameters
    network = "_NFOTABOO"  # Make sure this is the correct network code

    # Get station metadata to retrieve all station codes
    inventory = client.get_stations(network=network, starttime=starttime, endtime=endtime, level="response")

    # Save station metadata
    filename = f"{obsdir}/{network}_metadata.xml"
    inventory.write(filename, format="STATIONXML")
    
    # Iterate over stations and download waveforms
    for net in inventory:
        for station in net:
            station_code = station.code
            try:
                # Request waveform data for the station
                st = client.get_waveforms(network=net.code, station=station.code, location="*", channel="BH?,HH?,EH?", 
                                          starttime=starttime, endtime=endtime,attach_response=True)     
                
                # Remove instrument response
                st = st.remove_response()       
                
                # Save data in MiniSEED format
                filename = f"{obsdir}/{net.code}_{station.code}_{starttime.date}_{starttime.hour}_{duration}sec_RespRemouved.mseed"
                st.write(filename, format="MSEED", encoding=5) 
                print(f"Downloaded: {filename}")
                
            except Exception as e:
                print(f"Could not download data for {station_code}: {e}")    
         
get_TABOO_waveforms(args.eq_time,args.output_folder,args.duration)
