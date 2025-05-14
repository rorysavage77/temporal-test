# temporal-test
Just a simple app to test temporal workflows

# Temporal Healthcheck Python App

This application connects to a Temporal cluster and runs a simple healthcheck workflow that emits a log event every 5 seconds ("Hello, world! Healthcheck at <date>").

## Prerequisites
- Python 3.8+
- Access to a running Temporal server (default: localhost:7233)

## Setup
```sh
pip install -r requirements.txt
```

## Running the App
```sh
python temporal_healthcheck.py
```

The workflow logs a healthcheck event every 5 seconds. Check your Temporal UI or logs for output.
