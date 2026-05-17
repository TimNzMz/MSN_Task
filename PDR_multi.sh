#!/bin/bash

IP1="fdf4:c95d:3885:323d:15a0:44db:b192:65d0"
IP2="fdf4:c95d:3885:323d:91f4:8af5:b01f:1940"
IP3="fdf4:c95d:3885:323d:b870:f63:4533:79f0"

IPS=($IP1 $IP2 $IP3)

RESOURCE="led"

COUNT=500

success=0
min=999999
max=0
sum=0

for i in $(seq 1 $COUNT); do
    for IP in "${IPS[@]}"; do

        start=$(date +%s%3N)

        if timeout 1 coap-client-openssl -N -m get coap://[$IP]/$RESOURCE > /dev/null 2>&1; then
            end=$(date +%s%3N)
            latency=$((end - start))

            echo "coap_seq=$i ip=$IP time=${latency}ms"

            success=$((success + 1))
            sum=$((sum + latency))

            if [ $latency -lt $min ]; then min=$latency; fi
            if [ $latency -gt $max ]; then max=$latency; fi
        else
            echo "coap_seq=$i ip=$IP timeout"
        fi

    done

    sleep 0.2
done

TOTAL=$((COUNT * ${#IPS[@]}))
loss=$((TOTAL - success))
loss_pct=$(echo "scale=1; 100 * $loss / $TOTAL" | bc)

if [ $success -gt 0 ]; then
    avg=$(echo "scale=3; $sum / $success" | bc)
else
    avg=0
fi

echo "--- CoAP multi-node statistics ---"
echo "$TOTAL packets transmitted"
echo "$success packets received"
echo "$loss_pct% packet loss"
echo "round-trip min/avg/max = ${min}/${avg}/${max} ms"
