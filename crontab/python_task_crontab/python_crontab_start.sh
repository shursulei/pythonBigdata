#!/usr/bin/env bash
current_path="$PWD"
nohup /usr/bin/python $current_path/TaskTimer.py > $current_path/TaskTimer.log 2>&1 &