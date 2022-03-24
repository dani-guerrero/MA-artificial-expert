def log(text):
    with open('error.log', 'a+') as logfile:
        print(text, file=logfile)

