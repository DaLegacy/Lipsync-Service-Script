# Lipsync-Service-Script

## Requirements
- Python 3.8
- venv (`sudo apt install python3.8-venv`)
- Docker (`sudo apt install docker.io`)
- SAM CLI
- Lipspeak (`sudo apt install lipespeak1`)
- alsa-utils (`sudo apt install alsa-utils`)

- ubuntu-drivers devices
- ubuntu-drivers autoinstall

## Pre-requsites
- Ensure that Python defaults to version 3.x (tested with 3.10.4)

### Clone the repository

### Create the virtual environment
- `python3 -m venv venv`

### Activate the the virtual environment
#### Windows:
- `venv\scripts\activate`

#### Mac/Linux/WSL:
- `source ./venv/bin/activate`

### Make sure your venv environment is up to date:
```bash
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools
```



### Install prerequsites
```bash
pip install -r requirements.txt --upgrade
```


### Run
