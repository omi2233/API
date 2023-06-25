from flask import Flask, request, jsonify
from googlesearch import search
from bs4 import BeautifulSoup
import requests
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import nltk
import json
from functools import wraps

app = Flask(__name__)

# Load cache from file
cache_file = "cache.json"
try:
    with open(cache_file, "r") as f:
        cache = json.load(f)
except FileNotFoundError:
    cache = {}


def perform_search(query):
    try:
        print('\nSearching web .........\n\n')
        results = list(search(query, num_results=6))
        return results
    except Exception as e:
        print("An error occurred during the search:", e)
        return []


def summarize_text(text):
    try:
        print("Summarizing and preparing the content to display ...........\n\n")
        sentences = sent_tokenize(text)
        word_frequencies = FreqDist([word for word in text.lower().split() if word not in stopwords.words('english')])
        ranking = {}
        for i, sentence in enumerate(sentences):
            for word in sentence.lower().split():
                if word in word_frequencies:
                    if i in ranking:
                        ranking[i] += word_frequencies[word]
                    else:
                        ranking[i] = word_frequencies[word]

        sorted_sentences = sorted(ranking, key=ranking.get, reverse=True)
        top_sentences = sorted_sentences[:3]
        summary = ' '.join([sentences[i] for i in top_sentences])
        return summary
    except Exception as e:
        print("An error occurred during text summarization:", e)
        return ""


def verify_api_key(api_key):
    # Implement your API key verification logic here
    # For example, you can check if the provided API key is valid in your system/database
    valid_keys = [""vsl9mIA6iE4oOFHH0thVF3xGZG0qoKYJ" , "17PQTCLANahhXLgq0661JVmNrODJiVSs" , "jQIOVptq8hfLQtmxvnFlwogtQkcdAwH2" , "0k7qAd81n3eNufg00RaDJPrRHvJfWpmb" , "6YYTbaufTj37ZcMisHzklW68uG1mrMgn" , "fgQtFlL0tmfbGijdWGEFiswJbkseD6Ph" , "4RIMTiknY67teLFTuA7fKgimyGasdhKB" , "4q563OvgstHOftOcorS6ngDA6z06ZgoN" , "XxzOEXrY1kehkkePYGpHrDvEZ8j15CZ2" , "cKH4uUvxWCG8Vfo0ajTg1A7I4vrQyAQp" , "lsCFHxPDf0Yqdl5gNhhnInotUcvrV1pI" , "8EHxWRyatnkMCMsJMnFRk79q2isihe79" , "3nr8FH7GAOgs5AegfnbYru3SeokzoQa7" , "FhLHSsvNiBfiNnYCOoR2hwCH0bXoVw3Q" , "QlEwyoOjlooyCWqWR1sKiDL5CDidAsGS" , "hIx8khxEvN8kSH0m9QkN4JxidlwrG91v" , "Yd1BAy1CeHBqC8dGDFcvYqjzZa1hGHQm" , "qXAbiMnZWj5TpeyfG332QgQPjPzfdB6p" , "4gWebE1G6emNw5fCs04WAFiOkIU5rBnP" , "Rn72Sfig5kCPJlTNuwn7l3KIEo0rdbHl" , "SNDLqmhvwJcjO9BI4ENX4uF8JA3aFJ6d" , "izseV7UrQeIMRe50YLWuae55BhaxkbR4" , "5s8B70PPxd4uUnYoXDIIJ9lAefMhi8wj" , "Rmf2KRg4ilm6UIZFx4rAv3eGvab36ste" , "c54N0tt0pKRP983LDetZGWHymG9B0tZR" , "3E51Gt9dTist9DWL7gk7QErL4DZcx72S" , "2TC4oSfcdMpa5WRsFGbmgEX3H2qtkqXW" , "Nq0j4A7aB45lc1b08Pr3HeCIO4x2JhoH" , "jUIiNr0vBcuqfpp7lOe8IjFZbIejmUiM" , "OQpS54qhTutyjAAzpTjA1qzDYVxhMBJ0" , "vEFK1CaHhWT7ZrZ1QXduqQFs0DoiRkPG" , "UsEC3d72s7nglzuBG9i7bWQrkqBwCiVI" , "azgJomwRqfF6bHBYGvMeQMWMjXXU8GBv" , "tjfRKdSRmLHd7orrfK5elKusxwOhp1rA" , "5XWzY26TKi4RpptGlEBvWo4OMWiSefnJ" , "EuLmhilLZNxZMPHEnoFuI13DEt7zT5bX" , "JTr0V0YoeCIDfSVOeyzJ2S2scqQilsdA" , "RsiYasZ69EAuLWsezEtibW779YRsXdMw" , "6ssQSJaVeoVslyVkBqsTM4vCgp9N1kJr" , "MksELsDaN1AcSamqKh4PP5qh0UV9Evrh" , "R3U5pKeqZSJ767c062pUbJ4RoA0gKohz" , "Sgdxw2SCR6X5QoraU8GOAwjMNGt1rXaC" , "PfP5mkSKe2AXbDtjPW0ZnsINMCugIBdM" , "FoYK6RMCSzHJQsTSAYGiX92Ax3RZb97w" , "xMn6rukdBpGuJpliDdbBrnFfINBZ2kDY" ] 
    return api_key in valid_keys


def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.args.get('api_key')
        if not api_key:
            return jsonify({'error': 'API key is missing.'}), 400
        if not verify_api_key(api_key):
            return jsonify({'error': 'Invalid API key.'}), 401
        return f(*args, **kwargs)

    return decorated_function


@app.route('/search', methods=['GET'])
@api_key_required
def search_api():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is missing.'}), 400

    if query in cache:
        return jsonify({'summary': cache[query]})

    results = perform_search(query)
    text = ""
    if results:
        print('Getting content...........\n\n')
        for url in results[:3]:
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                paragraphs = soup.find_all('p')
                for paragraph in paragraphs:
                    text += paragraph.text
            except Exception as e:
                print("An error occurred while scraping the web page:", e)
    if text:
        summary = summarize_text(text)
        cache[query] = summary
        with open(cache_file, "w") as f:
            json.dump(cache, f)
        return jsonify({'summary': summary})
    else:
        return jsonify({'error': 'No content found for the search query.'}), 404


if __name__ == '__main__':

    app.run()
