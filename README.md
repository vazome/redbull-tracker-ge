# Tracker of RedBull prices
[![Run Red Bull Price Grabber](https://github.com/vazome/redbull-tracker-ge/actions/workflows/schedule_run.yml/badge.svg?branch=main)](https://github.com/vazome/redbull-tracker-ge/actions/workflows/schedule_run.yml)

Convenient Red Bull price tracker made for Tbilisi, Georgia.

Utilizes: 
- Python
- Github Actions
- Docker
- AWS RDS for PostgreSQL

Supports multiple platform being added

## How it works
### Config structure
Initially python script gets its config from the [requests_data.json](requests_data.json)

This file containes essential congurations for the script, in the following format 
``` md
- Locations 
- Platforms
  - Plarform Name  
  - Platform HTTP request type
  - Platform API URL
  - Platform Configs
  - Platform Headers
```
