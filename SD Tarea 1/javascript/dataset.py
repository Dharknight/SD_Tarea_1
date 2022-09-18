from time import time
from unicodedata import name
import requests
from bs4 import BeautifulSoup

# ------------------- READ_TXT ------------------- #
def read_csv(path, max_lines=None):
       
    with open(path, 'r') as f:
        cont = 0
        lines = f.readlines()[1:]
        for line in lines:
            if (cont == max_lines):
                return
            tab = line.split('\t')

# -------------------------- EVITAR LAS URLS QUE NO ESTEN. SE UTILIZA EL \N YA QUE ES EL ULTIMO CARACTER ANTES DE U SALTO DE LINEA ------------------ #
            if tab[4] == '\n':
                continue
            url = tab[4]

#------------- ------------------ EVITAR LOS SALTOS DE LINEAS ------------------------------ #
            f_url = url[:-1]
            
            data = getInfoUrl(f_url)
            
            if data is not None:
                print(f'[{cont}] {data["url"]}\n Title: {repr(data["title"])}\n Description: {repr(data["description"])}\n Keywords: {repr(data["keywords"])}')
                cont += 1
            
    return 

# ------------------------------ PROCESO DE WEB SCRAPING -------------------------------- #
def getInfoUrl(f_url):
    final = {'url': f_url, 'title': None, 'description': None, 'keywords': None}
    try:
        r = requests.get(f_url, timeout=1)
    except Exception:
        return None

    if r.status_code == 200:
        
        source = requests.get(f_url).text                           # CONEXION A LA URL CONTENIDA EN LA VARIABLE URL
        soup = BeautifulSoup(source, features='html.parser')      # LIBRERÍA BEAUTIFULSOUP PARA SCRAPING. 

        meta = soup.find("meta")                                  # SE BUSCA LA ETIQUETA HTML META. 
                                                                  # SE BUSCA LA ETIQUETA HTML TITLE
        title = soup.find('title')
        
        description = soup.find("meta", {'name': "description"})  # SE BUSCA LA ETIQUETA HTML META EN LA QUE DENTRO DE ESTA CONTENGA UN ATRIBUTO NAME QUE SE LLAME DESCRIPTION
        
        keywords = soup.find("meta", {'name': "keywords"})        # SE BUSCA LA ETIQUETA HTML META EN LA QUE DENTRO DE ESTA CONTENGA UN ATRIBUTO NAME QUE SE LLAME KEYWORDS
        
        try:
            if keywords is None:
                return None
            else:
                description = description['content'] if description else None
                keywords = keywords['content'] if keywords else None
                
                keywords = keywords.replace(" ", "") if keywords else None
                keywords = keywords.replace(".", "") if keywords else None

        except Exception:
            return None
        title = title.get_text().replace("\n","") if title else None
        title = title.replace("\r","") if title else None
        title = title.replace("\t","") if title else None
        final['title'] = title
        final['description'] = description
        final['keywords'] = keywords 
        if final['keywords'] is None:
                return None
        return final
          
    return None

if __name__ == '__main__':
    path = './user-ct-test-collection-09.txt'
    read_csv(path, 100)


