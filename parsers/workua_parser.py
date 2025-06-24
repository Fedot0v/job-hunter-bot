from typing import List, Dict
import logging
import urllib.parse

from base import BaseParser
from playwright_manager import AsyncPlaywrightManager


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WorkUaVacancyParser:
    async def parse(self, page) -> Dict[str, str]:
        try:
            title_el = await page.query_selector("h1#h1-name")
            title = await title_el.inner_text() if title_el else ''

            company_el = await page.query_selector("a.inline span.strong-500")
            company = await company_el.inner_text() if company_el else ''

            salary_el = await page.query_selector("span.strong-500")
            salary = await salary_el.inner_text() if salary_el else ''

            location_el = await page.query_selector(
                "li.text-indent span.glyphicon-map-marker + *"
            )
            location = await location_el.inner_text() if location_el else ''

            experience_el = await page.query_selector(
                "li.text-indent span.glyphicon-tick + *"
            )
            experience = await experience_el.inner_text() if experience_el else ''

            languages_el = await page.query_selector(
                "li.text-indent span.glyphicon-language + *"
            )
            languages = await languages_el.inner_text() if languages_el else ''

            skills_elements = await page.query_selector_all(
                "ul.list-unstyled li.label-skill span.ellipsis"
            )
            skills = [await skill.inner_text() for skill in skills_elements]

            description_el = await page.query_selector("div#job-description")
            description = await description_el.inner_text() if description_el else ''

            return {
                "title": title.strip(),
                "company": company.strip(),
                "salary": salary.strip(),
                "location": location.strip(),
                "experience": experience.strip(),
                "languages": languages.strip(),
                "skills": skills,
                "description": description.strip(),
                "link": page.url
            }
        except Exception as e:
            logger.error(f"Ошибка при обработке вакансии: {e}")
            return {}


class WorkUaParser(BaseParser):
    BASE_URL = "https://www.work.ua/jobs-"

    def __init__(self, keyword: str, location: str = None):
        self.location = location
        self.keyword = keyword
        self.url = f"{self.BASE_URL}{self.location}-{self.keyword}" if location else f"{self.BASE_URL}{self.keyword}/"
        self.vacancy_parser = WorkUaVacancyParser()

    async def fetch_vacancies(self) -> List[Dict[str, str]]:
        vacancies = []
        try:
            async with AsyncPlaywrightManager() as page:
                await page.goto(self.url, wait_until="load")
                await page.wait_for_timeout(2000)

                links = await self._parse_all_pages(page)
                logger.info(f"Всього зібрано {len(links)} посилань на вакансії.")

                for link in links:
                    logger.info(f"Переход на вакансию: {link}")
                    await page.goto(link, wait_until="load")
                    await page.wait_for_timeout(2000)

                    vacancy = await self.vacancy_parser.parse(page)
                    if vacancy:
                        vacancies.append(vacancy)
        except Exception as e:
            logger.error(f"Помилка при парсингу Work.ua: {e}")
        return vacancies

    async def _parse_all_pages(self, page) -> List[str]:
        links = []
        while True:
            job_links = await page.query_selector_all(
                "#pjax-jobs-list div.card.job-link a[tabindex='-1']"
            )
            logger.info(
                f"Знайдено {len(job_links)} вакансій на сторінці {page.url}"
            )

            for job_link in job_links:
                href = await job_link.get_attribute("href")
                if href:
                    vacancy_url = urllib.parse.urljoin(
                        "https://www.work.ua",
                        href
                    )
                    links.append(vacancy_url)

            next_page = await page.query_selector(
                "a.link-icon:has-text('Наступна')"
            )
            if next_page:
                logger.info("Переход на следующую страницу...")
                await next_page.click()
                await page.wait_for_timeout(2000)
            else:
                logger.info("Последняя страница достигнута.")
                break
        return links
