"""This file is used to contact the api and download data from it"""

import requests
from tqdm import tqdm
import time


class ProductDownloader:
    """imports products from api"""

    url = "https://fr.openfoodfacts.org/cgi/search.pl"
    params = {
        "action": "process",
        "sort_by": "unique_scans_n",
        "page": 1,
        "page_size": 1000,
        "json": 1,
    }

    def request(self):
        # sends request to API

        return requests.get(self.url, params=self.params)

    def response(self):
        # stores response from API in a json format

        data = []
        for i in tqdm(range(0, 5)):
            time.sleep(0.3)
            self.params["page"] += 1
            try:
                response = self.request()
            except requests.ConnectionError:
                pass
            else:
                if response.status_code == 200:
                    data.append(response.json())
        return data
