#!/usr/bin/env python3
"""Check that every RFD number follows the org-qualified hex rule.

RFD 2000 gives the rule. The number appears three times per RFD -- the
directory name, the `rfd:` front-matter field, and the `title:` string -- and
nothing checked that the three agreed until this script.

Run --self-test to watch each check reject a known-bad tree. A gate that
passes on broken input certifies the defect instead of catching it.
"""
import os
import re
import sys

ORG = "2"
DIR_RE = re.compile(r"^([0-9a-f]{4})-[a-z0-9-]+$")
FM_RE = re.compile(r'^rfd: "([0-9a-f]{4})"', re.M)
TITLE_RE = re.compile(r'^title: "RFD ([0-9a-f]{4}):', re.M)
# An old number always began with 0, and no organization digit is 0, so a
# leading zero is what tells an unmigrated citation from a valid new one.
OLD_CITE_RE = re.compile(r"\bRFD (0\d{3})\b")


def check(root):
    problems = []
    rfd_root = os.path.join(root, "rfd")
    if not os.path.isdir(rfd_root):
        return ["no rfd/ directory"]
    dirs = sorted(
        d for d in os.listdir(rfd_root)
        if os.path.isdir(os.path.join(rfd_root, d)) and re.match(r"^[0-9a-zA-Z]{4}-", d)
    )
    if not dirs:
        problems.append("no RFD directories found, which is never correct here")

    seen = {}
    for d in dirs:
        m = DIR_RE.match(d)
        if not m:
            problems.append(f"{d}: not four lower-case hex digits and a slug")
            continue
        num = m.group(1)
        if num[0] != ORG:
            problems.append(f"{d}: organization digit is {num[0]}, not {ORG}")
        if num in seen:
            problems.append(f"{d}: serial {num} already used by {seen[num]}")
        seen[num] = d

        index = os.path.join(rfd_root, d, "index.md")
        if not os.path.exists(index):
            problems.append(f"{d}: has no index.md")
            continue
        with open(index, encoding="utf-8", errors="ignore") as fh:
            body = fh.read()
        fm = FM_RE.search(body)
        if not fm:
            problems.append(f"{d}: front matter has no four-hex-digit rfd: field")
        elif fm.group(1) != num:
            problems.append(f"{d}: rfd: is {fm.group(1)}, directory says {num}")
        ti = TITLE_RE.search(body)
        if not ti:
            problems.append(f"{d}: title does not start 'RFD <num>:'")
        elif ti.group(1) != num:
            problems.append(f"{d}: title says {ti.group(1)}, directory says {num}")

    me = os.path.abspath(__file__)
    for cur, _, files in os.walk(root):
        parts = cur.split(os.sep)
        if ".git" in parts or "__pycache__" in parts or "_site" in parts:
            continue
        for f in files:
            p = os.path.join(cur, f)
            # ALIASES.md holds old numbers on purpose; this script holds them
            # in its own negative-control fixtures.
            if f == "ALIASES.md" or os.path.abspath(p) == me:
                continue
            try:
                with open(p, encoding="utf-8", errors="ignore") as fh:
                    body = fh.read()
            except OSError:
                continue
            for m in OLD_CITE_RE.finditer(body):
                problems.append(f"{p}: cites RFD {m.group(1)} in the old decimal form")

    # A relative link to a renamed folder is consumed by scripts/decision-meta.py,
    # which swallows errors, so a broken one is silent rather than fatal.
    for cur, _, files in os.walk(rfd_root):
        for f in files:
            if not f.endswith(".md"):
                continue
            p = os.path.join(cur, f)
            with open(p, encoding="utf-8", errors="ignore") as fh:
                body = fh.read()
            for m in re.finditer(r"\]\(\.\./([0-9a-zA-Z]{4}-[a-z0-9-]+)/", body):
                if not os.path.isdir(os.path.join(rfd_root, m.group(1))):
                    problems.append(f"{p}: links to ../{m.group(1)}/ which does not exist")

    aliases = os.path.join(root, "ALIASES.md")
    if not os.path.exists(aliases):
        problems.append("ALIASES.md is missing, so old numbers do not resolve")
    else:
        with open(aliases, encoding="utf-8") as fh:
            mapped = set(re.findall(r"RFD ([0-9a-f]{4})", fh.read()))
        for num in sorted(seen):
            if num not in mapped:
                problems.append(f"ALIASES.md has no row for RFD {num}")
    return problems


def self_test():
    import shutil
    import tempfile

    def build(tmp, dirname="2001-a-slug", fm="2001", title="2001", extra=None,
              aliases="| RFD 0001 | RFD 2001 |\n", link=""):
        d = os.path.join(tmp, "rfd", dirname)
        os.makedirs(d)
        with open(os.path.join(d, "index.md"), "w", encoding="utf-8") as fh:
            fh.write(f'---\ntitle: "RFD {title}: A slug"\nrfd: "{fm}"\nstate: published\n---\n{link}')
        with open(os.path.join(tmp, "ALIASES.md"), "w", encoding="utf-8") as fh:
            fh.write(aliases)
        if extra:
            with open(os.path.join(tmp, "note.md"), "w", encoding="utf-8") as fh:
                fh.write(extra)

    cases = [
        ("a clean tree passes", {}, False),
        ("wrong organization digit", {"dirname": "1001-a-slug"}, True),
        ("decimal directory name", {"dirname": "0001-a-slug"}, True),
        ("front matter disagrees with directory", {"fm": "2002"}, True),
        ("title disagrees with directory", {"title": "2002"}, True),
        ("an unmigrated decimal citation", {"extra": "see RFD 0021\n"}, True),
        ("a link to a folder that moved", {"link": "see [x](../2099-gone/index.md)\n"}, True),
        ("ALIASES.md missing the row", {"aliases": "| RFD 9999 |\n"}, True),
    ]
    ok = True
    for name, kw, should_fail in cases:
        tmp = tempfile.mkdtemp()
        try:
            build(tmp, **kw)
            failed = bool(check(tmp))
            if failed != should_fail:
                ok = False
            mark = "ok " if failed == should_fail else "BAD"
            print(f"  {mark} {name}: {'rejected' if failed else 'accepted'}")
        finally:
            shutil.rmtree(tmp)
    return 0 if ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        print("self-test: each known-bad tree must be rejected")
        sys.exit(self_test())
    found = check(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for line in found:
        print(line)
    print(f"{len(found)} problems")
    sys.exit(1 if found else 0)
