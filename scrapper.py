import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_cvpr2025_papers_with_authors(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    papers = []
    for row in soup.find_all('tr'):
        title_tag = row.find('strong')
        authors_tag = row.find('div', class_='indented')
        link_tag = row.find('a', href=True)

        if title_tag and authors_tag:
            title = title_tag.get_text(strip=True)
            authors_raw = authors_tag.get_text(strip=True)
            authors = [a.strip() for a in authors_raw.split('·') if a.strip()]
            link = link_tag['href'] if link_tag else None
            if link and not link.startswith('http'):
                link = f"https://cvpr.thecvf.com{link}"

            papers.append({
                "title": title,
                "authors": authors,
                "url": link
            })

    return papers

def save_papers_to_json(papers, out_path="data/cvpr2025_papers.json"):
    os.makedirs("data", exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(papers, f, indent=2)

if __name__ == "__main__":
    url = "https://cvpr.thecvf.com/Conferences/2025/AcceptedPapers"
    papers = scrape_cvpr2025_papers_with_authors(url)
    save_papers_to_json(papers)
    print(f"Saved {len(papers)} papers to JSON.")
