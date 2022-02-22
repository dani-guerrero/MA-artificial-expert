import os

def log(text):
    logfile = open('error.log', 'a+')
    print(text, file=logfile)
    logfile.close()

