#!/bin/sh
set -e
cd "$(dirname "$0")"
if [ -e ./ve ]; then
    printf >&2 'fatal: remove existing virtualenv "%s" first\n' ./ve
    exit 1
fi
virtualenv -p python3.6 ./ve
. ./ve/bin/activate
pip install tf-nightly-2.0-preview==2.0.0.dev20190820
pip install pympler==0.7
