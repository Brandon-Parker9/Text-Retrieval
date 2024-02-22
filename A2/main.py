from functions import *
import os

# Get the path to main file being executed
path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(path, "data_small")

print("Creating positional index...")

# Create positional index and list of document ids
positional_index, all_document_ids_and_names = create_positional_index_from_files(data_path)
list_of_document_ids = list(all_document_ids_and_names.keys())

# phrase_query = "abyss steep wall"
# phrase_query = "abyss anyone"
# phrase_query = "abyss wall anyone"
# phrase_query = "abyss wall ever"
phrase_query = "abyss wall molten"
matching_documents = search_phrase_query(phrase_query, positional_index)


print_dictionary(all_document_ids_and_names)
print_list_with_commas(matching_documents)

# Get user input, run queries and print results
# user_input(positional_index, list_of_document_ids, all_document_ids_and_names)

exit()