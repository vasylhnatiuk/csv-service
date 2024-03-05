# CSV-reader

## Project Description

### Key Features

- **Client Management**: The application allows users to manage clients by importing data from CSV files.
- **Data Import**: Users can import client data from CSV files, which are then stored in the database.
- **Data Visualization**: Users can use Swgger to see data and download file with data in scv format 

## Installation

To run the project using Docker Compose, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/project_name.git
2. Install requirements.txt
   ```bash
   pip install -r requirements.txt
3. Build and up set app by docker-compose (Docker and Docker-Compose should be installed!)
   ```bash
   docker-compose up --build
  
## Usage
1. To view, filter, and retrieve data, use Swagger:
   ```bash
   http://127.0.0.1:8000/api/doc/swagger/

2. To upload data from a CSV file, use the following command::
```bash
   python manage.py import_clients_from_csv file_name.txt

