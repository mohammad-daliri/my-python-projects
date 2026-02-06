#!/bin/bash

echo "=== OCI Data Centre Health Check ==="
echo "Date: $(date)"
echo ""

echo "Uptime:"
uptime
echo ""

echo "Disk Usage:"
df -h | grep -E '^/dev/'
echo ""

echo "Memory Usage:"
free -h
echo ""

echo "Top 5 CPU Processes:"
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head -n 6
echo ""

echo "Last 10 Alerts:"
tail -n 10 alerts_log.txt 2>/dev/null
