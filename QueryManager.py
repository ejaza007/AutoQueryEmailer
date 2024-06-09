#gets the stored queries
import LogManager


def get_query():
    with open('Routines/Queries.txt', 'r') as file:
        queries = [line.strip() for line in file.readlines()]
    return queries

#enables editing any stored queries, usefulness is questionable
def edit_query(old_query,edited_query):
    with open('Routines/Queries.txt', 'r') as file:
        queries = file.readlines()
        for index in range(len(queries)):
            if(queries[index].strip().__eq__(old_query)):
                queries[index] = edited_query + '\n'

#adds and stores new query to the query file
def add_query(insertion_query):
    with open('Routines/Queries.txt', 'r') as file:
        queries = file.readlines()

    exists = False
    for index in range(len(queries)):
        if(queries[index].strip().__eq__(insertion_query)):
            exists = True

    if(not exists):
        with open('Routines/Queries.txt', 'a') as file:
            file.write(insertion_query + '\n')
        print("SUCCESSFULLY ADDED '" + insertion_query + "' TO QUERY LIST")
    else:
        print("QUERY TO ADD ALREADY EXISTS '" + insertion_query + "'")

#removes a query from the query file
def remove_query(removal_query):
    with open('Routines/Queries.txt', 'r') as file:
        queries = file.readlines()

    removed = False
    for index in range(len(queries)):
        if(queries[index].strip().__eq__(removal_query)):
            del queries[index]
            removed = True
            with open('Routines/Queries.txt', 'w') as file:
                file.writelines(queries)
            break
    if(removed):
        LogManager.Log("SUCCESSFULLY REMOVED '" + removal_query + "' FROM QUERY LIST")
    else:
        LogManager.Log("QUERY TO REMOVE DOES NOT EXIST '" + removal_query + "'")

print(get_query())