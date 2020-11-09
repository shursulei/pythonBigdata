#!/bin/bash
shell_dir=/fss；
list="server_ip_domain.txt"
server_ip=(`cat $shell_dir/$list|grep -v "#"|awk -F ':' '{print $1}'`)
app_dir=(`cat $shell_dir/$list|grep -v "#"|awk -F ':' '{print $2}'`)
domain=(`cat $shell_dir/$list|grep -v "#"|awk -F ':' '{print $3}'`)
for((i=0;i<${#server_ip[@]};++i));
do
if [ "$localhost" == "${server_ip[$i]}"];
sed -i "/^\%let server_id/c\%let server_id=${app_dir[$i]};" /egprog/imporde.sas;
sed -i "/^\%let server_id/c\%let server_id=${domain[$i]};" /egprog/imporde.sas;
fi
done;