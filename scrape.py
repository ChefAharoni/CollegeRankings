from bs4 import BeautifulSoup
import json
import requests
import pandas as pd

# URL to scrape
usnews = "https://www.usnews.com/best-graduate-schools/top-science-schools/computer-science-rankings"
shanghairanking = "https://www.shanghairanking.com/rankings/gras/2023/RS0210"


def get_rankings():
    response = requests.get(shanghairanking)
    print(f"Response: {response.status_code}")
    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Save prettified HTML to file
    with open("prettified.html", "w") as file:
        file.write(soup.prettify())
    
    # Rest of the code...
    


def open_json_file(fname):
    with open(fname) as json_file:
        data = json.load(json_file)
        return data


def write_json_file(fname, data):
    with open(fname, "w") as outfile:
        json.dump(data, outfile)


if __name__ == "__main__":
    get_rankings()
