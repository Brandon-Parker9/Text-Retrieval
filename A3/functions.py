import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, urljoin

def run_web_scrapping(url):

    soup = prettify_raw_html_from_url(url)

    tables = get_tables(soup)

    print("\n########## Merged Data Frame ##########")

    merged_data_frame = create_data_frame_from_tables(tables)

    print(merged_data_frame)


    print("\n########## h2 contents excluding \"Contents\" and \"Notes\" ##########")

    h2_tags_content = get_h2_text(soup)

    # Iterate through the list of h2 tags and print their contents
    for h2_tag_content in h2_tags_content:

        print(h2_tag_content)

    print("\n########## Traversed Webpages ##########")

    url_list = create_list_of_hyper_links_from_html(soup, url)

    for url in url_list:
        print(url)

    pretty_html_list = get_prettified_raw_html_from_urls(url_list)

    for pretty_html in pretty_html_list:
        print(pretty_html)

def prettify_raw_html_from_url(url):
    
    try:
        # Initialize and return BeautifulSoup with the HTML content
        response = requests.get(url)

        # Raise an exception for any HTTP error status codes
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    
    except Exception as e:

        # Return an empty BeautifulSoup object
        return BeautifulSoup("", 'html.parser')  

def get_tables(soup):

    # Return all tables with class wikitable sortable
    return soup.find_all('table', {'class': 'wikitable sortable'})

def get_h2_text(soup):

    # Find all h2 tags in the parsed HTML
    h2_tags = soup.find_all('h2')

    #  list for content of h2 tags
    h2_tags_content = []

    # Iterate through the list of h2 tags
    for h2_tag in h2_tags:

        # Get the text content of the h2 tag
        h2_text = h2_tag.text
        
        # Remove "[edit]" suffix from the text content
        h2_text = h2_text.replace("[edit]", "").strip()

        if(h2_text != "Contents" and h2_text != "Notes"):

            # append cleaned content to list 
            h2_tags_content.append(h2_text)

    return h2_tags_content

def create_data_frame_from_tables(tables):

    # Initialize an empty list to store tables
    table_list = []

    # Iterate over each table in the input list of tables
    for i in range(len(tables)):

        # Append an empty list to the table_list for this table
        table_list.append([])

        # Find the header row of the current table
        table_header = tables[i].find("tr")

        # Find all th elements within the header row
        table_data = table_header.find_all('th')

        # Extract text from each th element and strip whitespace
        header_row = [element.text.strip() for element in table_data]

        # Append the header row to the current table list
        table_list[i].append(header_row)

        # Iterate over each row in the current table
        for table_row in tables[i].find_all("tr"):

            # Find all td elements within the current row
            table_data = table_row.find_all('td')

            # Extract text from each td element and strip whitespace
            row = [element.text.strip() for element in table_data]

            # If the row has content (i.e., it's not an empty row)
            if len(row) > 0:

                # Append the row to the current table list
                table_list[i].append(row)

    # Initialize an empty list to store DataFrames
    data_frame_list = []  

    # Iterate over each table in the table_list
    for table in table_list:

        # Create a DataFrame from the current table, excluding the first row (header)
        df = pd.DataFrame(table[1:], columns=table[0])
        
        # Drop rows where all values are NaN (if any) and reset index
        df = df.dropna(how='all').reset_index(drop=True)

        # Append the modified DataFrame to the data_frame_list
        data_frame_list.append(df)

    # Initialize merged_df with the first dataframe in the list
    merged_data_frame = data_frame_list[0]  

    # Iterate over the remaining dataframes in the list
    for df in data_frame_list[1:]:  

        # Merge on the 'Name' column using outer join
        merged_data_frame = pd.merge(merged_data_frame, df, on='Name', how='outer')  

    return merged_data_frame

def create_list_of_hyper_links_from_html(soup, url):

    # Find all <a> tags (hyperlinks) in the parsed HTML
    links = soup.find_all('a')

    # Parse the base URL to get the root domain
    base_url = urlparse(url)
    root_domain = base_url.scheme + '://' + base_url.netloc

    # Initialize list of hyperlinks
    hyperlinks = []

    # Iterate over each <a> tag
    for link in links:

        # Extract the href attribute (URL) from the <a> tag
        href = link.get('href')
        if href:

            # Check if the href is a relative URL
            if href.startswith('/') or href.startswith('#'):

                # Append the root domain to the relative URL
                hyperlinks.append(urljoin(root_domain, href))

            else:

                # Append the absolute URL as it is
                hyperlinks.append(href)

    return hyperlinks

def get_prettified_raw_html_from_urls(url_list):

    # Initialize an empty list to store prettified HTML contents
    pretty_html_list = []

    # Iterate over each URL in the url_list
    for i in range(len(url_list)):

        # Retrieve the prettified HTML content from the URL
        pretty_html = prettify_raw_html_from_url(url_list[i])
        
        # Check if the prettified HTML content is not empty
        if pretty_html != "":

            # Append the prettified HTML content to the pretty_html_list
            pretty_html_list.append(pretty_html_list)

        # For testing purposes
        print(f"{i + 1} of {len(url_list)} links completed!")

    return pretty_html_list

def print_list_with_commas(list_to_print):

    for i in range(len(list_to_print)):

        print(list_to_print[i], end="")

        # Add a comma if it's not the last element
        if i < len(list_to_print) - 1:
            print(", ", end="")

    print()  # Print a newline at the end

    return None