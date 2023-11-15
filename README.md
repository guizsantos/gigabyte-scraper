# Website scraper and images processor (text extraction)

This project uses several tools to extract information from a website, download
documents from the website, and process those documents to obtain text from images
pertaining to the document itself.

To achieve this, the following tools are used:
- Scrapy: Python library providing a framework for high-level web crawling and web scraping
- Pytesseract: Python wrapper for Google's OCR (Optical Character Recognition) Engine
- PikePDF: Python library allowing creation, manipulation and repair of PDFs
- Pillow: Python Imaging Library

## Initial setup

To effectively run this project, you should first install Tesseract, as described
in the OCR section (Linux instruction only, for other systems, search for official
documentation). Furthermore, install the Python dependencies (ensure you are running
in a virtual environment):
```shell
pip install -r requirements.txt
```

Now you may run the crawler using Scrapy:
```shell
python -m scrapy runspider main.py
```

This will crawl Gigabyte's website, retrieving motherboards data, downloading each
motherboard user's manual (saving the PDF file), then proceed by extracting all
images from the PDF and applying an OCR routine to extract textual data from the
PDF images.

### OCR

This project uses Tesseract OCR to retrieve text from images, in Linux systems,
install Tesseract OCR with:
```shell
sudo apt install tesseract-ocr
```

## Possible improvements

### Production deployments

It is noteworthy to state that this project relies on local runs of Tesseract,
only to demonstrate the results. However, in a production environment, where
larger computations may take place, it is possible to use Cloud services and
process the data using APIs, thus reducing the necessary resources to run the project.

### Usage of LLM models

Furthermore, it is also possible to use LLM models to extract further insight from
the textual data retrieved, e.g., using OpenAI GPT API to summarize the data.

## Caveats

Since this is a web crawling project, it is dependent on CSS selectors and XPaths,
which make it particular to the website it was developed for and also fragile for
any changes within the website structure, such as changing a CSS class name.
However, the technologies and knowledge from this project may be applied to other
websites to successfully extract their data.
