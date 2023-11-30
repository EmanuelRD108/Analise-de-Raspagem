import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

for x in range(10):
    url = f'https://quotes.toscrape.com/page/{x}'
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        frases = soup.find_all('span', class_='text')
        autores = soup.find_all('small', class_='author')


        for i in range(len(frases)):
            print(autores[i].text, ":", frases[i].text, "Polaridade: ", TextBlob(frases[i].text).sentiment.polarity)

    else:
            print("Falha, status:{}".format(response.status_code))

    print(response)
