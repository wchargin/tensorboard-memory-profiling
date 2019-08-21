# tensorboard-memory-profiling

Small test bed for investigating memory issues in TensorBoard, like:
<https://github.com/tensorflow/tensorboard/issues/766>

This is not an official Google product.

Usage instructions:

 1. Run `./set_up_env.sh` once, to create a virtualenv.
 2. Run `(. ./ve/bin/activate && python generate_logdir.py)` to generate
    a log directory.
 3. Run `./run.sh` and follow the log, which will also be saved under
    the `out/` directory.
 4. At your discretion, hit Ctrl-C on the `./run.sh` process to kill it,
    and respond “`y`” at the prompt to also kill the server.

Works on GNU/Linux; may require some minor changes for BSDs.
