import requests
def get_year_info(year):
    url = f"http://numbersapi.com/{year}/year"
    response = requests.get(url)
    if response:
        return response.text

def get_question(count):
    url = f"http://jservice.io/api/random?count={count}"
    response = requests.get(url)
    if response:
        return response.json()

def get_dog():
    url = "https://random.dog/woof.json"
    response = requests.get(url)
    if response:
        return response.json()["url"]

def get_fox():
    url = "https://randomfox.ca/floof/"
    response = requests.get(url)
    if response:
        return response.json()