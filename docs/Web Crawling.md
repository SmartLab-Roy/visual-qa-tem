## download the related PDF files on Nature
This tool is intended for academic research purposes only. Users must:

* Comply with Nature website terms of service
* Ensure usage complies with copyright regulations
* Not use for commercial purposes

This is an automation tool designed to crawl PDF files of research papers related to "transmission electron microscopy" from the Nature website.

### How to use
```bash
#using default settings
python scripts/nature_crawler.py

# Specify starting year
python scripts/nature_crawler.py --year 2020

# Specify the maximum number of articles per year
python scripts/nature_crawler.py --max-articles 500

# Specify download directory
python scripts/scripts/nature_crawler.py --output-dir ./my_papers

# Use in combination
python scripts/nature_crawler.py --year 2019 --max-articles 200 --output-dir ./research_papers
```

### Note 
we default to searching for TEM-related papers. If you need to change the search topic, you should modify the search title and filtering content in the **navigate_to_nature** function. Please be aware that this script uses XPath for element positioning, which may change as the website gets updated.
