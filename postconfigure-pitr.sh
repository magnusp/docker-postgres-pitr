#!/bin/bash

if [ $# -eq 0 ]
then
  echo "No arguments supplied"
  exit 1
fi

docker run -t --rm --privileged --volumes-from $1 busybox sh -c "echo archive_command=$'\'/bin/cp %p /var/lib/postgresql/archive/%f\'' >>/var/lib/postgresql/data/postgresql.conf"
docker run -t --rm --privileged --volumes-from $1 busybox sh -c 'echo "wal_level=archive" >> /var/lib/postgresql/data/postgresql.conf'
docker run -t --rm --privileged --volumes-from $1 busybox sh -c 'echo "archive_mode=on" >> /var/lib/postgresql/data/postgresql.conf'
docker run -t --rm --privileged --volumes-from $1 busybox sh -c 'echo "max_wal_senders=5" >> /var/lib/postgresql/data/postgresql.conf'
docker run -t --rm --privileged --volumes-from $1 busybox sh -c 'echo "host replication all 0.0.0.0/0 trust" >> /var/lib/postgresql/data/pg_hba.conf'

docker run -t --rm --privileged --volumes-from $1 busybox sh -c 'chown 999:999 /var/lib/postgresql/archive'

docker restart $1

