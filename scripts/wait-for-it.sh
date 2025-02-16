#!/usr/bin/env bash
host="$1"
port="$2"
timeout="${3:-30}"

echo "Waiting for $host:$port for $timeout seconds..."
for i in $(seq $timeout); do
  nc -z "$host" "$port" && echo "$host:$port is available" && exit 0
  sleep 1
done

echo "Error: Timeout waiting for $host:$port"
exit 1
