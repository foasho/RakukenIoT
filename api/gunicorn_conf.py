# from multiprocessing import cpu_count

user = "ubuntu"
application = "RakukenIoT/api"
bind = f'unix:/home/{user}/{application}/gunicorn.sock'

workers = 2
worker_class = 'uvicorn.workers.UvicornWorker'

loglevel = 'debug'
accesslog = f'/home/{user}/{application}/access_log'
errorlog =  f'/home/{user}/{application}/error_log'

