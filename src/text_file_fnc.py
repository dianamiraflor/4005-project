import os
from pathlib import Path

def list_to_text_file(directory, filename, list):
    dir = Path(directory)
    
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    file = open(dir / filename, 'w')
    for x in list:
        file.write(str(x)+"\n")

    file.close()
