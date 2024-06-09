import pyodbc
import mysql.connector
import pandas as pd
import Encryption
import LogManager


#Execute a query and return the data as data frame
def Run_Query(cursor,Query):
    try:
        cursor.execute(Query)
    except pyodbc.ProgrammingError as E:
        print(E)
    desc = []  # the column names
    full_data = []  # the entire data
    for i in cursor.description:
        desc.append(i[0])  # getting column names
        full_data.append([i[0]])  # for data structure, values removed later

    # get data and parse correctly for Excel file to avoid warnings
    data = cursor.fetchone()
    while data:
        for i in range(len(data)):
            try:
                data[i] = float(data[i])
            except ValueError as E:
                data[i] = str(data[i])
            full_data[i].append(data[i])
        data = cursor.fetchone()

    # remove the column names from data entry
    for i in full_data:
        i.pop(0)

    # Convert data to a DataFrame
    df = pd.DataFrame(full_data)
    df = df.T
    df.columns = desc
    LogManager.Log("RAN DATABASE QUERY: "+Query)
    return df

#executes query using SQL authentication and exports a excel file with its data
def query_to_excel_sql(query):
    user, password, hostname, database = Encryption.read_database_credentials()
    cnx = mysql.connector.connect(
        host=hostname,
        user=user,
        password=password,
        database=database
    )
    cursor = cnx.cursor()
    LogManager.Log("CONNECTED TO DATABASE USING SQL AUTHENTICATION")
    df = Run_Query(cursor, query)
    file_path = 'data.xlsx'
    df.to_excel(file_path, index=False)
    LogManager("FILE " + file_path + " CREATED")
    cnx.close()
    LogManager.Log("DISCONNECTED FROM DATABASE")

#selects which database authentication to use and executes the query using it
def query_to_excel(query):
    if(bool(get_type()=="0")):
        query_to_excel_sql(query)
    else:
        query_to_excel_win(query)

#executes query using windows authentication and exports a excel file with its data
def query_to_excel_win(query):
    LogManager.Log("CONNECTED TO DATABASE USING WINDOWS AUTHENTICATION")
    cnxn = pyodbc.connect(Encryption.generate_win_string())
    cursor = cnxn.cursor()
    df = Run_Query(cursor,query)
    file_path = 'data.xlsx'
    df.to_excel(file_path, index=False)
    LogManager("FILE " + file_path + " CREATED")
    cnxn.close()
    LogManager.Log("DISCONNECTED FROM DATABASE")

#sets which type of authentication to use SQL/Windows
def set_type(val):
    with open('Data/DbType.txt', 'w') as file:
        file.write(str(val))

#gets which type of authentication is selected
def get_type():
    with open('Data/DbType.txt', 'r') as file:
        return file.read()

#toggles between the two authentication types
def toggle_type():
    val = ""
    with open('Data/DbType.txt', 'r') as file:
        val = file.read()
    val = int(not int(val))
    with open('Data/DbType.txt', 'w') as file:
        file.write(str(val))
    if bool(get_type()=="0"):
        LogManager.Log("TOGGLED DATABASE AUTHENTICATION TO SQL AUTHENTICATION")
    else:
        LogManager.Log("TOGGLED DATABASE AUTHENTICATION TO WINDOWS AUTHENTICATION")

toggle_type()
print(get_type())

# connect to database
#r'Driver=SQL Server;Server=DESKTOP-R7V59HM;Database=Demo;Trusted_Connection=yes;'
#cnxn = pyodbc.connect(Encryption.generate_win_string())
#cursor = cnxn.cursor()
#print("Connected to Database")

#df = Run_Query("select * from production.products")

# Save DataFrame to Excel file
#file_path = 'data.xlsx'
#df.to_excel(file_path, index=False)

#cnxn.close()
#print("Disconnected from Database")
