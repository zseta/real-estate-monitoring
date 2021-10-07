# Real estate market monitoring tool with Scrapy, TimescaleDB, and Superset
This repo contains the sample application I presented on Extract Summit 2021

**Technologies**

* Scrapy for web data extraction
* TimescaleDB for storing data
* Superset to explore the data

## Setup

The whole project is Dockerized except the web spiders, for those you need to create a virtual environment, install 
the requirements and adjust the spiders to work with the websites you want to scrape.

But even if you don't want to set up the spiders, you can install this project by just cloning the repo and running a 
`docker-compose up` and it will build out itself.

The database and the Superset dashboard is fully Dockerized. After installation you will have a local TimescaleDB and 
a local Superset instance running - with real web extracted data (100K+ rows).

The Docker service uses port 8088 so make sure there's not other service using that port.


### Prerequisites

* [Docker](https://docs.docker.com/get-docker/)
* [Docker compose](https://docs.docker.com/compose/install/)

    Verify that both are installed:
    ```bash
    docker --version && docker-compose --version
    ```
* [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) (optional, only needed for the spiders)
    ```bash
    virtualenv venv && source venv/bin/activate
    pip install -r requirements.txt
    ```

### Installation

1. Clone the repo:
    ```bash
    git clone https://github.com/zseta/real-estate-monitoring
    ```
1. Run `docker-compose up` in the root folder of the project:
    ```bash
    cd real-estate-monitoring
    docker-compose up
    ```
    See when the process is done (it could take ~1min):
    ```bash
    superset-dashboard_1  | ****************Superset is starting up****************
    superset-dashboard_1  | ****************Go to http://0.0.0.0:8088/ to login****************
    ```
1. Go to http://0.0.0.0:8088/ in your browser and login with these credentials:
    ```txt
    user: admin
    password: admin
    ```
1. Open the `Databases` page inside Superset (http://0.0.0.0:8088/databaseview/list/). You will see exactly one item there
    called `real-estate`.
1. Click the edit button (pencil icon) on the right side of the table.
1. Don't change anything in the popup window, just click `Finish`. This will make sure the database can be 
    reached from Superset.
1. Go to the real-estate dashboard page (http://0.0.0.0:8088/superset/dashboard/1/) and you will see the all the charts that have 
    been created based on the web extracted data stored in TimescaleDB.


## Schema design

| Data field         | Field description                       |
|--------------------|-----------------------------------------|
| url                | Listing url.                            |
| time               | Time of extraction.                     |
| city               | Listing's city.                         |
| address            | Listing's address.                      |
| area               | Property area (m2).                     |
| rooms              | Number of rooms.                        |
| price              | Listing's price in HUF.                 |
| property_condition | Property condition.                     |
| build_year         | Property build year.                    |
| description        | Listing's description                   |
| floor              | On which floor the property is.         |
| building_floors    | Number of floors in the whole building. |
| property_type      | Type of the property.                   |
| area_lot           | Lot area (for houses).                  |
| price_eur          | Price in EUR.                           |
