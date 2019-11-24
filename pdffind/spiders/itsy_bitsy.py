import re
import textract
import requests
import re
from itertools import chain
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tempfile import NamedTemporaryFile
from pdffind.items import PdffindItem

from scrapy.shell import inspect_response
res = requests.get('http://boletinoficialsalta.gob.ar/BoletinAnexoPDF.php?cXdlcnR5ZGlnaXRhbD0xcXdlcnR5')
control_chars = ''.join(map(chr, chain(range(0, 9), range(11, 32), range(127, 160))))
CONTROL_CHAR_RE = re.compile('[%s]' % re.escape(control_chars))
TEXTRACT_EXTENSIONS = [".pdf"]

def find_between(s, first, last):
     try:
         result = re.search(first+'(.*)'+last, s)
         return result.group(1)
     except ValueError:
         return ""


class ItsyBitsySpider(CrawlSpider):
    name = "itsy_bitsy"
    allowed_domains = ['domain_pdf']
    #get the pdf	
    start_urls = ['http://domain_pdf'+find_between( res.content.decode('utf-8'), 'pagina="', '";' )]

    def parse(self, response):
        #inspect_response(response, self)
        item = PdffindItem()
        if hasattr(response, "text"):
            # The response is text - we assume html. Normally we'd do something

            pass
        else:
            # We assume the response is binary data
            # One-liner for testing if "response.url" ends with any of TEXTRACT_EXTENSIONS
            extension = list(filter(lambda x: response.url.lower().endswith(x), TEXTRACT_EXTENSIONS))[0]
            if extension:
                # This is a pdf or something else that Textract can process
                # Create a temporary file with the correct extension.
                tempfile = NamedTemporaryFile(suffix=extension)
                tempfile.write(response.body)
                tempfile.flush()
                extracted_data = textract.process(tempfile.name)
                extracted_data = extracted_data.decode('utf-8')
                extracted_data = CONTROL_CHAR_RE.sub('', extracted_data)
                edictos = extracted_data.split('OP N')
                for edicto in edictos:
                    item['edicto'] = edicto
                    yield item
                
