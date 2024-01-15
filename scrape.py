from bs4 import BeautifulSoup
import json
import requests

# URL to scrape
URL = "https://www.usnews.com/best-graduate-schools/top-science-schools/computer-science-rankings"


def get_rankings():
    response = requests.get(URL)
    print(f"Response: {response}")
    soup = BeautifulSoup(response.content, "xml")
    values = soup.find_all("tr")
    write_json_file("data.json", values)


def open_json_file(fname):
    with open(fname) as json_file:
        data = json.load(json_file)
        return data


def write_json_file(fname, data):
    with open(fname, "w") as outfile:
        json.dump(data, outfile)


if __name__ == "__main__":
    get_rankings()
