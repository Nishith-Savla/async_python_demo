import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

import aiofiles
import aiohttp
import requests

from timer import timer, async_timer

# Specify the URL for the images
IMAGE_URL = "https://picsum.photos/200/300"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)23s | %(levelname)-8s | %(lineno)3d:%(funcName)-20s | %(message)s'
)


@timer
def download_images_sync(num_images: int):
    save_directory = "downloaded_images/sync"

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for i in range(1, num_images + 1):
        response = requests.get(IMAGE_URL)

        if response.ok:
            image_filename = f"{save_directory}/image_{i}.jpg"
            with open(image_filename, "wb") as file:
                file.write(response.content)
            logging.info(f"Downloaded image {i}")
        else:
            logging.info(f"Failed to download image {i}. Status code: {response.status_code}")


def download_image(session, i, save_directory):
    response = session.get(IMAGE_URL)

    if response.ok:
        image_filename = f"{save_directory}/image_{i}.jpg"
        with open(image_filename, "wb") as file:
            file.write(response.content)
        logging.info(f"Downloaded image {i}")
    else:
        logging.info(f"Failed to download image {i}. Status code: {response.status_code}")


@timer
def download_images_sync_session(num_images: int):
    save_directory = "downloaded_images/sync_session"

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    with requests.Session() as session:
        for i in range(1, num_images + 1):
            download_image(session, i, save_directory)


async def download_image_async(session: aiohttp.ClientSession, i, save_directory):
    response = await session.get(IMAGE_URL)

    if response.ok:
        image_filename = f"{save_directory}/image_{i}.jpg"
        async with aiofiles.open(image_filename, "wb") as file:
            await file.write(await response.read())
        logging.info(f"Downloaded image {i}")
    else:
        logging.info(f"Failed to download image {i}. Status code: {response.status}")


@async_timer
async def download_images_async(num_images: int):
    save_directory = "downloaded_images/async"

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, num_images + 1):
            tasks.append(
                asyncio.create_task(download_image_async(session, i, save_directory)))

        await asyncio.gather(*tasks)


@timer
def download_images_multithreading(num_images: int):
    save_directory = "downloaded_images/multithreading"

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=10) as executor:
            for i in range(1, num_images + 1):
                executor.submit(download_image, session, i, save_directory)


@timer
def download_images_multiprocessing(num_images: int):
    save_directory = "downloaded_images/multiprocessing"

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    with requests.Session() as session:
        with ProcessPoolExecutor() as executor:
            for i in range(1, num_images + 1):
                executor.submit(download_image, session, i, save_directory)


async def main():
    num_images = 50

    download_images_sync(num_images)
    download_images_sync_session(num_images)
    await download_images_async(num_images)
    download_images_multithreading(num_images)
    download_images_multiprocessing(num_images)


if __name__ == "__main__":
    asyncio.run(main())
