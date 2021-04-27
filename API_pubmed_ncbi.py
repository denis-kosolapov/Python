from Bio.Entrez import efetch, read
from Bio import Entrez
from bs4 import BeautifulSoup
import requests
from requests import request
import requests
from lxml import etree
import math
from pprint import pprint as pp

# https://www.ncbi.nlm.nih.gov/geo/info/geo_paccess.html
# Entrez.email = 'scisoftdev@gmail.com'

email = 'scisoftdev@gmail.com'
search = 'gerontology'
print('текст запроса: ' + search)

query = r'https://pubmed.ncbi.nlm.nih.gov/?term=' + search
page = request('GET', query).text
soup = BeautifulSoup(page, features="lxml")
results_amount = [el.text for el in soup.select('span.value')]
res_num = int(results_amount[0].replace(',', ''))
print('найдено ' + str(res_num) + ' результатов')
pages = math.ceil(res_num / 10)
print('страниц ' + str(pages))

# ids = []
# for j in range(100):
#     search = 'gerontology'
#     query = r'https://pubmed.ncbi.nlm.nih.gov/?term=' + search + '&page=' + str(j + 1)
#     page = request('GET', query).text
#     soup = BeautifulSoup(page, features="lxml")
#     # так пишутся селекторы, классы и ид задаются как в css
#     results_amount = [el.text for el in soup.select('span.value')]
#     ids_on_page = [el.text for el in soup.select('span.docsum-pmid')]
#     for link in ids_on_page:
#         ids.append(link)

id_list = []
res_num = str(res_num)
url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=' + search + '&retmax=' + res_num + '&usehistory=y'
# url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=gerontology&retmax=104408&usehistory=y'
response = requests.get(url)
tree = etree.fromstring(response.content)
ids = tree.xpath("//IdList/Id")
print(len(ids))

for id in ids:
    id_list.append(id.text)


# ARTICLE_URL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&tool=PMA&id=33789757'
# для быстрого получения идентификаторов
# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=gerontology&retmax=104408&usehistory=y
ARTICLE_URL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?tool=PMA&email=' + email + '&db=pubmed&retmode=xml&id='

for id in id_list:
    url = ARTICLE_URL + id
    response = requests.get(url)

    tree = etree.fromstring(response.content)
    id_list = tree.xpath("//MedlineCitation/PMID[@Version='1']")
    title_list = tree.xpath("//Article/ArticleTitle")
    affiliation_list = tree.xpath("//AffiliationInfo/Affiliation")
    abstract_list = tree.xpath("//Abstract/AbstractText")
    journal_list = tree.xpath("//Journal/Title")
    keyword_list = tree.xpath("//KeywordList/Keyword ")

    author_last_name = tree.xpath("//AuthorList/Author/LastName")
    author_fore_name = tree.xpath("//AuthorList/Author/ForeName")

    DateCompleted_year = tree.xpath("//MedlineCitation/DateRevised/Year")
    DateCompleted_month = tree.xpath("//MedlineCitation/DateRevised/Month")
    DateCompleted_day = tree.xpath("//MedlineCitation/DateRevised/Day")

    for id in id_list:
        print(id.text)

    for title in title_list:
        print('title: ' + title.text)

    compare = []
    for affiliation in affiliation_list:
        if affiliation.text not in compare:
            compare.append(affiliation.text)
    for i in compare:
        print('affiliation: ' + i)

    for abstract in abstract_list:
        try:
            print('Abstract: ' + abstract.text)
        except:
            print('abstract not found')

    for journal in journal_list:
        print('journal: ' + journal.text)

    for keyword in keyword_list:
        print('keyword: ' + keyword.text)

    for i in range(len(author_last_name)):
        print(author_last_name[i].text, ' ', author_fore_name[i].text)

    for i in range(len(DateCompleted_year)):
        print(DateCompleted_year[i].text + '.' + DateCompleted_month[i].text + '.' + DateCompleted_day[i].text)
    print()



# def abstract(pmid):
#     handle = efetch(db='pubmed', id=pmid, retmode='xml', rettype='abstract')
#     return handle.read()
#
#
# file = (abstract(28593354))
# print(file)



# ARTICLE_URL = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&tool=PMA&id=29150897,32043525"
# ARTICLE_URL = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&tool=PMA&id=33786800"

# def main():
#     response = requests.get(ARTICLE_URL)
#     tree = etree.fromstring(response.content)
#     ids = tree.xpath("//MedlineCitation/PMID[@Version='1']")
#     titles = tree.xpath("//Article/ArticleTitle")
#     affiliation = tree.xpath("//AffiliationInfo/Affiliation")
#     if len(ids) != len(titles):
#         print("ID count doesn't match Title count...")
#         return
#     result = {_id.text: {"title": title.text, 'affiliation': affiliation[0].text} for _id, title in zip(ids, titles)}
#     pp(result)
#
#
# if __name__ == "__main__":
#     main()

# response = requests.get(ARTICLE_URL)
# tree = etree.fromstring(response.content)
# ids = tree.xpath("//MedlineCitation/PMID[@Version='1']")
# titles = tree.xpath("//Article/ArticleTitle")
# affiliations = tree.xpath("//AffiliationInfo/Affiliation")
# abstracts = tree.xpath("//Abstract/AbstractText")
#
# for title in titles:
#     print(title.text)
# print()
#
# compare = []
# for affiliation in affiliations:
#     if affiliation.text not in compare:
#         compare.append(affiliation.text)
#
# for i in compare:
#     print(i)
#
# for id in ids:
#     print(id.text)
#
# for abstract in abstracts:
#     print(abstract.text)
