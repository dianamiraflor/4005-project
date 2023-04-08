import os
from pathlib import Path
import json

def list_to_text_file(directory, filename, list):
    dir = Path(directory)
    
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    file = open(dir / filename, 'w')
    for x in list:
        file.write(str(x)+"\n")

    file.close()

def dict_to_text_file(directory, filename, dict):
    dir = Path(directory)
    
    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(dir / filename, "w") as outfile:
        json.dump(dict, outfile)