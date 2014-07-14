docker-postgres-pitr-lab
========================

docker run --name pgtest -p 15432:5432 -v /etc/localtime:/etc/localtime:ro -v /home/magnus.persson/pitrlabb/pitr-archive/$(date +%Y%m%d-%H%M%S)/archive:/var/lib/postgresql/archive -d postgres
./postconfigure-pitr.sh pgtest
<create basebackup>
docker run -i -t --rm --link pgtest:db --name foo -v /etc/localtime:/etc/localtime:ro -e PGRUNS=15 magnusp/runner


docker run --name pgrestore -p 15433:5432 -v /etc/localtime:/etc/localtime:ro -v /home/magnus.persson/pitrlabb/pitr-archive/20140714-150853/archive:/var/lib/postgresql/restore-archive:ro -v /home/magnus.persson/pitrlabb/pitr-archive/20140714-150853/basebackup:/var/lib/postgresql/basebackup:ro postgres sh -c "cp -R /var/lib/postgresql/basebackup/* /var/lib/postgresql/data && echo restore_command=\'/bin/cp /var/lib/postgresql/restore-archive/%f %p\' >> /var/lib/postgresql/data/recovery.conf && echo archive_command=\'\' >> /var/lib/postgresql/data/postgresql.conf && echo wal_level=minimal >> /var/lib/postgresql/data/postgresql.conf && echo archive_mode=off >> /var/lib/postgresql/data/postgresql.conf && echo max_wal_senders=0 >> /var/lib/postgresql/data/postgresql.conf && echo recovery_target_time=\'2014-07-14 15:25:04.007633\' >> /var/lib/postgresql/data/recovery.conf && echo log_statement=\'all\' >> /var/lib/postgresql/data/postgresql.conf && echo log_min_duration_statement=-1 >> /var/lib/postgresql/data/postgresql.conf && chown -R postgres:postgres /var/lib/postgresql/data && cat /var/lib/postgresql/data/postgresql.conf /var/lib/postgresql/data/recovery.conf && chmod 0700 /var/lib/postgresql/data && exec gosu postgres postgres -D /var/lib/postgresql/data"
