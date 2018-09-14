#!/bin/sh
# Date  : 2018-09-14 14:56:09
# Author: b4zinga
# Email : b4zinga@outlook.com
# Func  : 批量登陆Linux主机并执行命令

username="root"
password="centos"
port="22"
timeout=3

cmd="ip a"  # the command to be executed
succ_flag="eth0"  # Characteristics of the return value after exec the cmd

iplist="ip_list.txt"  # the ip list
succ_ip="success_ip_list.txt"  # ip, successfuly exec
failed_ip="failed_ip_list.txt" # ip, failed exec

c=192.168.27.  # ip segment

#---------------------------------------------------


# make ip address by ip segment
mkip(){
    for((i=1;i<256;i++))
    do
        echo "$c$i" >> $iplist
    done
    echo "ip finished ! see $iplist"
    echo ""
}


# login and exec cmd
login(){
    echo "-------------------------------------------------------- "
    echo "username: $username  password: $password  port: $port  timeout=$timeout" 
    echo "command: $cmd"
    echo "--------------------------------------------------------"
    echo ""

    for host in `cat $iplist`;
    do
        result=`sshpass -p "$password" ssh -p $port -o StrictHostKeyChecking=no -o ConnectTimeout=$timeout $username@$host $cmd`

    if [[ $result =~ $succ_flag ]] 
    then 
        echo $host >> $succ_ip
    else
        echo $host >> $failed_ip
    fi

    done
}



help(){
    echo "----------------------------------------------------------------"
    echo "bash remote.sh"
    echo ""
    echo "bash remote.sh mkip     make IP list"
    echo "bash remote.sh login    login to exec command "
    echo "bash remote.sh all      make IP list and login to exec command"
    echo "-----------------------------------------------------------------"
    exit 1

}


#-----------------------------start-------------------------------------------
[ $# -gt 0 ] || help $*
echo $1

case $1 in 
    mkip)
        mkip
        exit 0
        ;;
    login)
        login
        exit 0
        ;;
    all)
        mkip
        login
        exit 0
        ;;
    *)
        help $*
        exit 0
       ;;
esac
