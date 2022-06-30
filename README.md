# Sereno

A rules-based alerting and monitoring tool.

_Sereno_ is short for _el sereno_, which translates to _"watchman"_
in Spanish.

### Background

Social Systems, Inc. runs 3 different production services:

- Inbox Service: A backend RPC service that loads customer social
  media inbox data
- Report PDF Generator: A backend RPC service that generates custom
  PDF reports based on customer's social media data
- Facebook Realtime: A streaming ingestion service that receives
  realtime events from Facebook
  
All of these systems run with the following server level topology:

Inbox Service (ID: InboxService), load balanced between 3 different
servers: `inbox_production01`, `inbox_production02`, `inbox_production03`

Report PDF Generator (ID: ReportPDFGenerator), load balanced between 2
different servers: `reporting_pdf01`, `reporting_pdf02`

Facebook Realtime (ID: FacebookRealtime), active / passive with 2
different servers: `facebook_realtime01`, `facebook_realtime02`

> So what is Sereno trying to solve?

The SRE team was tasked with building an in-house monitoring and alerting system that
would help Social Systems Inc. observe operational problems with their production
services. Each server in their infrastructure has a running agent daemon
that monitors important components and pushes JSON events to a centralized
service every minute. An example event might look something like:

```json
{"server":"inbox_production01","service":"InboxService","component":"Load5mAvg","value":3.2,"timestamp":1476057600,"active":true}
```

The SRE team implemented an alert monitoring system that triggers alerts under the following conditions:

- Send an alert when any server's `DiskUsedPercentage` component exceeds 0.9 (90%). Do not alert for inactive servers.
- Send an alert when the majority of servers within a service exhibit `Load5mAvg` with a value greater than 4.0 at the same time. Do not include inactive servers when calculating majority.
- For non-server specific metrics (clustered services), the server field is replaced with the threshold.

For extensibility and ease-of-maintenance, the SRE team decided 
to utilize a rule-based engine and configuration-based approach
to define multiple conditions.

Please refer to [sereno/conf/rules.yaml](sereno/conf/rules.yaml)
for documentation regarding the rules.

### Installation

Requirements: Python 3.5+

#### Local/Virtual Environment

Simply run the following to install Sereno and
its dependencies locally or in a virtual environement:

```
./setup.py install
```

### Docker

You may build the Sereno Docker image locally by executing the following command:
```
docker build . -t sereno
```

### Development

#### Linting

[pylint](https://www.pylint.org/) and [flake8](https://flake8.pycqa.org/en/latest/) are used for linting.

#### Formatting

[`black`](https://github.com/psf/black) is the preferred tool for automformatting.

<!-- TODO: Unit Tests
#### Unit tests

TODO.
-->

### Usage

#### Installed with setuptools

Full usage instructions can be found by executing `sereno -h`.

After installing Sereno locally, you may run it against the sample data by executing:

```
sereno sample.json
```

#### Docker

Simply mount the metrics data into the container and run it as below:

```
docker run -it --rm -v `pwd`/sample.json:/data/sample.json sereno /data/sample.json
```

## License

Sereno is licensed under the GPL v3.0 license.
