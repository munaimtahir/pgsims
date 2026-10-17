#!/usr/bin/env python3
"""Replace only the PGSIMS site in a shared Caddyfile."""
import re
import sys
from pathlib import Path


def update_site(shared: str, site: str) -> str:
    starts = list(re.finditer(r"(?m)^[^\s#{}][^\n{}]*\{\s*$", shared))
    matches = [match for match in starts if "pgsims.alshifalab.pk" in re.split(r"[,\s]+", match.group().strip())]
    if len(matches) != 1:
        raise ValueError("Expected exactly one PGSIMS site block; refusing shared config update")
    start = matches[0].start()
    # Caddy site closing braces are unindented in the maintained shared config.
    end = re.search(r"(?m)^}\s*$", shared[matches[0].end():])
    if end is None:
        raise ValueError("Cannot find PGSIMS block boundary")
    stop = matches[0].end() + end.end()
    return shared[:start] + site.rstrip() + "\n" + shared[stop:]


if __name__ == "__main__":
    print(update_site(Path(sys.argv[1]).read_text(), Path(sys.argv[2]).read_text()), end="")
