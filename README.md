# e-menu

## Description
This is a simple application to manage menus in a restaurant. It allows to create menus, menu positions and send them to the users via email.

App is written in FastAPI and uses PostgreSQL as a database.
It also uses alembic for database migrations.

## Database
Database have tables such as:
### 1. users
It stores user's email, login and password, which are encrypted. It is being used for authentication, also for sending emails.

### 2. menu_positions
This table stores menu positions, which can be a single dishes in the menu. It stores the name, description, price and the creation / updates dates.

### 3. menus
This table stores the menus. It stores the name.

### 4. menu_menu_positions
Because of the many-to-many relationship between menus and menu_positions, this table is created to store the relations between them.
With that, every menu position know which menus it belongs to and every menu knows which menu positions it contains.
Records are being automatically deleted when the menu or menu position is deleted.

### 5. mail_pool
Sending emails require from us to search whole menu_positions table for the positions created yesterday, which can be a heavy operation in case there are many records in the table.
Because of that, there is mail_pool table, which stores foreign keys to the menu_positions created or updated in the last time.
When it comes to sending emails, we can just search for the records in the mail_pool table and send the emails to the users.
At the end, we the records from the mail_pool table are being deleted (not those one that were created today: those one are being sent in the next day).


## Configuration:
### 1. Requirements:
- Python 3.11 or higher
- Poetry 1.6 or higher (only for run init script or unit tests - it is not required for running the app)

### 2. Env variables
Please check file called .env, especially the following variables:

#### 2.1 Email configuration
If you want to enable sending emails, please set the following variables:
* SMTP_ENABLED
* SMTP_PORT
* SMTP_USER
* SMTP_PASSWORD

***And set variable SMTP_ENABLED to true***

### 3. Running the app
```bash
docker compose up --build
```
It will create two services: db (postgresql) and app (fastapi)

### 4. Example data
You can use init_data.main.py script to create some example data in the database (before that make sure that app and database is running - previous command :) ).  
This script will generate some menu positions, menus, users and mail pool with menu positions generated / created today and yesterday.
Please add your email to USERS variable in the init_data.init_schemas.py if you want to receive mails (or create user by /admin/user endpoint).

### 4.1 Create venv
```bash
python -m venv venv
```

### 4.2 Activate venv
```bash
source venv/bin/activate
```

### 4.3 Install dependencies
```bash
poetry install
```

### 4.4 Run the script
```bash
python3 init_data.main.py
```

## Endpoints:
Documentation is automatically generated by swagger. You can find it under: 0.0.0.0:8000/docs

### 1. Public endpoints:
Public user is able to:
- search for menus (it is possible to sort/filter menus by its properties)

### 2. Private endpoints:
Private endpoints require authentication. 
The simplest way to achieve that is to use init_data.main.py script to create a user. 
Then you can use the following credentials:
- login: admin
- password: string

Authenticated user is able to:
- create, remove, update and delete menu positions
- create, remove, update and delete menus
- create and get users
- add / remove menu positions to the menu


## Unit tests:
If you want to run the unit test, you have to run db service:
```bash
docker compose up db -d
```

Then you can run the tests:
```bash
pytest
```
Coverage is about 86%.


## Future improvements:
* Add images for the menu positions: Use S3 to store images and add image_url column for menu_positions table.
* Add more tests: Add integration tests, e2e tests, tests for the email sending.
* Response pagination: especially for the GET /menu endpoint.
