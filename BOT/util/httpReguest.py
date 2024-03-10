import aiohttp


async def fetch_data_get(endpoint, query=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:8000/{endpoint}', params=query) as response:
            return await response.json()

async def fetch_data_post(endpoint, query=None):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'http://localhost:8000/{endpoint}', params=query) as response:
            return await response.json()