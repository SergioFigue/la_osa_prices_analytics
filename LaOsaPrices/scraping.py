import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time


# HEADER = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,
#             */*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#            'Accept-Encoding': 'gzip, deflate',
#            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
#            'Dnt': '1',
#            'Host': 'httpbin.org',
#            'Upgrade-Insecure-Requests': '1',
#            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)
#            Chrome/44.0.2403.157 Safari/537.36'}


def product_list():
    # List of product to match id.
    products_dict = {101: 'tomate ensalada', 102: 'plátano canario', 103: 'manzana royal', 104: 'calabacín',
                     105: 'zanahoria', 106: 'patata blanca', 202: 'El Granero Int. – Copos de avena s. integral (1Kg.)',
                     301: 'Biocop – galleta copos aventa integral', 302: 'La granja – mini magdalenas varios',
                     303: 'Repostería Monjas – Rosquillas(p / u)',
                     304: 'La granja - Mármol', 401: 'Leon de Baker Hogaza de masa madre (470gr.)',
                     402: 'El Granero Integral – Integral (500gr.)', 501: 'Ethiquable – Negro 75% cacao (100gr.)',
                     602: 'Biobardales – Bacon Lonchas (100gr.)', 701: 'Ken – Leche vaca semi (1l.)',
                     702: 'Soria Natural – Avena calcio(1l.)', 703: 'YoSoy - Avena (1l.)',
                     704: 'Xanceda Yogur eco desnatado fresa(2 uds.)', 705: 'Puleva Eco – Leche semi (1l.)',
                     706: 'Cantero Letur - Leche entera eco Vaca(1l.)',
                     707: 'Cantero  Letur -  Kefir eco cabra (420gr.)',
                     802: 'Pan do mar – Mejillones eco escabeche(115 gr.)',
                     901: 'Natursoy - Tortellini queso espinaca (250 gr.)', 1001: 'Calasparra – Redondo (1Kg.)',
                     1002: 'Calasparra – Integral Bio(1 Kg.)',
                     1101: 'Tierra Madre – Café Natural (250 gr.) o Biológico',
                     1201: 'Mahou Clásica lata(33cl)'}

    return products_dict


def updating_dia():
    # This function creates a tiny dataframe with the product's prices updated and dated every time it runs. Raws will be added to the main database.

    daily_dia_dataframe = pd.DataFrame(columns=['id', 'producto', 'tienda', 'precio', 'unidad', 'fecha'])
    tienda = 'Dia'
    fecha = time.strftime('%A %H:%M %d-%m-%Y')
    products_dict = product_list()

    print('Starting to scrape Dia...')

    dia_url_dict = {
        101: f'https://www.dia.es/compra-online/al-dia/verduras-y-hortalizas/tomates-pimientos-y-pepinos/p/170524',
        102: f'https://www.dia.es/compra-online/al-dia/frutas/platanos/p/170563',
        103: f'https://www.dia.es/compra-online/al-dia/frutas/manzanas/p/271644',
        104: f'https://www.dia.es/compra-online/al-dia/verduras-y-hortalizas/calabacin-calabaza-y-berenjena/p/190696',
        105: f'https://www.dia.es/compra-online/al-dia/verduras-y-hortalizas/patatas-y-zanahorias/p/170530',
        703: f'https://www.dia.es/compra-online/despensa/lacteos-y-huevos/bebidas-vegetales/p/270828',
        705: f'https://www.dia.es/compra-online/despensa/lacteos-y-huevos/leche/p/141031',
        1201: f'https://www.dia.es/compra-online/bebidas/cervezas/nacionales/p/14752'}

    for product_id, url in dia_url_dict.items():
        print(url)
        time.sleep(5)
        html = requests.get(url).text
        soup_dia = BeautifulSoup(html, 'lxml')
        price_dia = soup_dia.find('span', {'class': 'average-price'})

        if price_dia is None:
            precio = 'No disponible'
            unidad = 'No disponible'
        else:
            price_dia = price_dia.text
            price = re.findall('[0-9,]+', price_dia)
            if len(price) == 1:
                precio = float(re.sub(",", '.', price[0]))
            else:
                precio = float(re.sub(",", '.', price[1]))

            unidad = re.findall('(\€.*)', price_dia)[0]

        print(product_id, '--', precio, '--', unidad)

        producto = [v for k, v in products_dict.items() if k == product_id]

        # Adding new line to the dataframe
        daily_dia_dataframe.loc[len(daily_dia_dataframe)] = [product_id, producto[0], tienda, precio, unidad, fecha]

    return daily_dia_dataframe
