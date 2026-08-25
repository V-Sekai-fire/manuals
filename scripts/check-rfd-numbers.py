#!/usr/bin/env python3
"""Check that every RFD number follows the org-qualified decimal rule.

RFD 2000 gives the rule. The number appears three times per RFD -- the
directory name, the `rfd:` front-matter field, and the `title:` string -- and
nothing checked that the three agreed until this script.

The numbers were hexadecimal for five days and are decimal now. Two citation
forms are therefore stale rather than one, and both are rejected by name. The
ALIASES.md checks are gone with the table: the decimal serial equals the
pre-hex number in every row it held, so an old number resolves by prepending
the organization digit rather than by a lookup.

Run --self-test to watch each check reject a known-bad tree. A gate that
passes on broken input certifies the defect instead of catching it.
"""
import os
import re
import sys

ORG = "2"
DIR_RE = re.compile(r"^([0-9]{4})-[a-z0-9-]+$")
FM_RE = re.compile(r'^rfd: "([0-9]{4})"', re.M)
TITLE_RE = re.compile(r'^title: "RFD ([0-9]{4}):', re.M)
# An old number always began with 0, and no organization digit is 0, so a
# leading zero is what tells an unmigrated citation from a valid new one.
OLD_CITE_RE = re.compile(r"\bRFD (0\d{3})\b")
# The other withdrawn form. Only a hex serial carries a letter, and a number
# that is four digits under an organization digit is current.
HEX_CITE_RE = re.compile(r"\bRFD ([1-9][0-9a-f]{0,2}[a-f][0-9a-f]*)\b")


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
            # This script holds both withdrawn forms in its own fixtures.
            if os.path.abspath(p) == me:
                continue
            try:
                with open(p, encoding="utf-8", errors="ignore") as fh:
                    body = fh.read()
            except OSError:
                continue
            for m in OLD_CITE_RE.finditer(body):
                problems.append(f"{p}: cites RFD {m.group(1)} in the first decimal form")
            for m in HEX_CITE_RE.finditer(body):
                problems.append(f"{p}: cites RFD {m.group(1)} in the withdrawn hex form")

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

    return problems


def self_test():
    import shutil
    import tempfile

    def build(tmp, dirname="2001-a-slug", fm="2001", title="2001", extra=None, link=""):
        d = os.path.join(tmp, "rfd", dirname)
        os.makedirs(d)
        with open(os.path.join(d, "index.md"), "w", encoding="utf-8") as fh:
            fh.write(f'---\ntitle: "RFD {title}: A slug"\nrfd: "{fm}"\nstate: published\n---\n{link}')
        if extra:
            with open(os.path.join(tmp, "note.md"), "w", encoding="utf-8") as fh:
                fh.write(extra)

    cases = [
        ("a clean tree passes", {}, False),
        ("wrong organization digit", {"dirname": "1001-a-slug"}, True),
        ("no organization digit", {"dirname": "0001-a-slug"}, True),
        # The two withdrawn forms, each rejected by name rather than by the
        # slug pattern happening to miss.
        ("a hex directory name", {"dirname": "200a-a-slug"}, True),
        ("a hex number in the front matter",
         {"dirname": "2010-a-slug", "fm": "200a", "title": "2010"}, True),
        ("front matter disagrees with directory", {"fm": "2002"}, True),
        ("title disagrees with directory", {"title": "2002"}, True),
        ("a citation in the first decimal form", {"extra": "see RFD 0021\n"}, True),
        ("a citation in the withdrawn hex form", {"extra": "see RFD 200a\n"}, True),
        ("a link to a folder that moved", {"link": "see [x](../2099-gone/index.md)\n"}, True),
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
