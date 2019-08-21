#!/bin/sh
set -eu

version="$(git hash-object -t blob "$0")"
cd "$(dirname "$0")"

set +u
. ./ve/bin/activate
set -u

output_dir=out
mkdir -p -- "${output_dir}"

log_file="${output_dir}/run_$(TZ=UTC date +'%Y%m%d_%H%M%SZ')"
full_log_file="${PWD}/${log_file}"
if [ -e "${log_file}" ]; then
    printf >&2 '%s\n' \
        'fatal: log file already exists; wait one second and try again'
    exit 1
fi

exec 4>&1 5>&2 >"${log_file}" 2>&1

printf 'run.sh version %s\n' "${version}"
printf 'log file %s\n' "${full_log_file}"

cat <<'EOF'

============================================================
                        INSTRUCTIONS                        

Once the server spins up, please open http://localhost:3456/
to the scalars dashboard, select all runs, expand all tag
groups, and ensure that automatic data reloading is ENABLED.

The server will run in the background. Killing this process
will NOT kill the server, but it will print the PID so that
you can kill it yourself.
============================================================

EOF

nohup python -u main.py \
    --logdir logdir \
    --port 3456 \
    <&- &
pid=$!

cleanup() {
    printf >&5 '\n'
    if [ "$(ps -q "${pid}" -o ppid=)" != "$$" ]; then
        printf >&5 \
            'Exiting. Server seems to have stopped (was pid %d).\n' "${pid}"
    else
        printf >&5 'Exiting. Also stop server (y/N)? '
        line=
        read -r line || printf >&5 '\n'
        if [ "${line-}" = y ] || [ "${line-}" = Y ]; then
            kill "${pid}"
            printf >&5 'Sent SIGTERM to pid %d.\n' "${pid}"
        else
            printf >&5 'Not killing server (pid %d).\n' "${pid}"
        fi
    fi
    printf >&5 'Log file: %s\n' "${full_log_file}"
}
trap cleanup INT

tail -n +1 -F "${log_file}" >&4 <&-
