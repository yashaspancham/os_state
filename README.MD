# OS_State
### A python script for recording OS state.

*AIM*-> The script will record cpu, memory, disk and os details.

*Tech*-> Python3, crontab and google sheet.

## Features
The script runs every 5 minutes (via Crontab) and captures:
- CPU: Core count and usage percentage.
- Memory: Used/Total/Free GB and usage percentage.
- Disk: Used/Total/Free GB and usage percentage.
- OS Details: Distro name, Kernel version, and Architecture.
- Automated Sync: Automatically creates a new worksheet for each unique Machine ID.
