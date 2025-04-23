# Database-Project

## Repository

You can find the code here: [GitHub Repository](https://github.com/stephaniefangs/Database-Project)

## Getting Started

Follow these steps to build and run the application locally.

### 1. Clone the Repository

```bash
git clone https://github.com/stephaniefangs/Database-Project.git
cd Database-Project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a .env File

```bash
USERNAME=our_group_username
PASSWORD=our_group_password
```

### 4. Run the Scheduler

```bash
python manage.py runapscheduler
```

Starts the APScheduler, which is responsible for update book fees once per day (NOTE: RUN ONLY ONE SCHEDULER AT A TIME)

### 5. Run the Application

```bash
python manage.py runserver
```

Run in a seperate instance from the scheduler.
Once this server is running, open your browser and go to http://127.0.0.1:8000/ or click on the link in your terminal. 

## Extra

Make sure you have Python installed. This project also uses Django.
