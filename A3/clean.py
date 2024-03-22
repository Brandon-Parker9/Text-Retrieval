import os

def clean_files():
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "output")
    
    for file in os.listdir(path):
        if file != ".gitkeep":
            os.remove(os.path.join(path, file))
    
# Call the function to delete files in the directory
clean_files()