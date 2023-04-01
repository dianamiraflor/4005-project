import os

def list_to_text_file(directory, filename, list):
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    file = open(directory + filename, 'w')
    for x in list:
        file.write(str(x)+"\n")

    file.close()
