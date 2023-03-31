import requests
from bs4 import BeautifulSoup as bs


def get_titles(soup):
    return soup.find_all('h1')

def get_dates(soup):
    return soup.find_all('div',{'class':'text-xs text-gray-500 mt-2'})

def get_contents(soup):
    return soup.find_all('div',{'class':'text-gray-500 text-[16px] mt-4'})

def get_articles(soup, site):
    titles = get_titles(soup)
    dates = get_dates(soup)
    contents = get_contents(soup)

    articles = []
    for i in range(len(contents)):
        article = {'site': site,
                   'titre': titles[i].get_text(strip=True),
                   'date': dates[i].get_text(strip=True),
                   'contenu': contents[i].get_text(strip=True)}
        articles.append(article)

    return articles


def compare_strings(a):
    c=['gang','kidnapping','mort','deces','bandit','disparition','balle','blesse','tue']
    for b in c:
        minimum = min(len(a), len(b)) 
        maximum=max(len(a),len(b))
        count = 0 

        for i in range(minimum):
            if a[i].upper() == b[i].upper():
                count += 1 
        taux=count/maximum
        if taux>=0.8:
            res=True
            break
        else:
            res=False
    return(res)

def affichage(table):
    for article in table:
        for mot in article['contenu'].split():
            if compare_strings(mot):
                print('Mot retrouve: '+mot)
                print("{title}: "+article['titre']+" {dat}:"+article['date'])
                break


leNouvelliste=requests.get('https://lenouvelliste.com')
haitiLibre=requests.get('https://www.haitilibre.com')
soupLenouv=bs(leNouvelliste.content,'html.parser')
soupHaiti=bs(haitiLibre.content,'html.parser')

articlesLenouv = get_articles(soupLenouv, 'Le Nouvelliste')
articlesHaiti = get_articles(soupHaiti, 'Haiti Libre')

print("ARTICLES DE LENOUVELLISTE")
affichage(articlesLenouv)

print("ARTICLES DE HAITILIBRE")
affichage(articlesHaiti)
