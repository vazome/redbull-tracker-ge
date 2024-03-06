# Red Bull Price Tracker 
![AWS CodePipeline Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fdnxqhcr6z1.execute-api.eu-central-1.amazonaws.com%2FBadge%2FGetPipelineStatus&query=%24.status&logo=data:image/svg%2bxml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4gPHN2ZyB3aWR0aD0iODBweCIgaGVpZ2h0PSI4MHB4IiB2aWV3Qm94PSIwIDAgODAgODAiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+IDwhLS0gR2VuZXJhdG9yOiBTa2V0Y2ggNjQgKDkzNTM3KSAtIGh0dHBzOi8vc2tldGNoLmNvbSAtLT4gPHRpdGxlPkljb24tQXJjaGl0ZWN0dXJlLzY0L0FyY2hfQVdTLUNvZGVQaXBlbGluZV82NDwvdGl0bGU+IDxkZXNjPkNyZWF0ZWQgd2l0aCBTa2V0Y2guPC9kZXNjPiA8ZGVmcz4gPGxpbmVhckdyYWRpZW50IHgxPSIwJSIgeTE9IjEwMCUiIHgyPSIxMDAlIiB5Mj0iMCUiIGlkPSJsaW5lYXJHcmFkaWVudC0xIj4gPHN0b3Agc3RvcC1jb2xvcj0iIzJFMjdBRCIgb2Zmc2V0PSIwJSI+PC9zdG9wPiA8c3RvcCBzdG9wLWNvbG9yPSIjNTI3RkZGIiBvZmZzZXQ9IjEwMCUiPjwvc3RvcD4gPC9saW5lYXJHcmFkaWVudD4gPC9kZWZzPiA8ZyBpZD0iSWNvbi1BcmNoaXRlY3R1cmUvNjQvQXJjaF9BV1MtQ29kZVBpcGVsaW5lXzY0IiBzdHJva2U9Im5vbmUiIHN0cm9rZS13aWR0aD0iMSIgZmlsbD0ibm9uZSIgZmlsbC1ydWxlPSJldmVub2RkIj4gPGcgaWQ9Ikljb24tQXJjaGl0ZWN0dXJlLUJHLzY0L0RldmVsb3Blci1Ub29scyIgZmlsbD0idXJsKCNsaW5lYXJHcmFkaWVudC0xKSI+IDxyZWN0IGlkPSJSZWN0YW5nbGUiIHg9IjAiIHk9IjAiIHdpZHRoPSI4MCIgaGVpZ2h0PSI4MCI+PC9yZWN0PiA8L2c+IDxwYXRoIGQ9Ik0zMCwzMSBMMzUsMzEgTDM1LDI5IEwzMCwyOSBMMzAsMzEgWiBNMzYuNjY3LDYxLjE2NiBMMzQuODE3LDYwLjQwNyBMNDIuNDA5LDQxLjg4NSBMNDQuMjU5LDQyLjY0NCBMMzYuNjY3LDYxLjE2NiBaIE00NS41NzEsNTUuNzggTDUxLjA2OCw1MC45NTggTDQ1LjU3NSw0Ni4xOTcgTDQ2Ljg4Niw0NC42ODUgTDUzLjI0NSw1MC4xOTggQzUzLjQ2Myw1MC4zODcgNTMuNTg5LDUwLjY2MiA1My41OTAwMDYsNTAuOTUxIEM1My41OTEsNTEuMjQgNTMuNDY3LDUxLjUxNSA1My4yNDksNTEuNzA2IEw0Ni44OSw1Ny4yODQgTDQ1LjU3MSw1NS43OCBaIE0yNS41MDg5NzYsNTEuMDQ4IEMyNS41MDcsNTAuNzU5IDI1LjYzLDUwLjQ4NCAyNS44NDcsNTAuMjkzIEwzMi4xODQsNDQuNjkxIEwzMy41MDgsNDYuMTkgTDI4LjAyOSw1MS4wMzMgTDMzLjQ3OCw1NS43MyBMMzIuMTcxLDU3LjI0NSBMMjUuODU1LDUxLjc5OSBDMjUuNjM3LDUxLjYxMSAyNS41MTEsNTEuMzM3IDI1LjUwODk3Niw1MS4wNDggTDI1LjUwODk3Niw1MS4wNDggWiBNNjIuNTM1LDM1IEwxOC40NjUsMzUgQzE2LjU1NSwzNSAxNSwzMy40NDYgMTUsMzEuNTM2IEwxNSwzMSBMMjcsMzEgTDI3LDI5IEwxNSwyOSBMMTUsMTguNDY0IEMxNSwxNi41NTQgMTYuNTU1LDE1IDE4LjQ2NSwxNSBMNjIuNTM1LDE1IEM2NC40NDUsMTUgNjYsMTYuNTU0IDY2LDE4LjQ2NCBMNjYsMjkgTDM4LDI5IEwzOCwzMSBMNjYsMzEgTDY2LDMxLjUzNiBDNjYsMzMuNDQ2IDY0LjQ0NSwzNSA2Mi41MzUsMzUgTDYyLjUzNSwzNSBaIE0yMiw2NiBMNTgsNjYgTDU4LDM3IEwyMiwzNyBMMjIsNjYgWiBNNjIuNTM1LDEzIEwxOC40NjUsMTMgQzE1LjQ1MSwxMyAxMywxNS40NTEgMTMsMTguNDY0IEwxMywzMS41MzYgQzEzLDM0LjU0OSAxNS40NTEsMzcgMTguNDY1LDM3IEwyMCwzNyBMMjAsNjcgQzIwLDY3LjU1MiAyMC40NDcsNjggMjEsNjggTDU5LDY4IEM1OS41NTMsNjggNjAsNjcuNTUyIDYwLDY3IEw2MCwzNyBMNjIuNTM1LDM3IEM2NS41NDksMzcgNjgsMzQuNTQ5IDY4LDMxLjUzNiBMNjgsMTguNDY0IEM2OCwxNS40NTEgNjUuNTQ5LDEzIDYyLjUzNSwxMyBMNjIuNTM1LDEzIFoiIGlkPSJBV1MtQ29kZVBpcGVsaW5lX0ljb25fNjRfU3F1aWQiIGZpbGw9IiNGRkZGRkYiPjwvcGF0aD4gPC9nPiA8L3N2Zz4=&label=Build%20Bot%20image%20with%20AWS%20CI%2FCD&color=%2332CB55
)
[![Build Tracker image with Github Actions](https://github.com/vazome/redbull-tracker-ge/actions/workflows/build_tracker_github.yml/badge.svg)](https://github.com/vazome/redbull-tracker-ge/actions/workflows/build_tracker_github.yml)
[![Run Red Bull Tracker](https://github.com/vazome/redbull-tracker-ge/actions/workflows/run_tracker_github.yml/badge.svg)](https://github.com/vazome/redbull-tracker-ge/actions/workflows/run_tracker_github.yml)
![Docker Image Version (tag)](https://img.shields.io/docker/v/vazome/redbull-tracker-ge/tracker-latest?arch=amd64&logo=docker&label=redbull-tracker-ge)

Convenient Red Bull price tracker made for Tbilisi, Georgia. This project covers both data collection and representation, with the latter delegated to Telegram bot and Grafana.

![image](.assets/redbull_architecture.drawio.svg)

As of now it supports two most major delivery providers: [Wolt](https://wolt.com/en/geo) and [Glovo](https://glovoapp.com/ge/en/tbilisi/).

Project utilizes: 
- Scripting \[Python, SQL\]
- Containerization \[Docker, Docker Hub, AWS ECS (EC2 based), AWS ECR\]
- CI/CD automation \[Github Actions, AWS CodePipeline, AWS CodeBuild, AWS CodeDeploy, AWS Lambda, AWS API Gateway\]
- Data storage \[AWS RDS for PostgreSQL, json\]
- User Interfaces \[Grafana, Telegram Bot API\]

Plans:
- [x] Bot: Deploy bot in AWS
- [x] Parse: Deploy parser in Github Actions with auto-commits for new json export files
- [x] Parser: enable parsing for most popular Tbilisi districts with products EN/GE variations.
- [x] DB: Enable product_volume column and autofill on Postgres side by parsing names
- [x] CI/CD: Implement Github actions for tracker and AWS CodePipeline for bot
- [x] CI/CD: Report AWS Codepipelie status and show it as a badge
- [ ] DB: Implement [Redis](https://github.com/redis/redis) for data cache hits and user responses 
- [ ] DB/Parser: Add [2 Nabiji](https://2nabiji.ge/en) grocery store
- [ ] Bot: Add product/store links to the bot output
- [ ] Bot: Allow users to define daily schedule time
- [ ] Bot: Dynamic checking of [`requests_data.json`](requests_data.json) file
- [ ] Grafana: Create average and lowest fluctuation charts
- [ ] Proxy: make requests via proxies for [run_tracker_github.yml](.github/workflows/run_tracker_github.yml)

## How to use

## Telegram bot
I've made a bot for immediate or daily reportings: [@RedBullTrackerBot](https://t.me/RedBullTrackerBot). Here is how it works:

https://github.com/vazome/redbull-tracker-ge/assets/46573198/3706c2ad-9227-4e72-a1a7-3eecae19d35a

## Grafana Analytics View
I wanted something to glance on and see the numbers changing, so I built a Grafana dashboard for that:

[<img width="1450" alt="image" src="https://github.com/vazome/redbull-tracker-ge/assets/46573198/7e62d523-29cd-4fb1-8d9e-308533685ad8">](https://vazome.grafana.net/public-dashboards/61b08f3b99974e1bab84a96e5c039a77)

Available here: [Red Bull Dynamics](https://vazome.grafana.net/public-dashboards/61b08f3b99974e1bab84a96e5c039a77)

## How does it work
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
The data parsing process is automated through GitHub Actions, which configurations are stored in [.github/workflows](.github/workflows) (default location).

The responsible action for scheduled runs is [![Run Red Bull Tracker](https://github.com/vazome/redbull-tracker-ge/actions/workflows/run_tracker_github.yml/badge.svg)](https://github.com/vazome/redbull-tracker-ge/actions/workflows/run_tracker_github.yml).

Tracker image is rebuilt if necessary tracker configurations are changed via git push, [![Build Tracker image with Github Actions](https://github.com/vazome/redbull-tracker-ge/actions/workflows/build_tracker_github.yml/badge.svg)](https://github.com/vazome/redbull-tracker-ge/actions/workflows/build_tracker_github.yml)

### Automation via AWS CI/CD
If necessary bot configurations are changed via git push, AWS CodePipeline rebuilds the image with new configurations.

Meanwhile AWS Lambda handles AWS CodePipeline status checks and AWS API Gateway makes the status available for the badge.
![AWS CodePipeline Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fdnxqhcr6z1.execute-api.eu-central-1.amazonaws.com%2FBadge%2FGetPipelineStatus&query=%24.status&logo=data:image/svg%2bxml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4gPHN2ZyB3aWR0aD0iODBweCIgaGVpZ2h0PSI4MHB4IiB2aWV3Qm94PSIwIDAgODAgODAiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+IDwhLS0gR2VuZXJhdG9yOiBTa2V0Y2ggNjQgKDkzNTM3KSAtIGh0dHBzOi8vc2tldGNoLmNvbSAtLT4gPHRpdGxlPkljb24tQXJjaGl0ZWN0dXJlLzY0L0FyY2hfQVdTLUNvZGVQaXBlbGluZV82NDwvdGl0bGU+IDxkZXNjPkNyZWF0ZWQgd2l0aCBTa2V0Y2guPC9kZXNjPiA8ZGVmcz4gPGxpbmVhckdyYWRpZW50IHgxPSIwJSIgeTE9IjEwMCUiIHgyPSIxMDAlIiB5Mj0iMCUiIGlkPSJsaW5lYXJHcmFkaWVudC0xIj4gPHN0b3Agc3RvcC1jb2xvcj0iIzJFMjdBRCIgb2Zmc2V0PSIwJSI+PC9zdG9wPiA8c3RvcCBzdG9wLWNvbG9yPSIjNTI3RkZGIiBvZmZzZXQ9IjEwMCUiPjwvc3RvcD4gPC9saW5lYXJHcmFkaWVudD4gPC9kZWZzPiA8ZyBpZD0iSWNvbi1BcmNoaXRlY3R1cmUvNjQvQXJjaF9BV1MtQ29kZVBpcGVsaW5lXzY0IiBzdHJva2U9Im5vbmUiIHN0cm9rZS13aWR0aD0iMSIgZmlsbD0ibm9uZSIgZmlsbC1ydWxlPSJldmVub2RkIj4gPGcgaWQ9Ikljb24tQXJjaGl0ZWN0dXJlLUJHLzY0L0RldmVsb3Blci1Ub29scyIgZmlsbD0idXJsKCNsaW5lYXJHcmFkaWVudC0xKSI+IDxyZWN0IGlkPSJSZWN0YW5nbGUiIHg9IjAiIHk9IjAiIHdpZHRoPSI4MCIgaGVpZ2h0PSI4MCI+PC9yZWN0PiA8L2c+IDxwYXRoIGQ9Ik0zMCwzMSBMMzUsMzEgTDM1LDI5IEwzMCwyOSBMMzAsMzEgWiBNMzYuNjY3LDYxLjE2NiBMMzQuODE3LDYwLjQwNyBMNDIuNDA5LDQxLjg4NSBMNDQuMjU5LDQyLjY0NCBMMzYuNjY3LDYxLjE2NiBaIE00NS41NzEsNTUuNzggTDUxLjA2OCw1MC45NTggTDQ1LjU3NSw0Ni4xOTcgTDQ2Ljg4Niw0NC42ODUgTDUzLjI0NSw1MC4xOTggQzUzLjQ2Myw1MC4zODcgNTMuNTg5LDUwLjY2MiA1My41OTAwMDYsNTAuOTUxIEM1My41OTEsNTEuMjQgNTMuNDY3LDUxLjUxNSA1My4yNDksNTEuNzA2IEw0Ni44OSw1Ny4yODQgTDQ1LjU3MSw1NS43OCBaIE0yNS41MDg5NzYsNTEuMDQ4IEMyNS41MDcsNTAuNzU5IDI1LjYzLDUwLjQ4NCAyNS44NDcsNTAuMjkzIEwzMi4xODQsNDQuNjkxIEwzMy41MDgsNDYuMTkgTDI4LjAyOSw1MS4wMzMgTDMzLjQ3OCw1NS43MyBMMzIuMTcxLDU3LjI0NSBMMjUuODU1LDUxLjc5OSBDMjUuNjM3LDUxLjYxMSAyNS41MTEsNTEuMzM3IDI1LjUwODk3Niw1MS4wNDggTDI1LjUwODk3Niw1MS4wNDggWiBNNjIuNTM1LDM1IEwxOC40NjUsMzUgQzE2LjU1NSwzNSAxNSwzMy40NDYgMTUsMzEuNTM2IEwxNSwzMSBMMjcsMzEgTDI3LDI5IEwxNSwyOSBMMTUsMTguNDY0IEMxNSwxNi41NTQgMTYuNTU1LDE1IDE4LjQ2NSwxNSBMNjIuNTM1LDE1IEM2NC40NDUsMTUgNjYsMTYuNTU0IDY2LDE4LjQ2NCBMNjYsMjkgTDM4LDI5IEwzOCwzMSBMNjYsMzEgTDY2LDMxLjUzNiBDNjYsMzMuNDQ2IDY0LjQ0NSwzNSA2Mi41MzUsMzUgTDYyLjUzNSwzNSBaIE0yMiw2NiBMNTgsNjYgTDU4LDM3IEwyMiwzNyBMMjIsNjYgWiBNNjIuNTM1LDEzIEwxOC40NjUsMTMgQzE1LjQ1MSwxMyAxMywxNS40NTEgMTMsMTguNDY0IEwxMywzMS41MzYgQzEzLDM0LjU0OSAxNS40NTEsMzcgMTguNDY1LDM3IEwyMCwzNyBMMjAsNjcgQzIwLDY3LjU1MiAyMC40NDcsNjggMjEsNjggTDU5LDY4IEM1OS41NTMsNjggNjAsNjcuNTUyIDYwLDY3IEw2MCwzNyBMNjIuNTM1LDM3IEM2NS41NDksMzcgNjgsMzQuNTQ5IDY4LDMxLjUzNiBMNjgsMTguNDY0IEM2OCwxNS40NTEgNjUuNTQ5LDEzIDYyLjUzNSwxMyBMNjIuNTM1LDEzIFoiIGlkPSJBV1MtQ29kZVBpcGVsaW5lX0ljb25fNjRfU3F1aWQiIGZpbGw9IiNGRkZGRkYiPjwvcGF0aD4gPC9nPiA8L3N2Zz4=&label=Build%20Bot%20image%20with%20AWS%20CI%2FCD&color=%2332CB55
)