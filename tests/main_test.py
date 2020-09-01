import pytest

from sanic.request import Request
from main import emojies_generator, handle
from httpx import Client


class Response:

    def __init__(self, status_code, text) -> None:
        self.text = text
        self.status_code = status_code


@pytest.fixture()
def client():
    return None


@pytest.fixture()
def response():
    return Response(200, 'привет привет при dtn привет привет привет')


@pytest.mark.asyncio
async def test_emojies_loop():
    emojies = ['😆', '💀', '😈', '👻', '🤘']
    gen = emojies_generator(emojies)

    em = next(gen)
    assert em == '😆'

    em = next(gen)
    assert em == '💀'

    em = next(gen)
    assert em == '😈'

    em = next(gen)
    assert em == '👻'

    em = next(gen)
    assert em == '🤘'

    em = next(gen)
    assert em == '😆'

    em = next(gen)
    assert em == '💀'

    em = next(gen)
    assert em != '👻'


@pytest.mark.asyncio
async def test_correct_replace(mocker, response):
    mocker.patch.object(Client, 'get', return_value=response)
    mocker.patch('main.get_emojies', return_value=[1, 2, 3, 4])

    r = Request(
        b'/test', headers={}, version=b'2.0', method=b'GET', transport=None, app='test'
    )
    route, handler = handle
    a = await handler(r, 'test_path')


    result = a.body.decode('utf8')
    assert result == 'привет1 привет2 при dtn привет3 привет4 привет1'

