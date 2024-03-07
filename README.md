# Django RESTFful Authentication Endpoints
Customizable RESTful API endpoints to facilitate user registration, login, access token refreshing, password reset, and password change functionalities. 

## Application Framework and Database
The backbone of my application is built upon Django Rest Framework with a robust PostgreSQL database.

## Authentication with JWT
Security is paramount. My system employs JWT (JSON Web Token) authentication, offering a secure and efficient method to authorize users.


## API Endpoints

POST /auth/register/ : create a new user account.

POST /auth/login/ : log in to an existing user account and receive an access token.

POST /auth/activate/ : activate your account after registration by clicking the link sent to the provided email.

POST /auth/resend-activation/ : resend the activation link that was sent during registration.

POST /auth/forgot-password/ : request a link for resetting your password in case you've forgotten it.

POST /auth/reset-password/ : reset your password by providing the new passwords.

POST /auth/change-password/ : change password while authenticated

GET  /auth/profile/ : get profile information while authenticated

PUT/PATCH /auth/profile/ : update profile information while authenticated

## How to install and run it locally

### Download
To download/clone the this app, move to your desired directory where to want to put the app and run the following commands.
Note: Make sure you have git installed. You can install git with the following commands.

Ubuntu::

    sudo apt update
    sudo apt install git

CentOS/Fedora/RedHat::

    sudo yum update
    sudo yum install git

OSX::

    brew install git

Download/Clone the App inside the directory of your choice.

To download/clone the app::

    git clone https://github.com/moses-mugoya/AuthModule.git

Install system required modules such as python, pip and postgresql::

    sudo apt install python3.10

    sudo apt install python3.10-pip python3.10-dev libpq-dev postgresql postgresql-contrib file
    
Before installing the required packages, it is recommended to create a virtual envirinment. The virtual environment for python 3.10 is created as follows.

    Install virtual environment for python 3.10 if you have not

    Install install virtualenv using pip3::

    sudo pip3 install virtualenv
    
Now move to the root directory of the downloaded project at create a virtual environment with your desired name. For instance::

    virtualenv --python=python3.10 venv
    
Active your virtual environment::

    source .venv/bin/activate

To install all the required packages, run the command in the root project folder::

    pip3 install -r requirements.txt
    
### Create database for Note App to use.

Create a database note_db::

    $ sudo -u postgres psql
    # CREATE DATABASE auth_db;

Create a user for the Database and grant them privileges::

    # CREATE USER auth_user WITH PASSWORD 'n0t3p@ss';
    # ALTER ROLE auth_user SET client_encoding TO 'utf8';
    # ALTER ROLE auth_user SET default_transaction_isolation TO 'read committed';
    # ALTER ROLE auth_user SET timezone TO 'UTC+3';
    # GRANT ALL PRIVILEGES ON DATABASE auth_db TO auth_user;
    # ALTER USER auth_user CREATEDB;

You can use different names for the user and database but be sure to change the same in the application settings file database section

## Basic Commands

### Database Migrations

    $ python3 manage.py migrate

### Run the Tests
    $ python3 manage.py test

    
### Create Superuser
    $ python3 manage.py createsuperuser

### Run the development server
    $ python3 manage.py runserver

This will open the development server on http://localhost:8000






