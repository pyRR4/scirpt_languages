import wikipedia


articleName = input("Enter name of article: ")
print(wikipedia.page(articleName).summary)
url = wikipedia.page(articleName).url
print(f'Url: {url}')
