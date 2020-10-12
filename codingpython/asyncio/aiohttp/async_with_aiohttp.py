import asyncio
import aiohttp


async def make_request(session, req_n):
    url = "https://baidu.com"
    async with session.get(url) as resp:
        if resp.status == 200:
            await resp.text()


async def main():
    n = 100
    print(f"Making {n} request with aiohttp.")
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[make_request(session, i) for i in range(n)])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
