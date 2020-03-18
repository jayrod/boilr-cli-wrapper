#!/bin/bash
pip3 uninstall {{AppName}}
python3 setup.py develop
pip3 install -e . --force-reinstall
