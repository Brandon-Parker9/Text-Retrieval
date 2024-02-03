import nltk 
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download necessary NLTK resources in quiet mode so it doesn't print status to console
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def create_inverted_index_from_files(folder_path):

    # List of file names that were unable to be opened
    files_unable_to_open = []

    # Dictionary of the document ids and their file names
    all_document_ids_and_names = {}

    # Initialize an empty inverted index dictionary
    inverted_index = {}

    # Initialize a set to store unique words across all files
    set_of_words = set()

    # Get the set of English stop words from NLTK
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

            # Add document id and name to the dictionary
            all_document_ids_and_names[i] = list_of_files[i]

            # Read the contents of the file and convert to lowercase
            file_contents = read_file(folder_path + "/" + list_of_files[i])
            
            # Check if file was able to be opened
            if file_contents != None:
    
                word_tokens = normalize_and_tokenize(file_contents)

                # Iterate through each word token
                for word in word_tokens:
                    # Check if the word is not a stop word and has a length greater than 1
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
                                    
            # If the file could not be opened, add it to a list
            else:
                files_unable_to_open.append(list_of_files[i])

    write_dictionary_to_file(inverted_index)      


    return inverted_index, all_document_ids_and_names

def normalize_and_tokenize(text):
    # Function to keeping only alphanumeric characters and spaces and return a tokenized list of the words

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

def user_input(inverted_index, list_of_document_ids, all_document_ids_and_names):

    while True:
        
        # Ask the user to input the number of queries
        num_queries_input = input("Enter the number of queries you would like to preform: ")

        # Check if the input is a non-empty string and consists only of digits
        if num_queries_input.isdigit():

            # Convert the input to an integer and break out of the loop
            num_queries = int(num_queries_input)
            break

        else:

            # If the input is not a valid number, display an error message and continue the loop
            print("Invalid input. Please enter a valid number.")

    for i in range(num_queries):

        #  Get user input sentence
        input_sentence = input("Input sentence: ")

        # Normalize and tokenize the input sentence
        words = normalize_and_tokenize(input_sentence)

        # get user desired operations
        input_operation_sequence = input("Input operation Sequence: ")

        operators = []
        
        # This is the part where we need to add the user filtering to get the operations
        # One filter we can't forget about is that the sentence and the operator cant be empty

        # Dont ask me lmao i asked chatgpt to make this ascii art as a place 
        # holder to know this code needs to be written

        #     ,ggggggggggg,                                                                
        # dP"""88""""""Y8,                   ,dPYb,                                    I8     
        # Yb,  88      `8b                   IP'`Yb                                    I8     
        # `"  88      ,8P     ,ggggg,        I8  8I   gg    gg    ,gggg,gg   ,gggggg,   I8     
        #     88aaaad8P"     dP"  "Y8gg,     I8  8'   I8    8I   dP"  "Y8I   dP""""8I   I8     
        #     88""""Yb,      i8'    ,8I     ,I8 dP    I8    8'  i8'    ,8I  ,8'    8I  ,I8,    
        #     88     "8i     ,d8,   ,d8'    ,d8IP     `8,  ,8' ,d8,   ,d8b,,dP     Y8,,d88b,   
        #     88      `8i   P"Y8888P"     ,d8I8'      `Y88P'  P"Y8888P"`Y88P      `Y88P""Y888  
        #     88       Yb,                                                          ,d8I'      
        #     88        Y8,                                                        ,dP'8I       
        #     88         Y8                                                        ,8"  8I       
        #     88         `8b                                                       dP'  8I       
        #     ,88P          `8                                                       8"   8I       
        # 8P'                                                               d8b,   Yb, d8I       
        # d8                                                               `Y88P'    "Y88P"        
        # ,8P'    

        # Used for testing purposes
        # print(f"Number input: {num_queries} \n Input sentence: {input_sentence} \n Input Operation Sequence: {input_operation_sequence}")                                                                                   

        # Print out expected preprocessed query
        # NEEDS TO BE COMPLETED

        # Run query with user input   
        number_of_matched_documents, total_number_of_comparisons, document_ids = run_query(words, operators, inverted_index, list_of_document_ids)
        
        # Print out results of query
        print_results(number_of_matched_documents, total_number_of_comparisons, document_ids, all_document_ids_and_names)

    return None

def run_query(words, operators, inverted_index, all_document_ids):
    
    document_ids = []  # List to store the document ids that match the query
    num_of_operators = len(operators) - 1
    total_number_of_comparisons = 0

    # Iterate over the words in the query
    for i in range(len(words) - 1):

        # Get the current word and the next word
        word1 = words[i]
        word2 = words[i + 1]

        if i == 0:

            if word1 in inverted_index:
                
                # Get the first list based on the first word if i = 0
                list1 = inverted_index[word1]
            
            else:

                # Set list1 to an empty list as the word was not in any files
                list1 = []
            
        else:
            
            # Make the first list the list made from previous operations if i > 0
            list1 = document_ids
        
        if word2 in inverted_index:
                
            # Get second list of document ids based on the i + 1 word
            list2 = inverted_index[word2]
            
        else:

            # Set list2 to an empty list as the word was not in any files
            list2 = []
      

        # Get the operator for the current pair of words
        operator = operators[min(i, num_of_operators)]

        # Initialize comparison count for each pair of words
        comparison_count = 0

        # Perform operations based on the operator
        if operator == "OR":

            # Perform union operation
            document_ids, comparison_count = union(list1, list2)

        elif operator == "AND":

            # Perform intersection operation
            document_ids, comparison_count = intersection(list1, list2)

        elif operator == "AND NOT":

            # Perform intersection and not operation
            document_ids, comparison_count = intersection_and_not(list1, list2)

        elif operator == "OR NOT":

            # Perform union and not operation
            document_ids, comparison_count = union_or_not(list1, list2, all_document_ids)

        else:

            # Handle invalid operator
            print("Invalid operation")
        
        # Update total number of comparisons
        total_number_of_comparisons += comparison_count

    # Calculate the number of matched documents
    number_of_matched_documents = len(document_ids)

    return number_of_matched_documents, total_number_of_comparisons, document_ids

def print_results(number_of_matched_documents, total_number_of_comparisons, document_ids, all_document_ids_and_names):
    
    print(f"Number of matched documents: {number_of_matched_documents}")
    print(f"Minimum number of comparisons required: {total_number_of_comparisons}")
    print("List of retrieved document names: ")

    for id in document_ids:
        print(f" - ID: {id} Name: {all_document_ids_and_names[id]}")

    # Print a new line
    print()

def intersection(list1, list2):

    # Initialize the count of comparisons
    comparison_count = 0

    # Initialize an empty list to store the intersection elements
    intersection_list = []

    # Iterate over each element in the first list
    for element in list1:

        # Check if the element is also present in the second list and not already in the intersection list
        if element in list2 and element not in intersection_list:
            # If the element satisfies both conditions, add it to the intersection list
            intersection_list.append(element)

        # Increment the number of comparisons
        comparison_count += 1

    # Return the intersection list
    return intersection_list, comparison_count

def intersection_and_not(list1, list2):

    # Initialize the count of comparisons
    comparison_count = 0
    
    # Initialize an empty list to store the intersection elements
    intersection_and_not_list = []

    # Iterate over elements in list1
    for element in list1:

        # Check if element is in list2
        if element not in list2:
            intersection_and_not_list.append(element)

        # Increment the number of comparisons
        comparison_count += 1

    return intersection_and_not_list, comparison_count

def union(list1, list2):

    # Initialize the count of comparisons
    comparison_count = 0

    # Initialize an empty list to store the union elements
    union_list = []

    # Add all elements from list1 to the union list
    union_list.extend(list1)

    # Iterate over each element in list2
    for element in list2:

        # If the element is not already in the union list, add it
        if element not in union_list:
            union_list.append(element)

        # Increment the number of comparisons
        comparison_count += 1

    # Return the union list
    return union_list, comparison_count

def union_or_not(list1, list2, full_list):

    # Initialize the count of comparisons
    comparison_count = 0
    
    # Initialize an empty list to store the union elements
    union_or_not_list = []

    # Add all elements from list1
    union_or_not_list.extend(list1)

    # Temp array full of all document ids
    temp_all_document_ids = []
    temp_all_document_ids.extend(full_list)

    # Iterate over elements in list2
    for element in list2:

        # Remove element from result_list if it exists
        if element in full_list:
            temp_all_document_ids.remove(element)

        # Increment the number of comparisons
        comparison_count += 1

    union_or_not_list, comp_count = union(union_or_not_list, temp_all_document_ids)

    comparison_count += comp_count

    return union_or_not_list, comparison_count

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

    # Open a file named "dictionary.txt" in write mode ('w') with UTF-8 encoding
    with open("dictionary.txt", 'w', encoding="utf-8") as f:

        # Iterate through key-value pairs in the dictionary
        for key, value in dictionary.items():

            # Write each key-value pair to the file with a newline character
            f.write(f"{key}:{value}\n")

def print_dictionary(dictionary):

    # Print the opening curly brace for the dictionary
    print("{")
    
    # Iterate through key-value pairs in the dictionary
    for key, value in dictionary.items():

        # Print each key-value pair with proper indentation
        print(f"    '{key}': {value},")
    
    # Print the closing curly brace for the dictionary
    print("}")

def print_list_with_commas(list_to_print):

    for i in range(len(list_to_print)):

        print(list_to_print[i], end="")

        # Add a comma if it's not the last element
        if i < len(list_to_print) - 1:
            print(", ", end="")

    print()  # Print a newline at the end

    return None
