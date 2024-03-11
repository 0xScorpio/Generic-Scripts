#!/bin/bash

IP_ADDRESS="TARGET-IP"
PORT="TARGET-PORT"

# Loop to send numbers from 1 to 200 and receive outputs
for ((i=0; i<=200; i++)); do
    # Use timeout to limit the time nc waits for a response
    result=$(timeout 0.5s nc -w 5 "$IP_ADDRESS" "$PORT" <<< "$i")
    echo "$result"
done

