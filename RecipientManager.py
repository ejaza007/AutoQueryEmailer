import LogManager


def debug_get_recipients():
    with open('Data/Recipients.txt', 'r') as file:
        emails = file.readlines()
    return emails

def get_emails():
    with open('Data/Recipients.txt', 'r') as file:
        emails = [line.strip() for line in file.readlines()]
    return emails

def add_recipient(insertion_email):
    with open('Data/Recipients.txt', 'r') as file:
        emails = file.readlines()

    exists = False
    for index in range(len(emails)):
        if(emails[index].strip().__eq__(insertion_email)):
            exists = True

    if(not exists):
        with open('Data/Recipients.txt', 'a') as file:
            file.write(insertion_email+'\n')
        LogManager.Log("SUCCESFULLY ADDED '"+ insertion_email + "' TO RECIPIENT LIST")
    else:
        LogManager.Log("EMAIL TO ADD TO RECIPIENT LIST ALREADY EXISTS '" + insertion_email + "'")


def remove_recipient(removal_email):
    with open('Data/Recipients.txt', 'r') as file:
        emails = file.readlines()

    removed = False
    for index in range(len(emails)):
        if(emails[index].strip().__eq__(removal_email)):
            del emails[index]
            removed = True
            with open('Data/Recipients.txt', 'w') as file:
                file.writelines(emails)
            break
    if(removed):
        LogManager.Log("SUCCESSFULLY REMOVED '" + removal_email + "' FROM RECIPIENT LIST")
    else:
        LogManager.Log("EMAIL TO REMOVE FROM RECIPIENT LIST DOES NOT EXIST '" + removal_email + "'")
