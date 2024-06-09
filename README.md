# DataRoutines
A database query and email manager, made specifically for setting up routine queries to automate the execution of queries and the emailing of data to recipients.

# Features
Navigate the self explanatory GUI \
Set up Queries to Run on demand and save the result\
Set up Routines to Run at a appointed time and save the result\
Set up Recipient emails to send Data\
Set up Email attachments\
Send Bulk Emails to all selected Recipients\
Utilize both SQL and Windows Authentication for Database Connection\
Save Encryped Credentials for Senders Email\
Save Encrypted Credentials for both SQL Connnection methods\
Save Recipient emails as plaintext\
Utilize Multithreading in order to avoid freezing the program while querying data from database\
Utilize Multithreading to send emails in parrallel to speed up the overall process

# Libraries utilized
tkinter\
threading\
cryptography.fernet\
smtplib\
email.mime\
pyodbc\
mysql.connector\
pandas




