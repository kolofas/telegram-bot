import logging
import collections
import csv

import bs4
import requests


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('pars')


ParseResult = collections.namedtuple(
    'ParseResult',
    (
        'brand_name',
        'url',
        'lover_name',
        'goods_name',
        'thumbnail',
    ),
)

HEADERS = (
    'Бренд',
    'Цена',
    'Товар',
    'Ссылка',
    'Фото',

)

class Client:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'accept': '*/*'
        }
        self.result = []

    def load_page(self):
        url = 'https://www.wildberries.ru/catalog/muzhchinam/odezhda/vodolazki'
        res = self.session.get(url=url)
        res.raise_for_status()
        return res.text

    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('div.dtList-inner')
        for block in container:
            self.parse_block(block=block)

    def parse_block(self, block):
        url_block = block.select_one('a.ref_goods_n_p.j-open-full-product-card')
        if not url_block:
            logger.error('no url_block')
            return

        url = url_block.get('href')
        if not url:
            logger.error('no href')
            return

        name_block = block.select_one('div.dtlist-inner-brand-name')
        if not name_block:
            logger.error(f'no name_block on {url}')
            return

        brand_name = name_block.select_one('strong.brand-name')
        if not brand_name:
            logger.error(f'no name_block on {url}')
            return

        # Wrangler /
        brand_name = brand_name.text
        brand_name = brand_name.replace('/', '').strip()

        price_block = block.select_one('div.j-cataloger-price')
        if not price_block:
            logger.error(f'no price on {url}')
            return

        price_name = price_block.select_one('span.price')
        if not price_name:
            logger.error(f'no price_name on {url}')
            return

        lover_name = price_name.select_one('ins.lower-price')
        if not lover_name:
            logger.error(f'no lover_name on {url}')
            return

        # lover_name = lover_name.text
        # lover_name = lover_name.replace('/', '').strip()

        goods_name = name_block.select_one('span.goods-name.c-text-sm')
        if not goods_name:
            logger.error(f'no goods_name on {url}')
            return

        goods_name = goods_name.text.strip()

        thumbnail = block.select_one('img.thumbnail')
        if not thumbnail:
            logger.error(f'no img on {url}')
            return



        self.result.append(ParseResult(
            url=url,
            brand_name=brand_name,
            lover_name=lover_name,
            goods_name=goods_name,
            thumbnail=thumbnail,

        ))

        logger.debug('%s, %s, %s, %s, %s', url, brand_name, lover_name, goods_name, thumbnail)
        logger.debug('-' * 100)

    def save_result(self):
        path = 'C:\python\Parsers\parser_shop\parser\zzhtest.csv'
        with open(path, 'w') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADERS)
            for item in self.result:
                writer.writerow(item)

    def run(self):
        text = self.load_page()
        self.parse_page(text=text)
        logger.info(f'Получили {len(self.result)} элементов')
        self.save_result()

if __name__ == '__main__':
    parser = Client()
    parser.run()


