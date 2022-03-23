import asyncio
import json
import os
import typing
import warnings

import pytest

import genshin


@pytest.fixture(scope="session")
def event_loop():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        loop = asyncio.get_event_loop()

    yield loop
    loop.close()


@pytest.fixture(scope="session")
def cookies() -> typing.Mapping[str, str]:
    try:
        return {"ltuid": os.environ["LTUID"], "ltoken": os.environ["LTOKEN"]}
    except KeyError:
        pytest.exit("No cookies set", 1)
        return {}


@pytest.fixture(scope="session")
def browser_cookies() -> typing.Mapping[str, str]:
    try:
        return genshin.utility.get_browser_cookies()
    except Exception:
        return {}


@pytest.fixture(scope="session")
def chinese_cookies() -> typing.Mapping[str, str]:
    try:
        return {"ltuid": os.environ["CN_LTUID"], "ltoken": os.environ["CN_LTOKEN"]}
    except KeyError:
        warnings.warn("No chinese cookies were set for tests")
        return {}


@pytest.fixture(scope="session")
def local_chinese_cookies() -> typing.Mapping[str, str]:
    try:
        return {
            "account_id": os.environ["LCN_ACCOUNT_ID"],
            "cookie_token": os.environ["LCN_COOKIE_TOKEN"],
        }
    except KeyError:
        return {}


@pytest.fixture(scope="session")
async def client(cookies: typing.Mapping[str, str]):
    """Return a client with environment cookies."""
    client = genshin.Client()
    client.debug = True
    client.set_cookies(cookies)
    client.set_cache()

    yield client

    # dump the entire cache into a json file
    assert isinstance(client.cache, genshin.Cache)

    cache = {str(key): value for key, (_, value) in client.cache.cache.items()}

    os.makedirs(".pytest_cache", exist_ok=True)
    with open(".pytest_cache/hoyo_cache.json", "w") as file:
        json.dump(cache, file, indent=4)


@pytest.fixture(scope="session")
async def lclient(browser_cookies: typing.Mapping[str, str]):
    """Return the local client."""
    if not browser_cookies:
        pytest.skip("Skipped local test")

    client = genshin.Client()
    client.debug = True
    client.default_game = genshin.Game.GENSHIN
    client.set_cookies(browser_cookies)
    client.set_authkey()

    return client


@pytest.fixture(scope="session")
async def cnclient(chinese_cookies: typing.Mapping[str, str]):
    """Return the client with chinese cookies."""
    if not chinese_cookies:
        pytest.skip("Skipped chinese test")

    client = genshin.Client()
    client.region = genshin.types.Region.CHINESE
    client.debug = True
    client.set_cookies(chinese_cookies)

    return client


@pytest.fixture(scope="session")
async def lcnclient(local_chinese_cookies: typing.Mapping[str, str]):
    """Return the local client with chinese cookies."""
    if not local_chinese_cookies:
        pytest.skip("Skipped local chinese test")
        return

    client = genshin.Client()
    client.region = genshin.types.Region.CHINESE
    client.debug = True
    client.set_cookies(local_chinese_cookies)

    return client


@pytest.fixture(scope="session")
def genshin_uid():
    return 710785423


@pytest.fixture(scope="session")
def honkai_uid():
    return 200365120


@pytest.fixture(scope="session")
def hoyolab_uid():
    return 8366222


@pytest.fixture(scope="session")
def genshin_cnuid():
    return 101322963


@pytest.fixture(scope="session")
def miyoushe_uid():
    return 75276539


def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--cooperative", action="store_true")


def pytest_collection_modifyitems(items: typing.List[pytest.Item], config: pytest.Config):
    if config.option.cooperative:
        for item in items:
            if isinstance(item, pytest.Function) and asyncio.iscoroutinefunction(item.obj):
                item.add_marker("asyncio_cooperative")

    for index, item in enumerate(items):
        if "reserialization" in item.name:
            break
    else:
        return items

    item = items.pop(index)
    items.append(item)

    return items
