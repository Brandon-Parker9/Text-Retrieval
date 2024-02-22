from functions import *
import os

# Get the path to main file being executed
path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(path, "data_small")

print("Creating positional index...")

# Create positional index and list of document ids
positional_index, all_document_ids_and_names = create_positional_index_from_files(data_path)

print_dictionary(all_document_ids_and_names)

generate_TF_IDF_matrices(positional_index, all_document_ids_and_names)

# Get user input, run queries and print results
# user_input(positional_index, all_document_ids_and_names)

exit()