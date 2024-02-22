import nltk 
import os
import re
import math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download necessary NLTK resources in quiet mode so it doesn't print status to console
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Constants
OPERATORS = ["AND", "OR", "NOT"]

class TermFrequency:

    NUM_OF_FUNCTIONS = 5

    BINARY = 0
    RAW_COUNT = 1
    TF = 2
    LOG_NORMALIZATION = 3
    DOUBLE_NORMALIZATION = 4

    def binary(term_count):

        result = 0

        if term_count > 0:
            result = 1

        return result
    
    def raw_count(term_count):

        result = 0

        if term_count > 0:
            result = term_count

        return result
    
    def tf(term_count, total_words):

        result = 0

        if term_count > 0:
            result = round(term_count/(total_words - term_count), 2)

        return result
    
    def log_normalization(term_count):

        result = 0

        if term_count > 0:
            result = round(math.log(1 + term_count), 2)

        return result
    
    def double_normalization(term_count, most_freq_word_count):

        result = 0

        if term_count > 0:
            result = round(0.5 + 0.5 * (term_count/most_freq_word_count), 2)

        return result

def create_positional_index_from_files(folder_path):

    # List of file names that were unable to be opened
    files_unable_to_open = []

    # Dictionary of the document ids and their file names
    all_document_ids_and_names = {}

    # Initialize an empty positional index dictionary
    positional_index = {}

    # Initialize a list of words
    list_of_words = []

    # Get the set of English stop words from NLTK
    stop_words = set(stopwords.words('english'))

    # List all files in the specified folder
    list_of_files = os.listdir(folder_path)

    # Iterate through each file in the folder
    for i in range(len(list_of_files)):

        # Initialize variables to store word tokens
        word_tokens = []

        # empty the list of words
        list_of_words.clear()

        # Get the file extension
        _, extension = os.path.splitext(list_of_files[i])

        # Check if the file has a .txt extension
        if extension == ".txt":

            # Add document id, name, length, most frequent word and most frequent word count to the dictionary
            all_document_ids_and_names[i] = {"name" : list_of_files[i], "length" : 0, "most_freq_word" : "", "most_freq_word_count" : 0, "second_most_freq_word" : "", "second_most_freq_word_count" : 0}

            # Read the contents of the file and convert to lowercase
            file_contents = read_file(folder_path + "/" + list_of_files[i])
            
            # Check if file was able to be opened
            if file_contents != None:
    
                word_tokens = normalize_and_tokenize(file_contents)

                all_document_ids_and_names[i]["length"] = len(word_tokens)

                # Iterate through each word token
                for word in word_tokens:

                    # Check if the word is not a stop word and has a length greater than 1
                    if word.lower() not in stop_words and len(word) > 1:

                        # Add the word to the set of unique words
                        list_of_words.append(word.lower())

                # Iterate through each word in the set of words
                for pos in range(len(list_of_words)):

                    word = list_of_words[pos]

                    # if the word is not in the positional index, add it
                    if word not in positional_index:
                        positional_index[word] = {}

                    # add the document index to the list for that word if it doesn't exist
                    if i not in positional_index[word]:
                         positional_index[word][i] = []
                    
                    # append the word position for that document
                    positional_index[word][i].append(pos)

                # Iterate through each word in list_of_words
                for word in list_of_words:

                    # update the most frequent word and its count
                    if len(positional_index[word][i]) >= all_document_ids_and_names[i]["most_freq_word_count"]:

                        all_document_ids_and_names[i]["most_freq_word"] = word
                        all_document_ids_and_names[i]["most_freq_word_count"] = len(positional_index[word][i])
                                    
                    # update the second most frequent word and its count
                    if len(positional_index[word][i]) >= all_document_ids_and_names[i]["second_most_freq_word_count"] and len(positional_index[word][i]) < all_document_ids_and_names[i]["most_freq_word_count"]:

                        all_document_ids_and_names[i]["second_most_freq_word"] = word
                        all_document_ids_and_names[i]["second_most_freq_word_count"] = len(positional_index[word][i])

            # If the file could not be opened, add it to a list
            else:
                files_unable_to_open.append(list_of_files[i])

    write_dictionary_to_file(positional_index)      

    return positional_index, all_document_ids_and_names

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

def search_phrase_query(query_terms, positional_index, proximity=5):

    # Retrieve positional information for each term in the phrase query
    positional_info = []
    for term in query_terms:
        if term in positional_index:
            positional_info.append(positional_index[term])

    # Initialize a list to store the final matching documents
    matching_documents = []

    # If the number of query terms doesn't match the terms retrieved from positional index
    # then the phrase cannot exist as all the words are on in the index
    if (len(positional_info) == len(query_terms)):

        # Iterate over positions of the first term in the document
        for doc_id in positional_info[0]:
            positions_first_term = positional_info[0][doc_id]

            # Check proximity for each position of the first term
            for pos_first_term in positions_first_term:
                found = True
                curr_pos = pos_first_term

                # Check proximity for each subsequent term
                for i in range(1, len(query_terms)):

                    next_term_info = positional_info[i].get(doc_id, [])
                    term_found = False

                    # Check if the next term exists within the specified proximity of the current term
                    for pos_next_term in next_term_info:
                        if (pos_next_term - curr_pos) <= proximity and (pos_next_term - curr_pos) >= 0:
                            term_found = True
                            curr_pos = pos_next_term
                            break

                    if not term_found:
                        found = False
                        break

                if found:
                    matching_documents.append(doc_id)
                    break

    return matching_documents

def generate_TF_IDF_matrices(positional_index, all_document_ids_and_names):

    # Get the number of documents and words in the index
    num_of_documents = len(all_document_ids_and_names)
    num_of_words_in_index = len(positional_index)

    # Initialize a list to store TF-IDF matrices
    TF_IDF_matrices = []

    # Populate the array with 5 2D arrays filled with zeros
    for _ in range(TermFrequency.NUM_OF_FUNCTIONS):

        # Initialize a 2D array with zeros
        array_2d = []

        for _ in range(num_of_documents):

            # Initialize each row with zeros
            row = [0] * num_of_words_in_index
            array_2d.append(row)

        TF_IDF_matrices.append(array_2d)

    # Get the keys of the positional index
    word_key_list = list(positional_index.keys())

    # Iterate through each word in the positional index
    for word_index in range(num_of_words_in_index):

        word = word_key_list[word_index]
        
        # Calculate IDF value for the current word
        IDF_value = round(math.log(num_of_documents/(len(positional_index[word]) + 1)), 2)

        # Iterate through each document containing the current word
        for doc_id in positional_index[word]:

            # Calculate TF-IDF values for different term frequency methods
            TF_IDF_matrices[TermFrequency.BINARY][doc_id][word_index] = TermFrequency.binary(len(positional_index[word][doc_id])) * IDF_value
            TF_IDF_matrices[TermFrequency.RAW_COUNT][doc_id][word_index] = TermFrequency.raw_count(len(positional_index[word][doc_id])) * IDF_value
            TF_IDF_matrices[TermFrequency.TF][doc_id][word_index] = TermFrequency.tf(len(positional_index[word][doc_id]), all_document_ids_and_names[doc_id]['length']) * IDF_value
            TF_IDF_matrices[TermFrequency.LOG_NORMALIZATION][doc_id][word_index] = TermFrequency.log_normalization(len(positional_index[word][doc_id])) * IDF_value
            
            # Determine the count of the most frequent word excluding the current term
            most_freq_not_current_term_count= all_document_ids_and_names[doc_id]['most_freq_word_count']

            # Update count if the current term is the most frequent word
            if (word == all_document_ids_and_names[doc_id]['most_freq_word']):
                most_freq_not_current_term_count = all_document_ids_and_names[doc_id]['second_most_freq_word_count']

            # Calculate TF-IDF value for double normalization method
            TF_IDF_matrices[TermFrequency.DOUBLE_NORMALIZATION][doc_id][word_index] = TermFrequency.double_normalization(len(positional_index[word][doc_id]), most_freq_not_current_term_count) * IDF_value        
    
    return TF_IDF_matrices

def generate_query_vector(query_terms, positional_index):

    # Initialize the query vector
    query_vector = []

    # Get the keys of the positional index
    word_key_list = list(positional_index.keys())

    # Initialize the query vector with zeros
    for _ in range(len(positional_index)):
        query_vector.append(0)

    # Iterate through each term in the query terms
    for term in query_terms:

        # Check if the term is in the positional index
        if term in positional_index:

            # Get the index of the term in the word key list
            index = word_key_list.index(term)

            # Set the corresponding element in the query vector to 1
            query_vector[index] = 1

    return query_vector

def rank_documents_by_TF_IDF(matching_document_ids, query_vector, positional_index, all_document_ids_and_names):

    # Generate TF-IDF matrices
    TF_IDF_matrices = generate_TF_IDF_matrices(positional_index, all_document_ids_and_names)

    # Initialize the results dictionary
    results = {'matching_document_ids' : matching_document_ids}

    # Iterate through matching document IDs
    for matched_id in matching_document_ids:

        # Initialize sub-dictionary for the current document
        results[matched_id] = {}
        
        # Calculate dot product of query vector with TF-IDF vectors for different term frequency methods
        results[matched_id][TermFrequency.BINARY] = dot_product(query_vector, TF_IDF_matrices[TermFrequency.BINARY][matched_id])
        results[matched_id][TermFrequency.RAW_COUNT] = dot_product(query_vector, TF_IDF_matrices[TermFrequency.RAW_COUNT][matched_id])
        results[matched_id][TermFrequency.TF] = dot_product(query_vector, TF_IDF_matrices[TermFrequency.TF][matched_id])
        results[matched_id][TermFrequency.LOG_NORMALIZATION] = dot_product(query_vector, TF_IDF_matrices[TermFrequency.LOG_NORMALIZATION][matched_id])
        results[matched_id][TermFrequency.DOUBLE_NORMALIZATION] = dot_product(query_vector, TF_IDF_matrices[TermFrequency.DOUBLE_NORMALIZATION][matched_id])

    return results

def dot_product(vector1, vector2):

    # Ensure both vectors have the same length
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have the same length.")

    # Initialize the dot product to zero
    dot_product = 0

    # Iterate through corresponding elements of the vectors
    for i in range(len(vector1)):
        # Accumulate the product of corresponding elements
        dot_product += vector1[i] * vector2[i]

    return round(dot_product, 2)

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

def remove_stop_words_from_user_query(words):

    set_of_words = []

    # Get the set of English stop words from NLTK
    stop_words = set(stopwords.words('english'))

    # Iterate through each word token
    for word in words:

        # Check if the word is not a stop word and has a length greater than 1
        if word not in stop_words and len(word) > 1:
            
            # Check if the word is a duplicate
            if word not in set_of_words:
                set_of_words.append(word)

    return set_of_words

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

def user_input(positional_index, all_document_ids_and_names):

    while True:

        phrase_query = input("Enter the phrase query you would like to search for (max 5 words): ")
        
        # Tokenize the phrase query and count the number of words
        num_words = len(phrase_query.split())
        if num_words > 5:

            print("Error: Maximum of 5 words allowed. Please try again.")
        else:
            break

     # Tokenize and normalize the phrase query
    query_terms = normalize_and_tokenize(phrase_query)

    # Remove stop words from the phrase query
    query_terms = remove_stop_words_from_user_query(query_terms)

    # Search for matching document IDs based on the phrase query
    matching_document_ids = search_phrase_query(query_terms, positional_index)
    print_results_without_ranks(matching_document_ids, all_document_ids_and_names)

    # Generate the query vector based on the query terms and positional index
    query_vector = generate_query_vector(query_terms, positional_index)

    # Rank the search results by TF-IDF scores
    rank_results = rank_documents_by_TF_IDF(matching_document_ids, query_vector, positional_index, all_document_ids_and_names)

    # Print the ranked search results
    print_results_with_ranks(rank_results, all_document_ids_and_names)

    return None

def print_results_with_ranks(rank_results, all_document_ids_and_names):
    
    print("\nBinary Rankings: ")
    for matched_id in rank_results["matching_document_ids"]:
        print(f" - ID: {matched_id:3} Name: {all_document_ids_and_names[matched_id]['name']:15} Rank: {rank_results[matched_id][TermFrequency.BINARY]:6} ")

    print("\nRaw Count Rankings: ")
    for matched_id in rank_results["matching_document_ids"]:
        print(f" - ID: {matched_id:3} Name: {all_document_ids_and_names[matched_id]['name']:15} Rank: {rank_results[matched_id][TermFrequency.RAW_COUNT]:6} ")

    print("\nTerm Frequency Rankings: ")
    for matched_id in rank_results["matching_document_ids"]:
        print(f" - ID: {matched_id:3} Name: {all_document_ids_and_names[matched_id]['name']:15} Rank: {rank_results[matched_id][TermFrequency.TF]:6} ")

    print("\nLog Normalization Rankings: ")
    for matched_id in rank_results["matching_document_ids"]:
        print(f" - ID: {matched_id:3} Name: {all_document_ids_and_names[matched_id]['name']:15} Rank: {rank_results[matched_id][TermFrequency.LOG_NORMALIZATION]:6} ")

    print("\nDouble Normalization Rankings: ")
    for matched_id in rank_results["matching_document_ids"]:
        print(f" - ID: {matched_id:3} Name: {all_document_ids_and_names[matched_id]['name']:15} Rank: {rank_results[matched_id][TermFrequency.DOUBLE_NORMALIZATION]:6} ")

    return None

def print_results_without_ranks(matching_document_ids, all_document_ids_and_names):
    
    print("\nList of matched document names NOT RANKED: ")

    for matched_id in matching_document_ids:
        print(f" - ID: {matched_id:3} Name: {all_document_ids_and_names[matched_id]['name']:15}")

    return None
