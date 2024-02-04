from functions import *
import os

# Get the path to main file being executed
path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(path, "data")

print("Creating inverted index...")

# Create inverted index and list of document ids
inverted_index, all_document_ids_and_names = create_inverted_index_from_files(data_path)
list_of_document_ids = list(all_document_ids_and_names.keys())

# Get user input, run queries and print results
user_input(inverted_index, list_of_document_ids, all_document_ids_and_names)

exit()
