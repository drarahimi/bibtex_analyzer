from collections import Counter

import bibtexparser
import matplotlib.pyplot as plt
import matplotlib
import os

# Get the directory of the currently running script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set font globally to Times New Roman
matplotlib.rcParams['font.family'] = 'Times New Roman'

def parse_bibtex(file_path):
    try:
        # Open and parse the .bib file
        with open(file_path, 'r', encoding='utf-8') as bib_file:
            parser = bibtexparser.bparser.BibTexParser()
            parser.common_strings = True  # Enable handling of common strings like "jan"
            bib_database = bibtexparser.load(bib_file, parser=parser)

        # Initialize variables for processing
        years = []
        categories = {'Conference': 0, 'Journal': 0, 'Arxiv': 0}

        # Iterate through the entries in the .bib file
        for entry in bib_database.entries:
            # Extract the publication year
            if 'year' in entry:
                years.append(entry['year'])

            # Classify the entry type
            entry_type = entry.get('ENTRYTYPE', '').lower()  # Use .get to avoid KeyError
            if entry_type == 'article':
                categories['Journal'] += 1
            elif entry_type == 'inproceedings':
                categories['Conference'] += 1
            elif entry_type == 'misc':
                # Additional filtering for arXiv (e.g., by identifier)
                categories['Arxiv'] += 1

        return years, categories

    except Exception as e:
        print(f"Error parsing .bib file: {e}")
        return [], {'conference': 0, 'journal': 0, 'arxiv': 0}


def plot_papers_per_year(years):
    year_counts = Counter(years)
    sorted_years = sorted(year_counts.keys())
    counts = [year_counts[year] for year in sorted_years]

    plt.figure(figsize=(4, 3))
    plt.bar(sorted_years, counts, color='b', alpha=0.7)
    plt.xlabel('Year')
    plt.ylabel('Number of Papers')
    #plt.title('Number of Papers per Year')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    # plt.show()
    plt.savefig(os.path.join(script_dir, "bibstatsyear.pdf"), bbox_inches="tight")


def plot_paper_distribution(categories):
    plt.figure(figsize=(4,3))
    plt.bar(categories.keys(), categories.values(), color=['blue', 'green', 'red'], alpha=0.7, width=0.3)
    plt.xlabel('Category')
    plt.ylabel('Number of Papers')
    #plt.title('Paper Distribution by Type')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # plt.show()
    plt.savefig(os.path.join(script_dir, "bibstatstype.pdf"), bbox_inches="tight")


def main():
    # Construct the full path to the .bib file
    bib_file = os.path.join(script_dir, "bib.bib")
    years, categories = parse_bibtex(bib_file)

    plot_papers_per_year(years)
    plot_paper_distribution(categories)


if __name__ == "__main__":
    main()