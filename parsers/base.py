from abc import ABC, abstractmethod
from typing import List, Dict


class BaseParser(ABC):
    @abstractmethod
    def fetch_vacancies(self) -> List[Dict[str, str]]:
        """
        Fetches a list of vacancies.

        Returns:
            List[Dict[str, str]]: \
                A list of dictionaries containing vacancy details.
        """
        pass
