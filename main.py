from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import threading
import time

from pympler import tracker


def main():
  sys.stderr.write("PID: %d\n" % (os.getpid(),))

  ready_lock = threading.Semaphore(0)

  threading.Thread(
    target=track_memory_forever,
    args=(ready_lock,),
    name="MemoryTracker",
    daemon=True,
  ).start()
  ready_lock.acquire()

  from tensorboard import main as tensorboard_main

  tensorboard_main.run_main()


def track_memory_forever(ready_lock):
  sys.stderr.write("Initializing tracker...\n")
  tr = tracker.SummaryTracker()
  ready_lock.release()

  start_time = time.time()
  sleep_time = 1.0
  while True:
    tr.print_diff()
    elapsed = time.time() - start_time
    sys.stderr.write("Elapsed time: %f seconds\n" % elapsed)
    time.sleep(sleep_time)
    if sleep_time < 60:
      sleep_time += 1


if __name__ == "__main__":
  main()
