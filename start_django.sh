#!/bin/bash

touch ./logs/gunicorn.log
sleep 0.1
gunicorn -c ./server_config/gunicorn/gunicorn.py
