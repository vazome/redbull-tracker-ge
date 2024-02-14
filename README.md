# RedBull price tracker 
[![Run Red Bull Price Grabber](https://github.com/vazome/redbull-tracker-ge/actions/workflows/schedule_run.yml/badge.svg?branch=main)](https://github.com/vazome/redbull-tracker-ge/actions/workflows/schedule_run.yml)

Convenient Red Bull price tracker made for Tbilisi, Georgia.

As of now it supports two most major delivery providers: Wolt and Glovo.

Utilizes: 
- Python
- Github Actions
- Docker
- AWS RDS for PostgreSQL
- Grafana

## How to use
## Telegram bot
I've made a bot for a simple now or daily reporting: [Red Bull Tracker Bot](https://t.me/RedBullTrackerBot)

<img src="https://github.com/vazome/redbull-tracker-ge/assets/46573198/8c59955b-85cf-4f14-984b-f6139c0f24a3" loop=infinite>

## Grafana Analytics View
I wanted something to glance on and see the numbers changing, so I built a Grafana dashboard for that:
<img width="1208" alt="image" src="https://github.com/vazome/redbull-tracker-ge/assets/46573198/49440610-9a37-4e54-8c73-69074e14e1ab">

Available here: [Red Bull Dynamics](https://vazome.grafana.net/public-dashboards/61b08f3b99974e1bab84a96e5c039a77)


## How it works
### Building a request
The script begins by loading its configuration from a JSON file named [`requests_data.json`](requests_data.json). This file contains essential configurations including the physical locations and the platform specific information.

For each platform specified in the configuration, the script makes HTTP requests to the platform's API. The type of request (`GET` or `POST`) and the necessary headers are defined per platform in the configuration file.

#### Dynamic Location Handling
The script utilizes the `locations_async` array from the configuration to dynamically adjust the request parameters for geolocation, enabling localized price tracking across different areas in Tbilisi.

### Data Extraction and transformation
Upon receiving the response from each platform, it parses the returned data for Red Bulls. This typically includes the product name, price, and any other pertinent details provided by the platform. Data from each platform is parsed in order to pull out only the nessesities.
<img width="631" alt="image" src="https://github.com/vazome/redbull-tracker-ge/assets/46573198/88a1e594-6c4c-4a24-bcff-f32fc1ad15a0">

### Storage
After data is parsed it is aggregated in both repo folder [./export](./export/) where each file is timestamped in UTC+00:00 and sent for store in bulk to AWS RDS PostgreSQL database.
For DB it ensures that new data is correctly inserted and provides an easy-to-analys dataset.
<img width="1171" alt="image" src="https://github.com/vazome/redbull-tracker-ge/assets/46573198/f3c2e9d3-d5f0-4d83-b5e9-d3492c509b78">

### Automation via GitHub Actions
The entire process is automated through GitHub Actions, which configurations are stored in [.github/workflows](.github/workflows) (default location).

The responsible action for scheduled runs is [![Run Red Bull Tracker](https://github.com/vazome/redbull-tracker-ge/actions/workflows/schedule_run.yml/badge.svg)](https://github.com/vazome/redbull-tracker-ge/actions/workflows/schedule_run.yml).
