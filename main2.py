import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from collections import defaultdict
import plotly.express as px

polaridade_por_autor = defaultdict(lambda: {'polaridade_acumulada': 0, 'num_frases': 0, 'frases': []})
frases_polaridades = []

for x in range(1, 11):
    url = f'https://quotes.toscrape.com/page/{x}'
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        frases = soup.find_all('span', class_='text')
        autores = soup.find_all('small', class_='author')

        for i in range(len(frases)):
            autor = autores[i].text
            frase = frases[i].text
            polaridade = TextBlob(frase).sentiment.polarity

            polaridade_por_autor[autor]['polaridade_acumulada'] += polaridade
            polaridade_por_autor[autor]['num_frases'] += 1
            polaridade_por_autor[autor]['frases'].append((frase, polaridade))

            frases_polaridades.append((frase, polaridade, autor))

    else:
        print("Falha, status: {}".format(response.status_code))

autores_lista = list(polaridade_por_autor.keys())
media_polaridade = [polaridade_por_autor[autor]['polaridade_acumulada'] / polaridade_por_autor[autor]['num_frases'] for autor in autores_lista]

autor_mais_positivo = max(polaridade_por_autor, key=lambda autor: media_polaridade[autores_lista.index(autor)])
autor_mais_negativo = min(polaridade_por_autor, key=lambda autor: media_polaridade[autores_lista.index(autor)])

frase_mais_positiva = max(frases_polaridades, key=lambda x: x[1])
frase_mais_negativa = min(frases_polaridades, key=lambda x: x[1])

print('\nResultados:')
print(f'\nAutor mais positivo: {autor_mais_positivo} | Polaridade: {max(media_polaridade):.4f}')
print(f'Autor mais negativo: {autor_mais_negativo} | Polaridade: {min(media_polaridade):.4f}')
print(f'\nFrase mais positiva ({frase_mais_positiva[2]}): {frase_mais_positiva[0]} | Polaridade: {frase_mais_positiva[1]:.4f}')
print(f'Frase mais negativa ({frase_mais_negativa[2]}): {frase_mais_negativa[0]} | Polaridade: {frase_mais_negativa[1]:.4f}')

frases, polaridades, autores = zip(*frases_polaridades)
fig = px.scatter(x=range(1, len(frases) + 1), y=polaridades, labels={'x': 'Frases', 'y': 'Polaridade'}, color=autores)
fig.update_layout(title='Polaridade de Todas as Frases', xaxis_title='Frases', yaxis_title='Polaridade')
fig.show()




