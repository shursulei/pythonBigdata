#!/bin/sh
mod=$1
if [ -z $1 ];then
echo "input add or del for paramter1!";
exit 1
fi
str=$2
if [ -z $2 ];then
echo "input key string for paramter1!";
exit 1
fi
file=$3
if [ -z $3 ];then
echo "input the total path filename for parmeter3!";
exit 1
fi

if [ "$mod" =="add" ];then
line=`cat $file|grep $str`
echo "$line"
line_note=`echo "#${line}"`
line=${line//\*/\\*}
line_note=${line_note//\*/\\*}
if_note=`echo "$line"|grep '#' | wc -l`;
if [ $if_note -eq 0 ];then
sed -i "s@line@line_note@g" $file
cat $file |grep $str
else
echo "no need to add '#' in front of the line"
fi
elif [ "$mod" == "del" ];then
line=`cat $file|grep $str`
echo "$line"
line_note=`echo "#${line}"|sed 's/#//g'`
line=${line//\*/\\*}
line_note=${line_note//\*/\\*}
if_note=`echo "$line"|grep '#' | wc -l`;
if [ $if_note -gt 0 ];then
sed -i "s@line@line_note@g" $file
cat $file |grep $str
else
echo "no need to delete '#' from line"
fi
else
echo "input add or del for parameter1 to add or del '#' to/from the line"
exit 1
fi
