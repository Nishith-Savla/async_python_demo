import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from json import JSONDecodeError

import aiohttp
import requests
from aiohttp import ContentTypeError

from timer import timer, async_timer

URL = 'https://httpbin.org/uuid'
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)23s | %(levelname)-8s | %(lineno)3d:%(funcName)-20s | %(message)s'
)


def fetch(url) -> str | None:
    with requests.get(url) as response:
        try:
            json_response = response.json()
            return json_response['uuid']
        except JSONDecodeError as e:
            logging.error(e.msg)
            return None


def fetch_session(session: requests.Session, url: str) -> str | None:
    with session.get(url) as response:
        try:
            json_response = response.json()
            return json_response['uuid']
        except JSONDecodeError as e:
            logging.error(e.msg)
            return None


async def async_fetch(session: aiohttp.ClientSession, url) -> str | None:
    async with session.get(url) as response:
        try:
            json_response = await response.json()
            return json_response['uuid']
        except ContentTypeError as e:
            logging.error(e.message)
            return None


@timer
def get_uuids_sync(n: int):
    uuids = [fetch(URL) for _ in range(n)]
    logging.info(uuids)


@timer
def get_uuids_sync_session(n: int):
    with requests.Session() as session:
        uuids = [fetch_session(session, URL) for _ in range(n)]
    logging.info(uuids)


@async_timer
async def get_uuids_async(n: int):
    async with aiohttp.ClientSession() as session:
        tasks = [async_fetch(session, URL) for _ in range(n)]
        uuids = await asyncio.gather(*tasks)
    logging.info(uuids)


@async_timer
async def get_uuids_async_create_task(n: int):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(async_fetch(session, URL)) for _ in range(n)]
        uuids = await asyncio.gather(*tasks)
    logging.info(uuids)


@timer
def get_uuids_multithreading(n: int):
    with requests.Session() as session:
        with ThreadPoolExecutor() as executor:
            uuids = list(executor.map(fetch_session, [session] * n, [URL] * n))

    logging.info(uuids)


@timer
def get_uuids_multiprocessing(n: int):
    with requests.Session() as session:
        with ProcessPoolExecutor() as executor:
            uuids = list(executor.map(fetch_session, [session] * n, [URL] * n))

    logging.info(uuids)


async def main():
    n = 1000

    get_uuids_sync(n)
    get_uuids_sync_session(n)
    await get_uuids_async(n)
    await get_uuids_async_create_task(n)
    get_uuids_multithreading(n)
    get_uuids_multiprocessing(n)


if __name__ == '__main__':
    asyncio.run(main())
