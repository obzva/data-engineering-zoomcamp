# Module 2 Homework: Workflow Orchestration

I set Kestra on my GCP VM instance and setting details are like below
- queue & repo: GCP SQL (postgres)
- storage: GCP Cloud Storage Bucket

Kestra extracted csv data from github and then loaded them onto my GCP Big Query dataset (as almost same as tutorial)

## Question 1

Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size (i.e. the output file yellow_tripdata_2020-12.csv of the extract task)?

A. 128.3MB

## Question 2

What is the value of the variable file when the inputs taxi is set to green, year is set to 2020, and month is set to 04 during execution?

A. green_tripdata_2020-04.csv

## Question 3

How many rows are there for the Yellow Taxi data for the year 2020?

A. 24,648,499

```sql
SELECT COUNT(1)
FROM `MY_PROJECT.MY_DATASET.yellow_tripdata`
WHERE filename LIKE '%2020%'
;
```

## Question 4

How many rows are there for the Green Taxi data for the year 2020?

A. 1,734,051

```sql
SELECT COUNT(1)
FROM `MY_PROJECT.MY_DATASET.green_tripdata`
WHERE filename LIKE '%2020%'
;
```

## Question 5

How many rows are there for the Yellow Taxi data for March 2021?

A. 1,925,152

```sql
SELECT COUNT(1)
FROM `MY_PROJECT.MY_DATASET.yellow_tripdata_2021_03`
;
```

## Question 6

How would you configure the timezone to New York in a Schedule trigger?

A. Add a timezone property set to America/New_York in the Schedule trigger configuration

[Kestra API reference link](https://kestra.io/plugins/core/triggers/io.kestra.plugin.core.trigger.schedule#timezone)