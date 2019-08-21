from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil
import sys

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"

import tensorflow as tf


RUNS = 100
TAGS = 500
STEPS = 1000


def main():
  base_logdir = os.path.join(os.path.dirname(__file__), "logdir")
  if tf.io.gfile.exists(base_logdir):
    sys.stderr.write("fatal: remove existing logdir first\n")
    raise SystemExit(1)

  sys.stderr.write("Creating seed logdir...\n")
  seed_logdir = os.path.join(base_logdir, "seed")
  with tf.compat.v2.summary.create_file_writer(seed_logdir).as_default():
    tag_names = [
      "critical_metric_%d/%d" % (i // 100, i % 100) for i in range(TAGS)
    ]
    for step_idx in range(STEPS):
      step = 1000 * step_idx
      for (i, tag) in enumerate(tag_names):
        value = step_idx - i
        tf.compat.v2.summary.scalar(tag, value, step=step)

  sys.stderr.write("Populating runs...\n")
  for run_idx in range(RUNS):
    run = "model_architecture_attempt_number_%d" % run_idx
    logdir = os.path.join(base_logdir, run)
    shutil.copytree(seed_logdir, logdir)

  print("Done.")


if __name__ == "__main__":
  main()
