from bs4 import BeautifulSoup
import pandas as pd

# Load the HTML file
file_path = "/mnt/data/ShanghaiRanking's Global Ranking of Academic Subjects.html"
with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()


def get_rankings():
    # Parse the HTML content
    soup = BeautifulSoup(content, "html.parser")

    # Find all universities
    universities = soup.find_all("tr", class_="bgfd")

    # Extract the required data
    data = []
    for uni in universities:
        logo = uni.find("img")["src"] if uni.find("img") else None
        name = uni.find("td", class_="left").get_text(strip=True)
        ranking = uni.find("td", class_="bgfd").get_text(strip=True)
        data.append({"Logo": logo, "Name": name, "Ranking": ranking})

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Save to CSV
    csv_file_path = "/mnt/data/universities_rankings.csv"
    df.to_csv(csv_file_path, index=False)
