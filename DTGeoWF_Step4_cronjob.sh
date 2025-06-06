#!/bin/bash

# to run this script you need to install the conda environment first
# please have a look at the Readme.md how to do so
# conda env create -f requirements.yml
#
# make sure you have a mail transfer agent installed and configured on your system
# sudo apt-get install mailutils  # For Debian/Ubuntu systems

# if mail is not configured, output will go to DTGeoWF_Step4.log/.err
mailw=0

# activate python environment (see Readme.md)
source /home/christadler/anaconda3/etc/profile.d/conda.sh
conda activate DTGeoWF_Step4_env

# detect if an EQ happened
# exit_code   0: no EQ
# exit_code   1:    EQ
# exit_code   n: n  EQs
# exit_code 255: error

# This script is directly called by crontab so it needs the full path
cronPath=/home/christadler/githubclones/download_TABOO_waveforms
logfile=$cronPath/DTGeoWF_Step4_detect_event.log
errfile=$cronPath/DTGeoWF_Step4_detect_event.err
python3 $cronPath/detect_event.py >> $logfile 2>> $errfile

exit_code=$?
utcdate=$(date -u +"%Y-%m-%dT%H:%M:%S")

if [ "$exit_code" -eq 255 ]; then
	recipient=iris.christadler@lmu.de
	subject="DTGeoWF_Step4_cronjob.sh: detect_event.py aborted with an error"  
	body="$utcdate: The DTGeoWF_Step4 detected problems. See DTGeoWF_Step4_detect_event.err for more information"
	if [ "$mailw" -eq 1 ]; then
		# send email 
		echo "sendmail"
		echo "$body" | mail -s "$subject" "$recipient"
	fi
	# and write to logfile
	echo "$body" >> $errfile
	echo "$body" >> $logfile

elif [ "$exit_code" -eq 0 ]; then
	#if $exit_code -eq 0: No EQ happened, nothing needs to be done
	body="$utcdate: DTGeoWF_Step4 detect_event.py: No EQ detected"
	echo "$body" >> $logfile

elif [ "$exit_code" -gt 0 ]; then
	recipient=iris.christadler@lmu.de
	subject="DTGeoWF_Step4_cronjob.sh: AltoTiberina Earthquake happened!"
	body="$utcdate: The DTGeoWF_Step4 detected $exit_code earthquake(s). See DTGeoWF_Step4_detect_event.log for more information"

	if [ "$mailw" -eq 1 ]; then
		# send email 
		echo "sendmail"
		echo "$body" | mail -s "$subject" "$recipient"
	fi
	# and write to logfile
	echo "$body" >> $logfile
fi


