#!/bin/bash

#Paco Li: 2015-11-3
#this script is to create docker containers for my test lab


# this is to create the ocg_dev from centos5_ocg image
docker create -i -t -h dev5 --name=dev5 -v /media/ocg_data:/shared -v /src:/ocg -v /proc:/writable-proc --cap-add ALL --net=none centos5_dev_swig /sbin/init
docker create -i -t -h dev6 --name=dev6 -v /media/ocg_data:/shared -v /src:/ocg -v /proc:/writable-proc --cap-add ALL --net=none dev6.go /sbin/init
#docker create -i -t -h dev7 --name=dev7 -v /media/ocg_data:/shared -v /src:/ocg daocloud.io/library/centos:centos7.1.1503
docker create -i -t -h dev7 --name=dev7 -v /media/ocg_data:/shared -v /src:/ocg -v /proc:/writable-proc -v /sys/fs/cgroup:/sys/fs/cgroup:ro --cap-add ALL --net=none –-privileged dev7_java /sbin/init

# this is to create the frontends of ps-ocg from centos6 image
docker create -i -t -h ocg_fe1 --name=ocg_fe1 -v /media/ocg_data:/shared -v /media/ocg_data/ocg_fe1:/ocg -v /proc:/writable-proc --cap-add ALL --net=none ocg_fe1 /sbin/init
docker create -i -t -h ocg_fe2 --name=ocg_fe2 -v /media/ocg_data:/shared -v /media/ocg_data/ocg_fe2:/ocg -v /proc:/writable-proc --cap-add ALL --net=none ocg_fe2 /sbin/init

# this is to create the backend of ocg from centos6 image
docker create -i -t -h ocg_be1 --name=ocg_be1 -v /media/ocg_data:/shared -v /media/ocg_data/ocg_be1:/ocg -v /proc:/writable-proc --cap-add ALL --net=none ocg_be1 /sbin/init
docker create -i -t -h ocg_be2 --name=ocg_be2 -v /media/ocg_data:/shared -v /media/ocg_data/ocg_be2:/ocg -v /proc:/writable-proc --cap-add ALL --net=none ocg_be2 /sbin/init
# this is to create a container for radius server from rhel6 image
#docker create -i -t -h ctm_rad --name=ctm_rad -v /media/ocg_data:/shared -v /media/ocg_data/radius:/radius --cap-add=NET_ADMIN rhel6.7-base /sbin/init


#docker run --name mysql -p 3306:3306 -v /var/lib/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d daocloud.io/library/mysql:5.7.9
docker create -h mysql --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -d daocloud.io/library/mysql:5.7.9
docker create -h mysql2 --name mysql2 -p 3307:3306 -e MYSQL_ROOT_PASSWORD=123456 -d daocloud.io/library/mysql:5.7.9
docker run -h xxx --name xxx -i -t --link=mysql:db --link=mysql2:db2 dev6 /bin/bash
docker run --name redis -p 6377:6377 -e REDIS_PASS=ericsson -e REDIS_PORT=6377 -d daocloud.io/daocloud/dao-redis:master-init
