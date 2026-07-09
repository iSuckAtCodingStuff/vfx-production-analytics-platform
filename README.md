
# 🎬 VFX Production Analytics Platform

A production-inspired **Data Engineering** project that simulates the end-to-end data pipeline of a Visual Effects (VFX) studio. The platform ingests synthetic production data, validates and transforms it through multiple ETL layers, loads it into a dimensional Snowflake data warehouse, and prepares it for analytical reporting and visualization.

The project is designed to demonstrate industry-standard Data Engineering practices rather than serve as a tutorial or coding exercise.

---

# Project Objectives

- Build a production-quality ETL pipeline using Python and PostgreSQL.
- Design a scalable multi-layer data architecture (Raw → Staging → Warehouse).
- Implement reusable validation, logging, and error handling.
- Model a Snowflake dimensional warehouse optimized for analytics.
- Extend the platform into a modern cloud-based ELT architecture in future phases.

---

# Tech Stack

| Category | Technologies |
|----------|--------------|
| Language | Python 3 |
| Database | PostgreSQL 18 |
| ORM | SQLAlchemy |
| SQL Client | DBeaver |
| Data Processing | Pandas |
| Data Generation | Faker |
| Version Control | Git & GitHub |
| Logging | Python Logging |
| Future | Apache Spark, Google Cloud Platform (BigQuery, Cloud Storage), Plotly |

---

# Project Architecture

```text
                CSV Files
                    │
                    ▼
              Python ETL Pipeline
                    │
      ┌─────────────┴─────────────┐
      ▼                           ▼
     Raw                      Validation
      │
      ▼
   Staging
      │
      ▼
 Warehouse (Snowflake Schema)
      │
      ▼
 Analytics SQL Layer
      │
      ▼
 Python Dashboard
```

---

# ETL Architecture

## Raw Layer

- Mirror source data exactly.
- Preserve original records.
- Enable traceability and reprocessing.
- Generic CSV loader
- Config-driven ingestion
- SQLAlchemy integration
- Logging

## Staging Layer

- Clean and normalize incoming data.
- Apply business validation.
- Prepare data for dimensional modeling.
- Centralized validation framework
- Invalid row logging
- Metadata-driven transformations
- Reusable helper functions
- Idempotent loading

## Warehouse Layer

Dimensions:
- dim_project
- dim_sequence
- dim_shot
- dim_task
- dim_artist
- dim_date

Facts:
- fact_task_assignment
- fact_timesheet
- fact_render
- fact_delivery

Features:
- Surrogate keys
- Natural business keys
- Named constraints
- Foreign key integrity
- Index optimization
- Audit columns

---

# Project Structure

```text
VFX Production Analytics Platform/

├── data/
├── database/
│   ├── raw_schema.sql
│   ├── staging_schema.sql
│   ├── warehouse_schema.sql
│   ├── indexes.sql
│   └── verify_warehouse.sql
├── pipeline/
│   ├── config.py
│   ├── db.py
│   ├── logger.py
│   ├── load_raw.py
│   ├── transform.py
│   ├── warehouse_loader.py
│   └── load_warehouse.py
├── analytics/
│   ├── project_metrics/
│   ├── artist_metrics/
│   ├── production_metrics/
│   ├── render_metrics/
│   └── delivery_metrics/
└── README.md
```

---

# Current Project Status

## ✅ Completed

- Synthetic VFX production dataset generation
- Raw ETL pipeline
- Staging ETL pipeline
- Centralized validation framework
- Invalid row logging
- Snowflake dimensional warehouse
- SQLAlchemy warehouse loader
- Warehouse verification scripts
- End-to-end dimensional validation
- Production-inspired project architecture

## 🚧 In Progress

### Analytics SQL Layer

- Project KPIs
- Production metrics
- Artist utilization
- Render performance
- Delivery analytics
- Executive dashboards

Each report will be maintained as an independent SQL script.

## 🔮 Planned Enhancements

- Interactive Python dashboards
- Data dictionary
- Architecture diagrams
- ETL documentation
- Apache Spark integration
- Google Cloud Platform (GCS & BigQuery)
- Modern cloud-native ELT architecture

---

# Design Principles

- Production-quality code
- Readability over clever abstractions
- Modular architecture
- Separation of concerns
- Reusable components
- Idempotent ETL
- Centralized configuration
- Analytics-ready data modeling
- Scalable and maintainable design

---

# Future Roadmap

- Complete Analytics SQL library
- Build interactive Python dashboards
- Expand technical documentation
- Integrate Apache Spark
- Migrate analytics workflow to Google Cloud
- Implement a modern ELT architecture

---

# Author

**Jaydeep Das**

**Data Engineer | Python Developer | Former CreatureFX Technical Director**

Experienced in Python automation, ETL pipelines, workflow optimization, backend tooling, and large-scale VFX production data processing.

This repository demonstrates the design and implementation of a production-inspired analytics platform using modern data engineering practices.
