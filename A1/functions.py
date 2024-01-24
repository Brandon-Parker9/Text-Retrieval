import nltk 
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

def create_inverted_index_from_files(folder_path):
    # Initialize an empty inverted index dictionary
    inverted_index = {}
    
    # Initialize a set to store unique words across all files
    set_of_words = set()

    # Get the set of English stopwords from NLTK
    stop_words = set(stopwords.words('english'))

    # List all files in the specified folder
    files = os.listdir(folder_path)

    # Iterate through each file in the folder
    for file in files:
        # Initialize variables to store normalized file contents and word tokens
        normalized_file_contents = ""
        word_tokens = []

        # Get the file extension
        _, extension = os.path.splitext(file)

        # Check if the file has a .txt extension
        if extension == ".txt":
            # Read the contents of the file and convert to lowercase
            file_contents = read_file(folder_path + "/" + file).lower()

            # Normalize the file contents by keeping only alphanumeric characters and spaces
            for character in file_contents:
                if character.isalnum() or character == " ":
                    normalized_file_contents += character

            # Tokenize the normalized file contents into words
            word_tokens = word_tokenize(normalized_file_contents)

            # Iterate through each word token
            for word in word_tokens:
                # Check if the word is not a stopword and has a non-zero length
                if word not in stop_words and len(word) != 0:
                    # Add the word to the set of unique words
                    set_of_words.add(word)

    # Return the populated inverted index (for now, it's an empty dictionary)
    return inverted_index



def read_file(file_path):
    try:
        # Attempt to open the file at the specified file_path in read mode ('r')
        with open(file_path, 'r') as file:

            # Read the contents of the file
            contents = file.read()

        # Return the contents of the file
        return contents
    
    except FileNotFoundError:

        # Handle the case where the specified file is not found
        print(f"Error: File not found at path '{file_path}'")

        return None
    
    except Exception as e:

        # Handle other exceptions
        print(f"Error: {e}")

        return None