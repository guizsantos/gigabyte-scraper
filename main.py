from scrapy import Spider, Request
from pikepdf import Pdf, PdfImage
from io import BytesIO
from PIL import Image, ImageEnhance, ImageOps
from pytesseract import pytesseract 

pytesseract.tesseract_cmd = "/usr/bin/tesseract" 


class GigabyteMotherboardSpider(Spider):
    name = 'gigabyte_motherboards_spider'
    base_url = 'https://www.gigabyte.com'
    downloads_folder = "downloads"
    start_urls = ['https://www.gigabyte.com/br/Motherboard/GIGABYTE']

    def parse(self, response):
        products = response.xpath('/html/body/div/div[2]/div[3]/div/div[1]/div[1]/div[3]/div[2]/div[has-class("product_list_box")]')
        yield from self.parse_products(products)

        # product_pages = products.xpath('./div/div[1]/div[2]/a')
        # yield from response.follow_all(product_pages, self.parse_product_page)

    def parse_products(self, products):
        for product in products:
            yield {
                'name': product.css('span.product_info_Name::text').get(),
                'url': f"{self.base_url}{product.css('a::attr(href)').get()}"
            }
    
    def parse_product_page(self, response):
        yield Request(
            f"{response.url}/support#support-manual",
            callback=self.parse_spec
        )
    
    def parse_spec(self, response):
        manual_languages = response.xpath('/html/body/div/div[2]/div[3]/div/div[2]/div/div[2]/div[4]/div/div/div/div[3]/div[4]/ul[2]/li[4]/ul/li/div/div/div[has-class("div-table-row")]/div[5]/div/a')
        yield from response.follow_all(
            manual_languages, 
            self.parse_manual,
            meta={'download_timeout': 600}
        )

    def parse_manual(self, response):
        filename = self.save_pdf(response)
        self.save_pdf_images(response, filename)

    def save_pdf(self, response):
        path = self._manual_filename(response)
        self.logger.info(f'Saving PDF {path}')
        with open(path, 'wb') as f:
            f.write(response.body)
        return path

    def save_pdf_images(self, response, filename):
        pdf_file = BytesIO(response.body)
        pdf = Pdf.open(pdf_file)

        for i, page in enumerate(pdf.pages):
            for j, (name, raw_image) in enumerate(page.images.items()):
                image = PdfImage(raw_image)
                image_filename = image.extract_to(fileprefix=f"{filename}-page{i:03}-img{j:03}")
    
    def extract_image_text(self, image_path):
        img = Image.open(image_path)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        img = img.convert('1')
        img = ImageOps.invert(img)
        text = pytesseract.image_to_string(img)

    def _manual_filename(self, response):
        name = response.url.split('/')[-1]
        if '?' in name:
            name = name.split('?')[-2]
        return f"{self.downloads_folder}/{name.lower().replace(' ','-')}"
