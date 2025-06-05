# download_TABOO_waveforms
This repository contains a script that downloads waveforms from the TABOO Near Fault Observatory together with a scripts that checks for earthquakes and all necessary files to install a cronjob.

# Cronjob

For rapid response, this will run hourly via crontab:
* Poll event list from seismicportal.eu via obspy ('detect_earthquake.py')
* If an Earthquake occured in the given area, download waveforms ('download_TABOO_waveforms.py')
* and in Step 5 compare those waveforms against the (AltoTiberina) catalogue computed by SeisSol

## Installation of environment

Please generate a virtual environment first with all dependencies installed as given in environment.yml
```
conda env create -f environment.yml
conda env list
conda activate DTGeoWF_Step4_env
```

You might try to run the obspy tests to verify your installation
```
obspy-runtests --report
```

## Adding Data and additional Scripts

To have the cronjob in one directory please download also Step5 
```
git clone https://github.com/NicoSchlw/search_SeisSol_ensemble
cp search_SeisSol_ensemble/search_catalog_for_best_fit_model.py download_TABOO_waveforms/
```

and add the AltoTiberina `AltoTiberinaCatalog` from the Geo-INQUIRE SDL:

https://sdl-dev.hpc.cineca.it/app/experiments/567/summary

Try if everything is working by launching './DTGeoWF_Step4_cronjob.sh' manually. You might want to increase the `timeframe_hours` or lower `minmagnitude` to make sure that it will detect at least one earthquake. 

## Installation of cronjob

Now you can add the cronjob to your crontab use
```
crontab DTGeoWF_Step4_cronjob.txt
```
and check if it has been installed via
```
crontab -l
```
