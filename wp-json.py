import requests
import argparse
import json

# Define the argument parser
parser = argparse.ArgumentParser(description="A tool to scrape data from wp-json path of a WordPress site")
parser.add_argument("-u", "--url", help="The URL of the WordPress site")
parser.add_argument("-f", "--file", help="The file containing a list of URLs of WordPress sites")
args = parser.parse_args()

# Define a function to scrape data from a single URL
def scrape_data(url):
    # Append the wp-json path to the URL
    url = url.rstrip("/") + "/wp-json"
    # Make a GET request to the URL and get the response as JSON
    response = requests.get(url).json()
    # Initialize an empty list to store the results
    results = []
    # Initialize an empty set to store the endpoints
    endpoints = set()
    # Initialize an empty set to store the href URLs
    href_urls = set()
    # Define a recursive function to traverse the response and extract the endpoints and href URLs
    def traverse(data, path):
        # Check if the data is a dictionary
        if isinstance(data, dict):
            # Loop through the keys and values in the data
            for key, value in data.items():
                # Check if the key is "href"
                if key == "href":
                    # Add the value to the href URLs set
                    href_urls.add(value)
                # Otherwise, append the key to the path and recurse on the value
                else:
                    traverse(value, path + "/" + key)
        # Check if the data is a list
        elif isinstance(data, list):
            # Loop through each element in the data
            for element in data:
                # Recurse on the element with the same path
                traverse(element, path)
        # Otherwise, check if the path is not empty
        elif path:
            # Add the path to the endpoints set
            endpoints.add(path)
    # Call the recursive function on the response with an empty path
    traverse(response, "")
    # Create a result dictionary with endpoints and href URLs
    result = {"endpoints": endpoints, "href_urls": href_urls}
    # Append the result to the results list
    results.append(result)
    # Return the results list
    return results

# Define a function to sort the results by endpoints and href URLs
def sort_results(results):
    # Loop through each result in the results list
    for result in results:
        # Sort the endpoints by endpoint name in ascending order and convert it to a list
        result["endpoints"] = sorted(list(result["endpoints"]))
        # Sort the href URLs by URL name in ascending order and convert it to a list
        result["href_urls"] = sorted(list(result["href_urls"]))
    # Return the sorted results list
    return results

# Define a function to write the results to files
def write_results(results):
    # Loop through each result in the results list
    for i, result in enumerate(results):
        # Create a file name for endpoints using the index of the result
        endpoints_file = f"endpoints_{i}.txt"
        # Create a file name for href URLs using the index of the result
        href_urls_file = f"href_urls_{i}.txt"
        # Open both files in write mode
        with open(endpoints_file, "w") as ef, open(href_urls_file, "w") as hf:
            # Loop through each endpoint name in the endpoints list
            for name in result["endpoints"]:
                # Write the endpoint name to the endpoints file with a newline character
                ef.write(name + "\n")
            # Loop through each href URL name in the href URLs list
            for name in result["href_urls"]:
                # Write the href URL name to the href URLs file with a newline character
                hf.write(name + "\n")

# Check if the user provided a URL as input
if args.url:
    # Scrape data from the URL and store it in a variable
    data = scrape_data(args.url)
    # Sort the data by endpoints and href URLs and store it in another variable
    sorted_data = sort_results(data)
    # Write the sorted data to files
    write_results(sorted_data)
#elif args.file:
# Check if the user provided a file as input
elif args.file:
    # Open the file in read mode
    with open(args.file, "r") as f:
        # Initialize an empty list to store the data from all URLs
        data = []
        # Loop through each line in the file
        for line in f:
            # Strip the newline character from the line and store it as a URL
            url = line.strip()
            # Scrape data from the URL using the scrape_data function and append it to the data list
            data.extend(scrape_data(url))
        # Sort the data by endpoints and href URLs using the sort_results function and store it in another variable
        sorted_data = sort_results(data)
        # Write the sorted data to files using the write_results function
        write_results(sorted_data)