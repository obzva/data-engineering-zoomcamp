# Data Engineering Zoomcamp

This is a repo of my notes, hands-on practices and homework from [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp), free online data engineering bootcamp.

I registered in 2025 cohort of this camp.

Here are some notes.

I wrote this down after each chapter and I just jotted down.

If it looks messy and un-organized, I am sorry.

## Module 1: Containerization and Infrastructure as Code

### 01. Docker and Terraform

- Learned Docker and how to run DB and some related things on Docker containers
- While following this chapter, [Ingesting NY Taxi Data to Postgres](https://www.youtube.com/watch?v=2JM-ziJt0WI&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=6), there was a little issue:
  - NYC no more provides their data in csv format but parquet
  - I handled it by converting parquet into csv with `pandas` and `pyarrow`
- I encountered several environment setting issues e.g. jupyter notebook showed me blank page, psycopg2 installation didn't work so well, ... and it may be related to my local python environment and package installation methods and here are my learning points
  - Check which python and which pip are you using while installing some packages if you don't want to see messages like `ImportError: No module named...`
  - It seems like mixed use of pip and brew might cause some problems
  - Although I didn't set venv in this chapter, using venv surely will blow these problems all gone and make you happy
- I excluded local database, `ny_taxi_postgres_data`, from git (see `.gitignore`)