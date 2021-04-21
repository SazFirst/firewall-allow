#!/bin/bash
#
#   Usage:
#       1. sudo sh firewall-allow.sh
#       2. sudo sh firewall-allow.sh 22,443,8080

# 한국 IP범위 새로 다운로드
FILE='statboardExcelDownload.jsp?searchType=44'
if test -e $FILE; then
    rm $FILE
fi
wget https://xn--3e0bx5euxnjje69i70af08bea817g.xn--3e0b707e/jsp/statboard/statboardExcelDownload.jsp?searchType=44

# 매개변수가 없으면 모든 포트 개방
# 매개변수 지정하면 지정한 포트 개방
if [ $# -eq 0 ]; then
    iptables --append INPUT --match iprange --src-range '127.0.0.0-127.255.255.255' --jump ACCEPT
    iptables --append INPUT --match iprange --src-range '172.30.1.0-172.30.1.255' --jump ACCEPT

    COUNT=0
    for RANGE in `sed -n '2,$p' $FILE | cut -f1,2 | sed 's/\t/-/g'`
    do
            iptables --append INPUT --match iprange --src-range $RANGE --jump ACCEPT
            COUNT=$(($COUNT+1))
    echo  "[ $COUNT ] : $RANGE"
    done
else
    iptables -A INPUT --protocol tcp --match multiport --dports $1 --match iprange --src-range '127.0.0.0-127.255.255.255' --jump ACCEPT
    iptables -A INPUT --protocol tcp --match multiport --dports $1 --match iprange --src-range '172.30.1.0-172.30.1.255' --jump ACCEPT

    COUNT=0
    for RANGE in `sed -n '2,$p' $FILE | cut -f1,2 | sed 's/\t/-/g'`
    do
        iptables -A INPUT --protocol tcp --match multiport --dports $1 --match iprange --src-range $RANGE --jump ACCEPT
        COUNT=$(($COUNT+1))
    echo  "[ $COUNT ] : $RANGE"
    done
fi

iptables -P INPUT DROP
