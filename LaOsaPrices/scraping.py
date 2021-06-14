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


def updating_osa():
    # This function takes new data from Google Spreadsheet temporarily

    osa_data = pd.read_csv('/home/sergio/Descargas/products_list (1) - precios LA OSA.csv')
    daily_osa_dataframe = pd.DataFrame(osa_data)
    return daily_osa_dataframe


def updating_dia():
    # This function creates a tiny dataframe with the product's prices updated and dated every time it runs.

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


def updating_eroski():
    # This function creates a tiny dataframe with the product's prices updated and dated every time it runs.

    daily_eroski_dataframe = pd.DataFrame(columns=['id', 'producto', 'tienda', 'precio', 'unidad', 'fecha'])
    tienda = 'Eroski'
    fecha = time.strftime('%A %H:%M %d-%m-%Y')
    products_dict = product_list()

    print('Starting to scrape Eroski...')

    eroski_url_dict = {
        101: f'https://supermercado.eroski.es/es/productdetail/23628514-tomate-ecologico-eroski-natur-bio-al-peso'
             f'-compra-minima-500-g/',
        102: f'https://supermercado.eroski.es/es/productdetail/23628209-platano-de-canarias-eco-eroski-natur-bio-al'
             f'-peso-compra-minima-1-kg/',
        103: f'https://supermercado.eroski.es/es/productdetail/23628084-manzana-roja-ecologica-eroski-natur-bio-al'
             f'-peso-compra-minima-1-kg/',
        104: f'https://supermercado.eroski.es/es/productdetail/23628340-calabacin-ecologico-eroski-natur-bio-al-peso'
             f'-compra-minima-500-g/',
        105: f'https://supermercado.eroski.es/es/productdetail/23628548-zanahoria-ecologica-eroski-natur-bio-bandeja'
             f'-600-g/',
        106: f'https://supermercado.eroski.es/es/productdetail/23628431-patata-ecologica-eroski-natur-bio-al-peso'
             f'-compra-minima-1-kg/',
        501: f'https://supermercado.eroski.es/es/productdetail/24031197-chocolate-negro-74-costa-de-marfil-ethiquable'
             f'-tableta-100-g/',
        703: f"https://supermercado.eroski.es/es/productdetail/11735339-bebida-de-avena-yosoy-brik-1-litro/",
        705: f'https://supermercado.eroski.es/es/productdetail/14854624-leche-semidesnatada-ecologica-puleva-brik-1'
             f'-litro/',
        707: f'https://supermercado.eroski.es/es/productdetail/12450268-kefir-ecologico-de-cabra-cantero-de-letur'
             f'-frasco-420-g/',
        901: f'https://supermercado.eroski.es/es/productdetail/16425886-tortellini-integral-queso-espinacas-natursoy'
             f'-bandeja-250-g/',
        1201: f'https://supermercado.eroski.es/es/productdetail/311712-cerveza-mahou-clasica-lata-33-cl/'}

    for product_id, url in eroski_url_dict.items():
        print(url)
        time.sleep(5)
        html = requests.get(url).text
        soup_eroski = BeautifulSoup(html, 'lxml')
        price_eroski = soup_eroski.find('span', {'class': 'price-product'})

        if price_eroski is None:

            try:
                precio = soup_eroski.find('span', {'class': 'offer-now'}).text.strip().replace(',', '.')
                unidad = '1 KILO'

            except:

                precio = 'No disponible'
                unidad = 'No disponible'

        else:
            precio = price_eroski.text.split()[0]
            unidad = soup_eroski.find('span', {'class': 'quantity-product'}).text.split()[0:2]
            unidad = ' '.join(unidad)

        print(product_id, '--', precio, '--', unidad)

        producto = [v for k, v in products_dict.items() if k == product_id]

        # Adding new line to the dataframe
        daily_eroski_dataframe.loc[len(daily_eroski_dataframe)] = [product_id, producto[0], tienda, precio, unidad,
                                                                   fecha]
    return daily_eroski_dataframe


def alcampo_urls():
    al_dict = {101: f"https://www.alcampo.es/compra-online/frescos/verduras-y-hortalizas/verduras-ecologicas"
                    f"/hortaliza-ecologica-tomate-de-ensalada-ecologico-600g/p/55576",
               102: f'https://www.alcampo.es/compra-online/alimentacion/ecologicos/productos-frescos-ecologicos'
                    f'/frutas-y-verduras-ecologicas/frutas-ecologicas/fruta-ecologica-platanos-ecologicos-bandeja-de'
                    f'-800-g/p/57540',
               103: f'https://www.alcampo.es/compra-online/frescos/frutas/frutas-ecologicas/fruta-manzanas-royal'
                    f'-ecologica-800-g/p/57561',
               104: f'https://www.alcampo.es/compra-online/frescos/verduras-y-hortalizas/verduras-ecologicas'
                    f'/hortaliza-ecologica-calabacin-ecologico-600-g/p/55542',
               105: f'https://www.alcampo.es/compra-online/frescos/verduras-y-hortalizas/verduras-ecologicas'
                    f'/alcampo-produccion-controlada-ecologico-zanahoria-ecologico-700-g/p/58394',
               106: f'https://www.alcampo.es/compra-online/frescos/verduras-y-hortalizas/verduras-ecologicas'
                    f'/alcampo-produccion-controlada-ecologico-patata-ecologica-malla-de-2-kg/p/58396',
               302: f'https://www.alcampo.es/compra-online/alimentacion/desayuno-y-merienda/bolleria-y'
                    f'-pasteleria/croissants-magdalenas-y-muffins/magdalenas/la-granja-mini-magdalenas'
                    f'-ecologicas-chocochip-con-yogur-200-g/p/563256',
               303: f'https://www.alcampo.es/compra-online/alimentacion/desayuno-y-merienda/bolleria-y'
                    f'-pasteleria/rosquillas-y-sobaos/rosquillas/monjas-rosquillas-250-g/p/13606',
               304: f'https://www.alcampo.es/compra-online/alimentacion/alimentos-especiales-/alimentos'
                    f'-especiales/dulces-y-desayunos/bolleria/la-granja-bizcocho-marmol-ecologico-300-g/p/801212',
               702: f'https://www.alcampo.es/compra-online/alimentacion/alimentos-especiales-/alimentos'
                    f'-especiales/bebidas-soja-avena-y-arroz/bebidas-de-avena/soria-natural-bebida-de-avena-1-l'
                    f'/p/12207',
               704: f'https://www.alcampo.es/compra-online/alimentacion/leche-huevos-yogures-y-lacteos/yogures'
                    f'-bifidus-y-lcasei/desnatado/sabores/casa-grande-de-xanceda-yogur-de-fresa-ecologico-2-uds'
                    f'-x-125-g/p/52971',
               705: f'https://www.alcampo.es/compra-online/alimentacion/ecologicos/productos-frescos-ecologicos'
                    f'/lacteos-quesos-y-huevos-ecologicos/leche-y-nata-ecologicas/puleva-eco-leche-semidesnatada'
                    f'-ecologica-1-l/p/53042',
               707: f"https://www.alcampo.es/compra-online/alimentacion/ecologicos/productos-frescos-ecologicos"
                    f"/lacteos-quesos-y-huevos-ecologicos/kefir-ecologico/cantero-de-letur-kefir-de-cabra-bio"
                    f"-420-gramos/p/519624",
               1001: f'https://www.alcampo.es/compra-online/alimentacion/caldos-pasta-arroz-legumbres-pure/arroz'
                     f'/arroz-para-cocinar/calasparra-arroz-redondo-1-kg/p/25214',
               1101: f'https://www.alcampo.es/compra-online/alimentacion/desayuno-y-merienda/cafessucedaneos-y'
                     f'-derivados-del-cacao/cafe-molido/molido-natural/intermon-oxfam-tierra-madre-cafe-molido'
                     f'-natural-250-g/p/16348',
               1201: f'https://www.alcampo.es/compra-online/bebidas/cervezas/lata-estandar/mahou-cerveza-33cl/p/30378'}

    return al_dict


def updating_alcampo():
    # This function creates a tiny dataframe with the product's prices updated and dated every time it runs.

    daily_alcampo_dataframe = pd.DataFrame(columns=['id', 'producto', 'tienda', 'precio', 'unidad', 'fecha'])
    tienda = 'Alcampo'
    fecha = time.strftime('%A %H:%M %d-%m-%Y')
    products_dict = product_list()

    print('Starting to scrape Alcampo...')
    
    alcampo_url_dict = alcampo_urls()

    for product_id, url in alcampo_url_dict.items():
        print(url)
        time.sleep(5)
        html = requests.get(url).text
        soup_alcampo = BeautifulSoup(html, 'lxml')

        try:
            price_alcampo = soup_alcampo.find('span', {'class': 'precioUnidad pesoVariable'}).text

        except:
            price_alcampo = soup_alcampo.find('span', {'class': 'pesoVariable precioUnidad'}).text

        if price_alcampo is None:

            precio = 'No disponible'
            unidad = 'No disponible'

        else:
            precio = re.findall('[0-9,]+', price_alcampo)[0].replace(',', ('.'))
            unidad = re.findall('(\€.*)\)', price_alcampo)[0]

        print(product_id, '--', precio, '--', unidad)

        producto = [v for k, v in products_dict.items() if k == product_id]

        # Adding new line to the dataframe
        daily_alcampo_dataframe.loc[len(daily_alcampo_dataframe)] = [product_id, producto[0], tienda, precio, unidad,
                                                                     fecha]
    return daily_alcampo_dataframe


def updating_navarro():
    # This function creates a tiny dataframe with the product's prices updated and dated every time it runs.

    daily_navarro_dataframe = pd.DataFrame(columns=['id', 'producto', 'tienda', 'precio', 'unidad', 'fecha'])
    tienda = 'Navarro'
    fecha = time.strftime('%A %H:%M %d-%m-%Y')
    products_dict = product_list()

    print('Starting to scrape Herbolario Navarro...')

    navarro_url_dict = {202: f'https://www.herbolarionavarro.es/copos-de-5-cereales.html',
                        402: f'https://www.herbolarionavarro.es/harina-de-avena-integral-ecologica.html',
                        501: f'https://www.herbolarionavarro.es/chocolate-negro-75-nicaragua-100g.html',
                        701: f'https://www.herbolarionavarro.es/leche-de-vaca-semi-eco-1l.html',
                        702: f'https://www.herbolarionavarro.es/bebida-de-avena-1.html',
                        704: f'https://www.herbolarionavarro.es/yogur-cremoso-eco-desnatado-con-fresa.html',
                        706: f'https://www.herbolarionavarro.es/leche-de-vaca-entera.html',
                        707: f'https://www.herbolarionavarro.es/kefir-cabra-420gr.html',
                        802: f'https://www.herbolarionavarro.es/mejillones-en-escabeche.html',
                        1002: f'https://www.herbolarionavarro.es/arroz-redondo-integral-de-calasparrra-bio.html'}

    for product_id, url in navarro_url_dict.items():
        print(url)
        time.sleep(5)
        html = requests.get(url).text
        soup_navarro = BeautifulSoup(html, 'lxml')

        try:
            price_navarro = soup_navarro.find('div', {'class': 'capacity-calculator'}).text
        except AttributeError:
            pass
        else:
            price_navarro = soup_navarro.find('span', {'class': 'price'}).text

        if price_navarro is None:

            precio = 'No disponible'
            unidad = 'No disponible'

        else:
            precio = re.findall('[0-9,]+', price_navarro)[0].replace(',', ('.'))
            unidad = re.findall('(\€.*)', price_navarro)[0].strip()

        print(product_id, '--', precio, '--', unidad)

        producto = [v for k, v in products_dict.items() if k == product_id]

        # Adding new line to the dataframe
        daily_navarro_dataframe.loc[len(daily_navarro_dataframe)] = [product_id, producto[0], tienda, precio, unidad,
                                                                     fecha]
    return daily_navarro_dataframe


def carrefour_urls():
    cr_dict = {
        101: f'https://www.carrefour.es/supermercado/tomate-rama-ecologico-carrefour-bio-500-g-carrefour-bio/R'
             f'-600709258/p?ic_source=food&ic_medium=undefined&ic_content=cat20002-productos-frescos',
        102: f'https://www.carrefour.es/supermercado/platano-ecologico-carrefour-bio-1-kg-aprox-carrefour-bio/R'
             f'-fprod1320276/p?ic_source=food&ic_medium=undefined&ic_content=cat20002-productos-frescos',
        103: f'https://www.carrefour.es/supermercado/manzana-royal-gala-ecologica-bandeja-4-ud-600-g-carrefour-bio/R'
             f'-600709190/p?ic_source=food&ic_medium=undefined&ic_content=cat20002-productos-frescos',
        104: f'https://www.carrefour.es/supermercado/calabacin-ecologico-carrefour-bio-500-g-carrefour-bio/R'
             f'-600709114/p?ic_source=food&ic_medium=undefined&ic_content=cat20002-productos-frescos',
        105: f'https://www.carrefour.es/supermercado/zanahoria-ecologica-carrefour-bio-750-g-carrefour-bio/R'
             f'-prod1070419/p?ic_source=food&ic_medium=undefined&ic_content=cat20002-productos-frescos',
        106: f'https://www.carrefour.es/supermercado/patata-ecologica-carrefour-bio-2-kg-carrefour-bio/R-600709102/p'
             f'?ic_source=food&ic_medium=undefined&ic_content=cat20002-productos-frescos',
        304: f'https://www.carrefour.es/supermercado/bizcocho-marmol-con-chocolate-ecologico-la-granja-300-g/R'
             f'-VC4AECOMM-491615/p?ic_source=food&ic_medium=undefined&ic_content=cat20002-productos-frescos',
        501: f'https://www.carrefour.es/supermercado/chocolate-negro-75-ecologico-ethiquable-100-g-ethiquable/R'
             f'-fprod1450021/p?ic_source=portal-y-corporativo&ic_medium=search-empathy&ic_content=ns',
        602: f'https://www.carrefour.es/supermercado/bacon-lonchas-ecologico-biobardales-100-g-biobardales/R'
             f'-590205589/p?ic_source=portal-y-corporativo&ic_medium=search-empathy&ic_content=ns',
        702: f'https://www.carrefour.es/supermercado/bebida-de-avena-con-calcio-ecologica-soria-natural-brik-1-l'
             f'-soria-natural/R-701717697/p',
        703: f'https://www.carrefour.es/supermercado/bebida-de-avena-sin-azucar-anadido-yosoy-brik-1-l-yosoy/R'
             f'-804323938/p',
        704: f'https://www.carrefour.es/supermercado/yogur-con-vainilla-ecologico-casa-grande-de-xanceda-pack-de-2'
             f'-unidades-de-125-g-casa-grande-de-xanceda/R-590206249/p',
        705: f'https://www.carrefour.es/supermercado/leche-semidesnatada-ecologica-puleva-brik-1-l-puleva/R-625735708/p',
        706: f'https://www.carrefour.es/supermercado/leche-entera-ecologica-cantero-de-letur-1-l-cantero-de-letur/R'
             f'-fprod1250295/p',
        707: f'https://www.carrefour.es/supermercado/kefir-de-cabra-ecologico-cantero-de-letur-420-g-cantero-de-letur'
             f'/R-prod410336/p',
        1101: f'https://www.carrefour.es/supermercado/cafe-molido-natural-tierra-madre-oxfam-intermon-250-g-oxfam'
              f'-intermon/R-526510893/p',
        1201: f'https://www.carrefour.es/supermercado/cerveza-mahou-clasica-lata-33-cl-mahou-clasica/R-520661319/p'}

    return cr_dict


def updating_carrefour():
    daily_carrefour_dataframe = pd.DataFrame(columns=['id', 'producto', 'tienda', 'precio', 'unidad', 'fecha'])
    tienda = 'Carrefour'
    fecha = time.strftime('%A %H:%M %d-%m-%Y')
    products_dict = product_list()

    print('Starting to scrape Carrefour...')

    carrefour_url_dict = carrefour_urls()

    for product_id, url in carrefour_url_dict.items():
        print(url)
        time.sleep(30)
        html = requests.get(url).text
        soup_carrefour = BeautifulSoup(html, 'lxml')
        price_carrefour = soup_carrefour.find(('div'), {'class': 'buybox__price-per-unit'}).text.strip().replace(',',                                                                                                         '.')

        if price_carrefour is None:
            precio = 'No disponible'
            unidad = 'No disponible'
        else:
            precio = price_carrefour.split()[0]
            unidad = price_carrefour.split()[-1]
            print(product_id, '--', precio, '--', unidad)

        producto = [v for k, v in products_dict.items() if k == product_id]

        # Adding new line to the dataframe
        daily_carrefour_dataframe.loc[len(daily_carrefour_dataframe)] = [product_id, producto[0], tienda, precio,
                                                                         unidad, fecha]
    return daily_carrefour_dataframe
