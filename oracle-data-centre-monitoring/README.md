# OCI Data Centre Monitoring (Simulation)

## Overview

This project simulates rack-level monitoring within an Oracle Cloud Infrastructure (OCI) data centre environment.  

It was built to better understand infrastructure monitoring, alert management, and operational resilience workflows typically used in cloud data centre operations.

---

## Environment Simulation

- Environment: OCI-UK-LONDON-DC01
- Rack ID: RACK-07
- Monitoring Interval: 5 seconds
- Summary Interval: 60 seconds

---

## Features

### Real-Time Monitoring
- CPU utilisation tracking
- Memory utilisation tracking
- Disk utilisation tracking

### Threshold-Based Alerting
- Configurable CPU, Memory, and Disk thresholds
- Automatic incident detection
- Capacity planning notification simulation

### Alert Cooldown Mechanism
- Prevents alert fatigue
- Suppresses repeated alerts within cooldown window

### Health State Classification
Each monitoring cycle is classified as:
- OK
- WARNING
- CRITICAL

### Operational Summary Reporting
- 60-second infrastructure summary
- Logged for operational visibility

### Incident Logging
- `system_log.txt` → All monitoring data
- `alerts_log.txt` → Incident + summary events

### Linux-Based Health Check Script
A Bash operational script (`health_check.sh`) simulates data centre engineer workflows by displaying:
- Uptime
- Disk usage
- Memory usage
- Top CPU processes
- Recent alert history

---

## Project Structure

oci-data-centre-monitoring/
│
├── oci_monitor.py
├── health_check.sh
├── system_log.txt
├── alerts_log.txt
└── README.md


---

## Purpose

This project demonstrates:

- Infrastructure monitoring logic
- Incident handling design
- Alert suppression techniques
- Operational reporting
- Basic Linux system diagnostics familiarity

The goal was to simulate production-style monitoring behaviour aligned with cloud data centre operations.

---

## Future Improvements

- Multi-rack simulation
- Email or webhook alert notifications
- Deployment on live cloud VM
- Dashboard-based visualisation

---

## Author

Built as part of preparation for Data Centre Operations roles in cloud infrastructure environments.