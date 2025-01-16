# Module 1 Homework: Docker & SQL

## Question 1. Understanding docker first run

Run docker with the `python:3.12.8` image in an interactive mode, use the entrypoint bash.

What's the version of pip in the image?

A. 24.3.1

```
$ docker run -it --entrypoint bash python:3.12.8 
Unable to find image 'python:3.12.8' locally
3.12.8: Pulling from library/python
e05e1469c731: Download complete 
ded9ddaf4f92: Download complete 
Digest: sha256:5893362478144406ee0771bd9c38081a185077fb317ba71d01b7567678a89708
Status: Downloaded newer image for python:3.12.8
root@244410f55f33:/# pip --version
pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)
```

## Question 2. Understanding Docker networking and docker-compose

Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin  

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

A. db:5432

Since `docker compose` automatically creates a default network and connects all services to it, containers should communicate via ther internal ports, not mapped ports, inside that network.

## Prepare Postgres

To load gzipped csv into PostgreSQL with python script, I made `ingest_gzipped_csv_data.py`.

## Question 3. Trip Segmentation Count

During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened:

1. Up to 1 mile
2. In between 1 (exclusive) and 3 miles (inclusive),
3. In between 3 (exclusive) and 7 miles (inclusive),
4. In between 7 (exclusive) and 10 miles (inclusive),
5. Over 10 miles

A. 104802, 198924, 109603, 27678, 35189

```sql
SELECT
	COUNT(*) FILTER (WHERE trip_distance <= 1),
	COUNT(*) FILTER (WHERE trip_distance > 1 AND trip_distance <= 3),
	COUNT(*) FILTER (WHERE trip_distance > 3 AND trip_distance <= 7),
	COUNT(*) FILTER (WHERE trip_distance > 7 AND trip_distance <= 10),
	COUNT(*) FILTER (WHERE trip_distance > 10)
FROM green_taxi_trips
WHERE DATE(lpep_pickup_datetime) >= '2019-10-01'
	AND DATE(lpep_dropoff_datetime) < '2019-11-01'
;
```

## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.

A. 2019-10-31

```sql
SELECT DATE(lpep_pickup_datetime)
FROM green_taxi_trips
ORDER BY trip_distance DESC
LIMIT 1
;
```

## Question 5. Three biggest pickup zones

Which were the top pickup locations with over 13,000 in `total_amount` (across all trips) for 2019-10-18?

Consider only `lpep_pickup_datetime` when filtering by date.

A. East Harlem North, East Harlem South, Morningside Heights

```sql
SELECT
	z."Zone",
	SUM(g.total_amount)
FROM green_taxi_trips AS g
JOIN zones AS z
	ON g."PULocationID" = z."LocationID"
WHERE DATE(g.lpep_pickup_datetime) = '2019-10-18'
GROUP BY z."Zone"
ORDER BY SUM(g.total_amount) DESC
LIMIT 3
;		
```

## Question 6. Largest tip

For the passengers picked up in Ocrober 2019 in the zone name "East Harlem North" which was the drop off zone that had the largest tip?

A. JFK Airport

```sql
SELECT "Zone"
FROM zones
WHERE "LocationID" = (
	SELECT gtt."DOLocationID"
	FROM green_taxi_trips AS gtt
		JOIN zones AS z
			ON gtt."PULocationID" = z."LocationID"
	WHERE DATE_TRUNC('month', gtt.lpep_pickup_datetime) = '2019-10-01 00:00:00'
		AND z."Zone" = 'East Harlem North'
	ORDER BY gtt.tip_amount DESC
	LIMIT 1
)
;
```

## Question 7. Terraform Workflow

Which of the following sequences, respectively, describes the workflow for:

1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform`

A. terraform init, terraform apply -auto-aprove, terraform destroy
