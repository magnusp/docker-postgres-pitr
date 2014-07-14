#!/usr/bin/env python

import datetime as dt
import sys
import os
from pytz import timezone
from time import sleep
import argparse
import psycopg2
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

def insert_job(host, port):
  con = psycopg2.connect(host=host, port=port, user='postgres')
  cur = con.cursor()
  cur.execute('INSERT INTO entry VALUES (DEFAULT, NOW(), %s) RETURNING (id, db_ts, script_ts, txid, txid_current_snapshot); ', [dt.datetime.now()])
  print repr(cur.fetchone())
  con.commit()
  cur.close()
  con.close()

parser = argparse.ArgumentParser()
parser.add_argument('--host')
parser.add_argument('--port')
parser.add_argument('--runs')
args = parser.parse_args()
pghost=os.getenv('DB_PORT_5432_TCP_ADDR', args.host)
pgport=os.getenv('DB_PORT_5432_TCP_PORT', args.port)
pgruns=os.getenv('PGRUNS', args.runs)
if not pghost or not pgport or not pgruns: raise Exception("Invalid arguments/no environment")
 
con = psycopg2.connect(host=pghost, port=pgport, user='postgres')
cur = con.cursor()
cur.execute('''
DROP TABLE IF EXISTS entry;
CREATE TABLE entry
(
  id serial NOT NULL,
  db_ts timestamp without time zone NOT NULL DEFAULT now(),
  script_ts timestamp without time zone NOT NULL,
  txid bigint NOT NULL DEFAULT txid_current(),
  txid_current_snapshot txid_snapshot NOT NULL DEFAULT txid_current_snapshot(),
  CONSTRAINT entry_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
''')
con.commit();
cur.close()
con.close()


tz = timezone("Europe/Stockholm")
sched = BackgroundScheduler()
now = dt.datetime.now()
print now
then = now - dt.timedelta(seconds=now.second, microseconds=now.microsecond)
then += dt.timedelta(minutes=1, seconds=1)
for i in range(int(pgruns)):
    trigger = DateTrigger(timezone=tz, run_date=then)
    sched.add_job(insert_job, trigger, [pghost, pgport])
    then += dt.timedelta(microseconds=500000)
sched.start()        # start the scheduler
while len(sched.get_jobs()) > 0: sleep(1)


con = psycopg2.connect(host=pghost, port=pgport, user='postgres')
cur = con.cursor()
cur.execute('SELECT pg_switch_xlog()')
con.commit();
cur.close()
con.close()

