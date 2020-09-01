from httpx import Client
import re

from sanic import Sanic, response

# I used Sanic because it provides async requests, plus async httpx requests to the website
#
# Use command to build image
# docker build -t uptest .
#
# To start project
# docker run --name upproxy uptest:latest
#
# Links on the haven't been replaced, because this manipulation is damaged css, js files.
# You must paste a link into the address bar. Like this (http://localhost:9000/topics/health/)
# You can use every link in the website and script will add beautiful emojies to the words.

app = Sanic('uptest')


# Better to use generator in case of long list of emojies
def emojies_generator(emojies):
    i = 0
    while True:
        try:
            yield emojies[i]
            i += 1
        except IndexError:
            i = 0


def get_emojies():
    return ['😆', '💀', '😈', '👻', '🤘']  # default emoji list


@app.route("<path_arg:path>")
async def handle(request, path_arg):
    gen = emojies_generator(get_emojies())

    def repl_func(match):
        em = next(gen)  # iterate over generator
        return f'{match.group()}{em}'  # prepare string

    with Client() as client:
        r = client.get(f'https://lifehacker.ru/{path_arg}')
        result = re.sub(r'(\b[а-яА-Я]{6}\b)', repl_func, r.text)  # Using regex to replace all boundaries with 6 russian letters
        return response.html(result, status=r.status_code)


if __name__ == '__main__':
    app.run('localhost', 9000, debug=True)
