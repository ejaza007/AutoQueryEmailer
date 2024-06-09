# Automated Database Query and Email Manager

A secure database query and email manager, specifically designed for automating routine queries and emailing data to recipients.

## Features

- **Self-Explanatory GUI**: Navigate the intuitive interface with ease.
- **On-Demand Queries**: Set up queries to run on demand and save the results.
- **Scheduled Routines**: Schedule queries to run at specific times and save the results.
- **Email Management**: Set up recipient emails to send data.
- **Email Attachments**: Attach files to emails.
- **Bulk Emailing**: Send bulk emails to all selected recipients.
- **Database Connections**: Utilize both SQL and Windows Authentication for database connections.
- **Encrypted Credentials**: Save encrypted credentials for sender's email and SQL connection methods.
- **Multithreading**: Use multithreading to avoid freezing the program while querying data from the database and to send emails in parallel, speeding up the overall process.

## Libraries Utilized

- `tkinter`: For creating the GUI.
- `threading`: For multithreading functionality.
- `cryptography.fernet`: For encrypting credentials.
- `smtplib`: For sending emails.
- `email.mime`: For handling email MIME types.
- `pyodbc`: For connecting to SQL databases.
- `mysql.connector`: For connecting to MySQL databases.
- `pandas`: For data manipulation.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/DataRoutines.git
    cd DataRoutines
    ```

2. Install the required libraries:
    ```bash
    pip install tkinter cryptography smtplib pyodbc mysql-connector-python pandas
    ```

## Usage

1. Run the application:
    ```bash
    python DataRoutines.py
    ```

2. Follow the GUI instructions to set up queries, routines, recipients, and email settings.

## Files Overview

- `DataRoutines.py`: Main file to run the application.
- `RecipientManager.py`: Manages recipient emails.
- `QueryManager.py`: Manages database queries.
- `LogManager.py`: Manages logging activities.
- `encryption.py`: Handles encryption and decryption of credentials.



