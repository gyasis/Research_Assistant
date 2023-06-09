# scripts/bib_downloader.py
import bibtexparser
from scidownl import scihub_download


def build_source_data(bib_entries):
    source = []
    failed_downloads = []

    for entry in bib_entries:
        paper_type = None
        paper = None

        if 'doi' in entry:
            paper_type = 'doi'
            paper = "https://doi.org/" + entry['doi']
        elif 'pmid' in entry:
            paper_type = 'pmid'
            paper = entry['pmid']
        
        if paper_type is not None:
            source.append((paper, paper_type, "./paper/"))
        elif 'title' in entry:  # paper failed to download, will retry with title
            failed_downloads.append((entry['title'], 'title', "./paper/"))
    
    return source, failed_downloads


def download_papers(bib_file):
    with open(bib_file) as bibtex_file:
        bibtex_str = bibtex_file.read()

    bib_database = bibtexparser.loads(bibtex_str)
    source_data, failed_downloads = build_source_data(bib_database.entries)

    for paper, paper_type, out in source_data:
        try:
            scihub_download(paper, paper_type=paper_type, out=out)
        except Exception as e:
            print(f"Failed to download {paper_type}: {paper}. Error: {e}")

    print("Retrying failed downloads with 'title'...")
    for paper, paper_type, out in failed_downloads:
        try:
            scihub_download(paper, paper_type=paper_type, out=out)
        except Exception as e:
            print(f"Failed to download {paper_type}: {paper}. Error: {e}")

