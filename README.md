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

## Caveats

Since this is a web crawling project, it is dependent on CSS selectors and XPaths,
which make it particular to the website it was developed for and also fragile for
any changes within the website structure, such as changing a CSS class name.
However, the technologies and knowledge from this project may be applied to other
websites to successfully extract their data.
