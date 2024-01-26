from functions import *

list_of_files, invereted_index, all_document_ids = create_inverted_index_from_files("./data_small")

# # user_input()

# words1 = ["cat", "house" , "cards", "table"]
# operations1 = ["OR", "AND", "OR"]

# words2 = ["cat", "house" , "cards", "table"]
# operations2 = ["AND", "AND", "AND"]

# words3 = ["lion", "stood" , "thoughtfully", "moment"]
# operations3 = ["OR", "OR", "OR"]

# words4 = ["cat", "house" , "cards", "table"]
# operations4 = ["AND"]

# words5 = ["telephone", "paved" , "roads"]
# operations4 = ["OR NOT", "AND NOT"]

# number_of_matched_documents, total_number_of_comparisons, document_list = run_query(words1, operations1, invereted_index, all_document_ids)
# number_of_matched_documents, total_number_of_comparisons, document_list = run_query(words2, operations2, invereted_index, all_document_ids)
# number_of_matched_documents, total_number_of_comparisons, document_list = run_query(words3, operations3, invereted_index, all_document_ids)
# number_of_matched_documents, total_number_of_comparisons, document_list = run_query(words4, operations4, invereted_index, all_document_ids)
# number_of_matched_documents, total_number_of_comparisons, document_list = run_query(words5, operations5, invereted_index, all_document_ids)

# Testing
list1 = [1, 2, 3, 4, 5]
list2 = [4, 5, 6, 7, 8]

result, _ = union_or_not(list1, list2, all_document_ids)
print("Union of", list1, "OR NOT", list2, "is", result, "\n")

result, _ = intersection_and_not(list1, list2)
print("Intersection of", list1, "AND NOT", list2, "is", result, "\n")

result, _ = union(list1, list2)
print("Union of", list1, "OR", list2, "is", result, "\n")

result, _ = intersection(list1, list2)
print("Intersection of", list1, "AND", list2, "is", result, "\n")

print("UNION DOES NOT INSERT IN SORTED ORDER!!!!!!!!  Must fix lolol\n")

