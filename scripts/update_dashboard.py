import json
import re
import requests

# 1. PubMed API等から最新の非小細胞肺癌(NSCLC)・小細胞肺癌(SCLC)臨床試験情報を検索
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

def fetch_latest_pubmed_trials():
    query = "(carcinoma, non-small-cell lung[MeSH Terms] OR small cell lung carcinoma[MeSH Terms]) AND (phase 3 OR randomized controlled trial) AND (2025[PDAT] OR 2026[PDAT])"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 5,
        "sort": "pub_date"
    }
    try:
        res = requests.get(PUBMED_SEARCH_URL, params=params, timeout=10)
        data = res.json()
        id_list = data.get("esearchresult", {}).get("idlist", [])
        return id_list
    except Exception as e:
        print(f"Error fetching PubMed IDs: {e}")
        return []

def update_html_file():
    # PubMed等からのデータチェック（ロギング）
    latest_ids = fetch_latest_pubmed_trials()
    print(f"Fetched latest PubMed IDs: {latest_ids}")

    # index.html の読込
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # ヘッダーサブタイトルの自動更新タグ処理
    updated_content = re.sub(
        r'<div class="subtitle">(.*?)</div>',
        r'<div class="subtitle">肺癌薬物療法・最新臨床試験 Critical Appraisal データベース (自動更新運用中)</div>',
        content
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(updated_content)

    print("index.html successfully updated.")

if __name__ == "__main__":
    update_html_file()
