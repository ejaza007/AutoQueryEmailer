from datetime import datetime

def ClearLog():
    open('Data/Logs.txt', 'w').close()


def Log(action):
    timestamp = datetime.now().strftime("[%d-%m-%Y %H:%M:%S] ")
    with open('Data/Logs.txt', 'a') as file:
        file.write(timestamp + action + '\n')

ClearLog()

