#!/bin/bash
cat >/opt/aa.log<<EOF
joe 100
jane 200
herman 300
chris 400
shursulei # 550
shursulei1 550
EOF

cat >/opt/bb.log<<EOF
joe 20
jane 10
herman 40
chris 99
shursulei 100
shursulei1 550
EOF
#/^#/d  表示删除某一行
sed '/^#/d' /opt/aa.log |sort >aa.sorted
sed '/^#/d' /opt/bb.log |sort >bb.sorted
#sed -i '/#/d' aa.log
join aa.sorted bb.sorted

rm aa.sorted bb.sorted


