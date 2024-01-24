import nltk 
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download necessary NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def create_inverted_index_from_files(folder_path):

    files_unable_to_open = []

    # Initialize an empty inverted index dictionary
    inverted_index = {}

    # Initialize a set to store unique words across all files
    set_of_words = set()

    # Get the set of English stopwords from NLTK
    stop_words = set(stopwords.words('english'))

    # List all files in the specified folder
    list_of_files = os.listdir(folder_path)

    # Iterate through each file in the folder
    for i in range(len(list_of_files)):

        # Initialize variables to store word tokens
        word_tokens = []

        # empty the set of words
        set_of_words.clear()

        # Get the file extension
        _, extension = os.path.splitext(list_of_files[i])

        # Check if the file has a .txt extension
        if extension == ".txt":
            # Read the contents of the file and convert to lowercase
            file_contents = read_file(folder_path + "/" + list_of_files[i])
            
            # Check if file was able to be opened
            if file_contents != None:
    
                word_tokens = normalize_and_tokenize(file_contents)

                # print(word_tokens)

                # Iterate through each word token
                for word in word_tokens:
                    # Check if the word is not a stopword and has a length greater than 1
                    if word not in stop_words and len(word) > 1:
                        # Add the word to the set of unique words
                        set_of_words.add(word.lower())

                # Iterate through each word in the set of words
                for word in set_of_words:
                    # if the word is not in the inverted index, add it
                    if word not in inverted_index:
                        inverted_index[word] = []
                    
                    # append the document index to the list for that word
                    inverted_index[word].append(i)
                        
                # print(set_of_words)
            
            # If the file coudl not be opened, add it to a list
            else:
                files_unable_to_open.append(list_of_files[i])

    write_dictionary_to_file(inverted_index)      

    # Return the populated inverted index (for now, it's an empty dictionary)
    return list_of_files, inverted_index

# Function to keeping only alphanumeric characters and spaces and return a tokenized list of the words
def normalize_and_tokenize(text):

    normalized_text = ""

    # Normalize the file contents by keeping only alphanumeric characters and spaces
    for character in text:
        if character.isalnum() or character == " ":
            normalized_text += character

        # replace all the \n and \r with regular spaces
        elif character == "\n" or character == "\r":
            normalized_text += " "

    # Tokenize the normalized file contents into words
    text_tokenized = word_tokenize(normalized_text)

    return text_tokenized


def read_file(file_path):

    try:

        # Attempt to open the file at the specified file_path in read mode ('r')
        with open(file_path, 'r', encoding="utf-8", errors='ignore') as file:
            
            # Read the contents of the file
            contents = file.read()

        # Return the contents of the file
        return contents
    
    except FileNotFoundError:

        # Handle the case where the specified file is not found
        print(f"Error with file {file_path}: File not found at path '{file_path}'")

        return None
    
    except Exception as e:

        # Handle other exceptions
        print(f"Error with file {file_path}: {e}")

        return None

def write_dictionary_to_file(dictionary):
    with open("dictionary.txt", 'w', encoding="utf-8") as f:  
        for key, value in dictionary.items():  
            f.write(f"{key}:{value}\n")

def print_dictionary(dictionary):
    print("{")
    for key, value in dictionary.items():
        print(f"    '{key}': {value},")
    print("}")