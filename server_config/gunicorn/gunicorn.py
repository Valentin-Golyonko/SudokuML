# import multiprocessing

wsgi_app = "dj_config.asgi:application"
worker_class = "uvicorn.workers.UvicornWorker"
command = "./venv/bin/gunicorn"
pythonpath = "."
bind = ":8000"
workers = 4
raw_env = "DJANGO_SETTINGS_MODULE=dj_config.settings"
errorlog = "./logs/gunicorn.log"
max_requests = 100
# reload = True
# loglevel = "debug"
