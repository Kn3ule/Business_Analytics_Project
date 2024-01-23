# Wildlife Tracker Application
This application was developed as part of the Business Analytics - System Development course at Aalen University.

## Overview
Our Wildlife Tracker Application is an innovative tool designed to facilitate the tracking and analysis of wildlife data. Developed with Python and Dash, this application offers a robust web interface for data management and visualization. It leverages a PostgreSQL database for data storage, SQL Alchemy for efficient data handling, and integrates R for advanced data analytics. This unique combination of technologies ensures a seamless experience in wildlife data tracking and analysis.

## Features
- **Data Creation and Editing:** Intuitive web interface to input, access and modify wildlife data.
- **Data Visualization:** Dynamic dashboards for visualizing wildlife trends and patterns.
- **Advanced Analytics:** Integration with R for sophisticated data analysis, ensuring accurate and insightful results.
- **Database Integration:** Robust PostgreSQL database for secure and efficient data storage.

## Technologies Used
- **Python:** Core programming language for application development.
- **Dash:** Framework for building the web interface.
- **PostgreSQL:** Database system for data storage.
- **SQL Alchemy:** Toolkit for database management and communication.
- **R:** Language and environment for statistical computing and graphics.
- **rpy2:** Interface for calling R from Python.
- **RDS files:** Format for storing R data structures.

## Installation

### Prerequisites
- Python 3.x
- R
- PostgreSQL

### Setup
1. **Clone the Repository:**
   ```bash
   git clone [repository-url]
   ```
2. **Install Dependencies:**
   - Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - R dependencies (run in R console):
     ```R
     install.packages("RPostgres")
     ```
3. **Connect the service to Postgres Database**
   - Create .env File with following information for python db-connection:
     ```bash
     POSTGRES_URL="postgres://{user}:{password}@{hostname}:{port}/{database-name}"
     ```
   - Insert db-connection information in genus_analytics.R and genus_specific_analytics.R:
     ```R
     # Establish a connection using RPostgres
      con <- dbConnect(
        RPostgres::Postgres(),
        dbname = "dbname",
        user = "postgres",
        password = "password",
        host = "localhost",
        port = 5432
      )
     ```
   - Insert the database model to your postgres:
     - start the models.py

## Usage
1. **Start the Application:**
   ```bash
   python app.py
   ```
2. **Navigate to the Web Interface:** Open your browser and go to `http://localhost:8050` (or the configured port). 
