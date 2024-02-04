from functions import *
import os

# Get the path to main file being executed
path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(path, "data")

print("Creating inverted index...")

# Create inverted index and list of document ids
inverted_index, all_document_ids_and_names = create_inverted_index_from_files(data_path)
list_of_document_ids = list(all_document_ids_and_names.keys())

words1 = ["cat", "house" , "cards", "table"]
operations1 = ["OR", "AND", "OR"]

words2 = ["cat", "house" , "cards", "table"]
operations2 = ["AND", "AND", "AND"]

words3 = ["lion", "stood" , "thoughtfully", "moment"]
operations3 = ["OR", "OR", "OR"]

words4 = ["cat", "house" , "cards", "table"]
operations4 = ["AND"]

words5 = ["telephone", "paved" , "roads"]
operations5 = ["OR NOT", "AND NOT"]

number_of_matched_documents, total_number_of_comparisons, document_ids = run_query(words1, operations1, inverted_index, list_of_document_ids)
print_results(number_of_matched_documents, total_number_of_comparisons, document_ids, all_document_ids_and_names)

number_of_matched_documents, total_number_of_comparisons, document_ids = run_query(words2, operations2, inverted_index, list_of_document_ids)
print_results(number_of_matched_documents, total_number_of_comparisons, document_ids, all_document_ids_and_names)

number_of_matched_documents, total_number_of_comparisons, document_ids = run_query(words3, operations3, inverted_index, list_of_document_ids)
print_results(number_of_matched_documents, total_number_of_comparisons, document_ids, all_document_ids_and_names)

number_of_matched_documents, total_number_of_comparisons, document_ids = run_query(words4, operations4, inverted_index, list_of_document_ids)
print_results(number_of_matched_documents, total_number_of_comparisons, document_ids, all_document_ids_and_names)

number_of_matched_documents, total_number_of_comparisons, document_ids = run_query(words5, operations5, inverted_index, list_of_document_ids)
print_results(number_of_matched_documents, total_number_of_comparisons, document_ids, all_document_ids_and_names)

# Testing
# list1 = [1, 2, 3, 4, 5]
# list2 = [4, 5, 6, 7, 8]

# result, _ = union_or_not(list1, list2, list_of_document_ids)
# print("Union of", list1, "OR NOT", list2, "is", result, "\n")

# result, _ = intersection_and_not(list1, list2)
# print("Intersection of", list1, "AND NOT", list2, "is", result, "\n")

# result, _ = union(list1, list2)
# print("Union of", list1, "OR", list2, "is", result, "\n")

# result, _ = intersection(list1, list2)
# print("Intersection of", list1, "AND", list2, "is", result, "\n")

# Print out all the files that were used to create inverted index
# print_dictionary(all_document_ids_and_names)

# Print out all the files that were used to create inverted index
print_dictionary(all_document_ids_and_names)

