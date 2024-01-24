# Text Retrieval System

## Introduction

This project implements a Text Retrieval System that performs various preprocessing steps on a given dataset, builds an inverted index, supports queries, and evaluates the system's performance against provided queries.

## Requirements

- Python 3.x
- NLTK (Natural Language Toolkit)

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/text-retrieval-system.git
    cd text-retrieval-system
    ```

2. Install the required dependencies:

    ```bash
    pip install nltk
    ```

3. Run the system:

    ```bash
    python main.py
    ```

## Project Structure

- `main.py`: Entry point of the system.
- `functions.py`: Contains functions for text preprocessing, Implements the inverted index data structure, Implements query processing and support functions, Evaluates the system against provided queries.

## Functionality

### 1. Text Preprocessing

- Converts all text to lowercase.
- Tokenizes the text using NLTK.
- Removes stop words using NLTK.
- Excludes special characters except alphanumeric characters.
- Eliminates singly occurring characters.
- Creates a set of all the words.

### 2. Inverted Index Implementation

- Implements an inverted index data structure for the preprocessed dataset.

### 3. Query Support

- Supports various queries with AND, OR, and NOT operations.
- Handles queries with a variable number of words.
- Apply preprocessing to the input queries.

### 4. System Evaluation

- Evaluates the system against a set of provided queries.
- Outputs the number of documents retrieved.
- Outputs the minimum number of total comparisons made (if applicable, only for the merging algorithm).
- Outputs the list of retrieved document names.



