# stock_prices

This repository contains the data project —[datasources](./datasources), and [endpoints](./endpoints)— and [data-generator](./data-generator) scripts for an audit log example of using Tinybird.

To clone the repository:

`git clone git@github.com:tinybirdco/stock_prices.git`

`cd stock_prices`

## Working with the Tinybird CLI

To start working with data projects as if they were software projects, let's install the Tinybird CLI in a virtual environment.
Check the [CLI documentation](https://docs.tinybird.co/cli.html) for other installation options and troubleshooting.

```bash
virtualenv -p python3 .e
. .e/bin/activate
pip install tinybird-cli
tb auth --interactive
```

Choose your region: __1__ for _us-east_, __2__ for _eu_

Go to your workspace, copy a token with admin rights and paste it. A new `.tinyb` file will be created.  

## Project description

```bash
├── README.md
├── data-generator
│   └── gen_data.py
├── datasources
│   ├── fixtures
│   │   ├── prices.ndjson
│   │   └── symbol_currency.csv
│   ├── prices.datasource
│   ├── prices_5min_mv.datasource
│   └── symbol_currency.datasource
├── endpoints
│   ├── avg_per_5mins.pipe
│   ├── avg_per_5mins_from_MV.pipe
│   ├── candlestick.pipe
│   ├── candlestick_from_MV.pipe
│   ├── last_price.pipe
│   └── ui_filter_symbols.pipe
└── pipes
    └── mat_5_mins.pipe
```

## Pushing the data project to your Tinybird workspace

### Pushing the simplest version, no MVs yet

Push the data project —datasources, endpoints and fixtures— to your workspace.

```bash
tb push datasources/prices.datasource datasources/symbol_currency.datasource --fixtures
```

```bash
tb push endpoints/candlestick.pipe endpoints/avg_per_5mins.pipe endpoints/ui_filter_symbols.pipe endpoints/last_price.pipe
```
  
Your data project is ready for realtime analysis.

### Pushing the MV to improve performance

See this [guide](https://www.tinybird.co/guide/materialized-views) to learn more about Materialized Views.

Let's push the pipe that materilizes, and as we push deps, the _prices_5min_mv.datasource_ will be generated. We add the --populate flag to move the already existing data to the MV.

```bash
tb push --push-deps --populate --wait pipes/mat_5_mins.pipe
```

And now we can push the endpoints that get the same results from the MV.

```bash
tb push endpoints/avg_per_5mins_from_MV.pipe endpoints/candlestick_from_MV.pipe 
```

## Check the values from a frontend

Go to your workspace and copy the value of the __stock_prices_demo token__.

Visit this page with your token:
[https://pocs.tinybird.co/stockprices?token=<YOUR_DEMO_TOKEN>](https://pocs.tinybird.co/stockprices?token=)

## Ingesting data using the /events endpoint

Let's add some data through the [/events endpoint](https://www.tinybird.co/guide/high-frequency-ingestion).

To do that we have created a python script to generate and send dummy events.

```bash
python3 data-generator/gen_data.py
```

Note: Ctrl+C to stop ingestion.

## Ask us any doubt

This project shows just some of the features of Tinybird. If you have any questions, come along and join our community [Slack](https://join.slack.com/t/tinybird-community/shared_invite/zt-yi4hb0ht-IXn9iVuewXIs3QXVqKS~NQ)!
