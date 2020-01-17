#!/usr/bin/env bash
set -e

install_and_run(){
    pip3 install .
    rallfd
}

wait_for_changes() {
    old=""
    while true; do
        new=$(find $1 -type f -name "*.py" -exec ls --full-time {} \; | shasum | cut -f1 -d" ")
        if [[ "$old" != "$new" ]] ; then
            old=$new
            if pgrep rallfd;then
                pkill rallfd
            fi
            $2 &
        fi
        sleep 1
    done
}


if [[ "$DEBUG" == "yes" ]];then
    wait_for_changes /incubator/rallf install_and_run
else
    install_and_run
fi
