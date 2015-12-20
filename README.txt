Paco Li's scripts to control my docker containers as a cluster env
[root@docker scripts]# tree /var/lib/docker/scripts
/var/lib/docker/scripts
├── create_containers.sh          # sample commands to create containers
├── docker_start.py               # to startup pre-created containers configured in 'my_containers.py'
├── docker_stop.py                # to stop running containers
├── my_containers.py              #config file to set container information for docker_start.py usage
├── my_fork.py                    #fork helper class for docker_start.py and docker_stop.py usage
├── assign_interface.sh           #to assign physical eth interface to a container
├── docker_pid.sh                 #to find a docker container pid via docker inspect
└── start_docker.sh               #'docker start' a container, assign interface to it, start up sshd inside
