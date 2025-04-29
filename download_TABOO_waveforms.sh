#!/bin/bash

output_folder='TABOO_waveforms'
eq_time='2023,3,9,19,8,6.0'
duration=60
python3 download_TABOO_waveforms.py $eq_time $output_folder $duration
