import os
import time
import json
import psycopg2

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'postgres')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')

def process_worker_loop():
    import redis
    r = redis.Redis(host=REDIS_HOST, port=6379, db=0)
    print("Worker engine listening for asynchronous broker events...")

    while True:
        # Blinking pop from redis queue (blocking until item arrives)
        _, message = r.brpop('task_queue')
        task = json.loads(message.decode('utf-8'))
        
        print(f"Processing background async task: {task['title']}")
        time.sleep(5)  # Simulate heavy computing resource consumption (e.g., report generation)
        
        # Update database item state directly from the decoupled background thread
        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            cur = conn.cursor()
            cur.execute("UPDATE tasks SET status = 'Completed' WHERE id = %s;", (task['id'],))
            conn.commit()
            cur.close()
            conn.close()
            print(f"Task ID {task['id']} completely synchronized.")
        except Exception as e:
            print(f"Worker failed database sync write-back: {e}")

if __name__ == '__main__':
    # Add a slight delay on container startup to let DB/Redis warm up
    time.sleep(10)
    process_worker_loop()