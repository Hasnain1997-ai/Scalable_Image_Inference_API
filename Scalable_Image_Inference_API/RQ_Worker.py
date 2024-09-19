import redis
from rq import Worker, Queue, Connection
import multiprocessing
import os

multiprocessing.set_start_method('spawn', force=True)

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_conn = redis.Redis(host='localhost', port=6379)

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker([Queue('default')])
        worker.work()