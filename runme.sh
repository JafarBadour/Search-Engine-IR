#!/bin/bash
source venv/bin/activate
pip install config
pip install bs4
pip install --user -U nltk
mkdir misc
pip install flask
pip install flask-wtf
pip install requests
pip install -r requirements.txt
#export FLASK_APP=hello.py
