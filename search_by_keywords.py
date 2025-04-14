import json
import re
from collections import defaultdict
import os 

# Define your keywords of interest here
KEYWORDS = [
    "gaussian splatting", "semantics", "instance", "foundation",
    "segmentation", "multi-view",  "language"
]


def load_papers(json_path="data/cvpr2025_papers.json"):
    with open(json_path, 'r') as f:
        return json.load(f)


def categorize_papers_by_keywords(papers, keywords):
    categorized = defaultdict(list)
    
    for paper in papers:
        title = paper['title'].lower()
        for kw in keywords:
            if kw.lower() in title:
                categorized[kw].append(paper)
    print(f"Categorized {len(papers)} papers into {len(categorized)} categories.")
    return dict(categorized)


def save_each_category_to_json(categorized, out_dir="data/categories"):
    os.makedirs(out_dir, exist_ok=True)
    for kw, papers in categorized.items():
        filename = kw.replace(" ", "_").lower() + ".json"
        path = os.path.join(out_dir, filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(papers, f, indent=2)
        print(f"Saved {len(papers)} papers for keyword '{kw}' to {path}")


def search_keyword(categorized, keyword):
    return categorized.get(keyword.lower(), [])


if __name__ == "__main__":
    papers = load_papers()
    categorized = categorize_papers_by_keywords(papers, KEYWORDS)
    save_each_category_to_json(categorized)
    print("Categorized papers saved.")

    # Example CLI search prompt
    # prompt = input("Enter keyword to search: ").strip().lower()
    # matches = search_keyword(categorized, prompt)
    # print(f"\nFound {len(matches)} papers for keyword '{prompt}':\n")
    # for paper in matches:
    #     print(f"- {paper['title']}\n  {paper['url']}")
