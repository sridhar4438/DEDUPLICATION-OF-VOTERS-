# Setup Instructions for De-duplication Analysis Project

## Prerequisites

1. **Python 3.7 or higher** - Download from https://www.python.org/downloads/
   - During installation, make sure to check "Add Python to PATH"

2. **MySQL Server** - Download from https://dev.mysql.com/downloads/mysql/
   - Set root password as "root" (or update settings.py if using different password)

## Installation Steps

### 1. Install Python Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install pandas==0.25.3
pip install numpy==1.19.2
pip install Django==2.1.7
pip install PyMySQL==0.9.3
pip install openpyxl==3.0.9
pip install matplotlib==3.3.4
```

### 2. Setup MySQL Database

1. Open MySQL command line or MySQL Workbench
2. Run the SQL commands from `DB.txt`:
   ```sql
   create database deduplicate;
   use deduplicate;
   
   create table register(username varchar(30) primary key,
   password varchar(30),
   contact varchar(12),
   email varchar(30),
   address varchar(40));
   ```

### 3. Run Database Migrations

```bash
python manage.py migrate
```

### 4. Start the Development Server

```bash
python manage.py runserver
```

Or simply double-click `run.bat`

The server will start at http://127.0.0.1:8000/

## Access the Application

Open your web browser and navigate to:
- http://127.0.0.1:8000/index.html

## Notes

- Make sure `DataVoter.xlsx` file exists in the project root directory
- The application uses MySQL database with:
  - Host: 127.0.0.1
  - Port: 3306
  - User: root
  - Password: root
  - Database: deduplicate

