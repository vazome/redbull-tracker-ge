# Red Bull Price Tracker 
![Badge](https://codebuild.eu-central-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoieW13QkdUc1NYQ0gyL0QvMkJNcjR6eHlVTHAxeUZkblA3WUJjamNpZTBHeWlWVVJMYWx0cTVyZTMwRmY0REZ2NExTSEZTZUJtQXJYZWlQWm4xMFFWOHlRPSIsIml2UGFyYW1ldGVyU3BlYyI6Ikp5dmo2MWp0VFlzZWJET2ciLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main)
[![Build Tracker image with Github Actions](https://github.com/vazome/redbull-tracker-ge/actions/workflows/build_tracker_github.yml/badge.svg)](https://github.com/vazome/redbull-tracker-ge/actions/workflows/build_tracker_github.yml)
[![Run Red Bull Tracker](https://github.com/vazome/redbull-tracker-ge/actions/workflows/run_tracker_github.yml/badge.svg)](https://github.com/vazome/redbull-tracker-ge/actions/workflows/run_tracker_github.yml)
![Docker Image Version (tag)](https://img.shields.io/docker/v/vazome/redbull-tracker-ge/tracker-latest?arch=amd64&logo=docker&label=redbull-tracker-ge)

Convenient Red Bull price tracker made for Tbilisi, Georgia. This project covers both data collection and representation, with the latter delegated to Telegram bot and Grafana.

As of now it supports two most major delivery providers: [Wolt](https://wolt.com/en/geo) and [Glovo](https://glovoapp.com/ge/en/tbilisi/).

Project utilizes: 
- Scripting \[Python, SQL\]
- Containerization \[Github Actions, Docker, AWS ECS (EC2 based)\]
- Storage \[AWS RDS for PostgreSQL, json\]
- User Interfaces \[Grafana, Telegram Bot API\]

Plans:
- [x] Bot: Deploy bot in AWS
- [x] Parse: Deploy parser in Github Actions with auto-commits for new json export files
- [x] Parser: enable parsing for most popular Tbilisi districts with products EN/GE variations.
- [x] DB: Enable product_volume column and autofill on Postgres side by parsing names
- [ ] DB/Parser: Add `2 Nabiji` grocery store
- [ ] Bot: Add product/store links to the bot output
- [ ] Bot: Allow users to define daily schedule time
- [ ] Bot: Dynamic checking of [`requests_data.json`] file
- [ ] Grafana: Create average and lowest fluctuation charts

## How to use



## Telegram bot
I've made a bot for immediate or daily reportings: [@RedBullTrackerBot](https://t.me/RedBullTrackerBot). Here is how it works:

https://github.com/vazome/redbull-tracker-ge/assets/46573198/3706c2ad-9227-4e72-a1a7-3eecae19d35a

## Grafana Analytics View
I wanted something to glance on and see the numbers changing, so I built a Grafana dashboard for that:

[<img width="1450" alt="image" src="https://github.com/vazome/redbull-tracker-ge/assets/46573198/7e62d523-29cd-4fb1-8d9e-308533685ad8">](https://vazome.grafana.net/public-dashboards/61b08f3b99974e1bab84a96e5c039a77)

Available here: [Red Bull Dynamics](https://vazome.grafana.net/public-dashboards/61b08f3b99974e1bab84a96e5c039a77)

## How it works
### Building a request
The script begins by loading its configuration from a JSON file named [`requests_data.json`](requests_data.json). This file contains essential configurations including the physical locations and the platform specific information.

For each platform specified in the configuration, the script makes HTTP requests to the platform's API. The type of request (`GET` or `POST`) and the necessary headers are defined per platform in the configuration file.


#### Dynamic Location Handling
The script utilizes the `locations_async` array from the configuration to dynamically adjust the request parameters for geolocation, enabling localized price tracking across different areas in Tbilisi.

[@RedBullTrackerBot](https://t.me/RedBullTrackerBot) also looks into requests_data.json, this is where it gets current list of all supported districts.

### Data Extraction and transformation
Upon receiving the response from each platform, it parses the returned data for Red Bulls. This typically includes the product name, price, and any other pertinent details provided by the platform. Data from each platform is parsed in order to pull out only the necessities.
<img width="631" alt="image" src="https://github.com/vazome/redbull-tracker-ge/assets/46573198/88a1e594-6c4c-4a24-bcff-f32fc1ad15a0">

### Storage
After data is parsed it is aggregated in both repo folder [./export](./export/) where each file is timestamped in UTC+00:00 and sent for store in bulk to AWS RDS PostgreSQL database.
Ready to be picked up at UI stage.
<img width="1171" alt="image" src="https://github.com/vazome/redbull-tracker-ge/assets/46573198/f3c2e9d3-d5f0-4d83-b5e9-d3492c509b78">

### Automation via GitHub Actions
The entire process is automated through GitHub Actions, which configurations are stored in [.github/workflows](.github/workflows) (default location).

The responsible action for scheduled runs is [![Run Red Bull Tracker](https://github.com/vazome/redbull-tracker-ge/actions/workflows/redbulltracker_run.yml/badge.svg)](https://github.com/vazome/redbull-tracker-ge/actions/workflows/redbulltracker_run.yml).
