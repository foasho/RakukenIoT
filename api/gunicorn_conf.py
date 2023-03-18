from multiprocessing import cpu_count

user = "ubuntu"
application = "RakukenIoT/api"
# bind = f'unix:/home/{user}/{application}/gunicorn.sock'
bind = "127.0.0.1:8000"

# workers = 2
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

loglevel = 'debug'
accesslog = f'/home/{user}/{application}/access_log'
errorlog =  f'/home/{user}/{application}/error_log'

