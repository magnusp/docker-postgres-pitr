FROM centos:centos7

RUN yum install http://mirror.nsc.liu.se/fedora-epel/beta/7/x86_64/epel-release-7-0.2.noarch.rpm wget -y
RUN yum install python-pip -y
RUN yum install http://yum.postgresql.org/9.3/redhat/rhel-7-x86_64/pgdg-centos93-9.3-1.noarch.rpm -y && yum install postgresql93 postgresql93-devel -y
RUN pip install APScheduler
RUN yum install gcc make python-devel -y
RUN PATH=/usr/pgsql-9.3/bin:"$PATH" pip install psycopg2

ADD runnerscript.py /root/runnerscript.py
ENTRYPOINT ["/root/runnerscript.py"]
