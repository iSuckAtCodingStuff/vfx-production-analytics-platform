# 🎬 VFX Production Analytics Platform

## 📌 Overview

The VFX Production Analytics Platform is a simulated end-to-end data engineering project that models a real-world Visual Effects (VFX) studio production pipeline.

It generates structured production data such as artists, projects, sequences, shots, tasks, and assignments, and enforces realistic relationships between them. The project also includes data validation checks to ensure consistency and integrity across all datasets.

This project demonstrates core Data Engineering skills including ETL pipeline design, relational data modeling, data validation, and analytics-ready dataset creation.

## 🏗️ Project Structure

data_generation/        → Data generation scripts (ETL source layer)  
generate.py             → ETL pipeline orchestrator (runs full data generation)  
data/                   → Output datasets (raw and processed)  
main.py                 → Data loading and validation entry point  

## 📊 Data Model

The project simulates a VFX studio production workflow.

Entities:
- Artists → Creative professionals working on production tasks  
- Projects → Client-driven productions (films, series, etc.)  
- Sequences → Logical breakdown of projects  
- Shots → Individual production units within sequences  
- Tasks → Work units such as Animation, FX, Lighting, Compositing  
- Assignments → Mapping between artists and tasks  

## 🔗 Data Relationships

Projects → Sequences → Shots → Tasks → Assignments → Artists

This hierarchy represents a real-world VFX production pipeline where work flows from high-level project planning down to individual artist task execution.

## ⚙️ How to Run the Project

1. Install dependencies  
pip install -r requirements.txt  

2. Generate datasets (ETL pipeline)  
python generate.py  

This creates CSV files inside:  
data/raw/

3. Run data validation  
python main.py  

This step:
- Loads generated datasets
- Runs data integrity checks
- Validates relationships between entities
- Detects data quality issues

## 🧪 Validation Checks

- Primary key uniqueness validation  
- Foreign key integrity checks  
- Date consistency validation (start_date < end_date)  
- Null / missing value detection  
- Task assignment consistency checks  
- Negative or invalid hours detection  

## 📂 Output Datasets

data/raw/
- artists.csv
- projects.csv
- sequences.csv
- shots.csv
- tasks.csv
- task_assignments.csv

## 🛠️ Tech Stack

- Python 3.9+
- Pandas
- NumPy
- Faker
- Git

## 🎯 Learning Outcomes

This project demonstrates:
- Building modular ETL pipelines in Python
- Designing relational data models
- Simulating real-world production systems
- Writing data validation and quality checks
- Structuring analytics-ready datasets

## 🚀 Future Enhancements

- PostgreSQL data warehouse integration  
- Star schema (fact & dimension modeling)  
- SQL analytics layer (KPI queries)  
- Power BI / Tableau dashboards  
- Logging and pipeline monitoring system  

## 👨‍💻 Author

Jaydeep Das  
Data Engineering Portfolio Project
