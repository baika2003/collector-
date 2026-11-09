Collector

Centralized Log Collection System

Collector is a lightweight log collection system designed for centralized log ingestion from different sources.

Features

UDP Syslog log receiver

HTTP log ingestion endpoint

RAW event storage in JSONL format

File monitoring agent

HTTP event forwarding

Checkpoint-based file reading

Architecture

Log Sources
    |
    +---- UDP Syslog ----> Syslog Receiver
    |
    +---- File Logs -----> Collector Agent
                              |
                              v
                         HTTP /ingest
                              |
                              v
                         RAW Storage

Project Structure

collector/
├── agent/
│   └── agent.py
├── server/
│   ├── main.py
│   └── syslog.py
├── storage/
│   └── raw/
├── requirements.txt
└── README.md

Installation

git clone https://github.com/baika2003/collector-.git
cd collector-

Install dependencies:

pip install -r requirements.txt

Run HTTP Server

python server/main.py

Run Syslog Receiver

python server/syslog.py

Run Agent

python agent/agent.py --file sample.log --server http://127.0.0.1:8000/ingest

API Endpoints

Method

Endpoint

Description

GET

/health

Server health check

POST

/ingest

Receive log events

Storage

Events are stored in:

storage/raw/events.jsonl

Project Status

Version: 0.1.0

Status: Initial development.
