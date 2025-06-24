import asyncio
from workua_parser import WorkUaParser


async def main():
    parser = WorkUaParser(keyword="python")
    jobs = await parser.fetch_vacancies()
    for job in jobs:
        print(f"{job['title']} | {job['company']} | {job['salary']} | {job['link']} | {job['location']}")

if __name__ == "__main__":
    asyncio.run(main())
