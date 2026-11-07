"""checks/m2/m2places.py: a copy of pipeline/places.py's matching rules as of e524840 (D3's #86), for the fifth pass's
check c34, so that the rule can be run again by M2 over the one-county questions and its every outcome compared with the
record. It is a copy (the orchestrator's brief allows a pipeline rule to be re-applied in M2's scripts where the copy
says so); it reads the two Census files from M2's own cache (checks/m2/fetch_fourth_pass.sh, whose sha256 c33 found
equal to the record's), not through pipeline/fetch.py. The functions and constants are those of places.py: load, match,
_goes_on, _county, _sub, _place; nothing is added but the file paths. M2's own, independent readings of the titles are in
c34 itself.
"""
import collections
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402

FOURTH = os.path.join(L.CACHE, "fourth")
PATH_PLACES = os.path.join(FOURTH, "census_places.txt")
PATH_COUSUB = os.path.join(FOURTH, "census_cousub.txt")

MCD_TOWNS = {"CT", "MA", "ME", "NH", "NY", "RI", "VT", "WI", "MN"}
KINDS = ("city and borough", "city", "town", "village", "borough", "municipality", "township")
_LSAD = re.compile(r"^(.*?) (city and borough|city|town|village|borough|municipality|township)$")
_TYPED = re.compile(r"\b(CITY|TOWN|VILLAGE|BOROUGH) OF\s+")
_KIND_WORDS = {"CITY", "TOWN", "VILLAGE", "BOROUGH"}
_NOT_PLACE = re.compile(r"\bSCHOOLS?\b|\bDISTRICT\b|\bDIST\b|\bUSD\b|\bISD\b|\bCISD\b|\bESD\b|\bHSD\b|\bUHSD\b|"
                        r"\bUNION (#|HSD|HS\b|NO\b)|\bBOE\b|BOARD OF EDUCATION|\bUNIFIED\b|\bCOLLEGE\b|\bESPLOST\b")
_COUNTY_WORD = re.compile(r"\bCOUNTY\b|\bPARISH\b")
_TOWNSHIP_WORD = re.compile(r"\bTOWNSHIP\b|\bTWP\b")
_SUB_LSAD = re.compile(r"^(.*?) (charter township|township|town|plantation|borough|city|village|gore|grant|location|"
                       r"purchase|reservation|unorganized territory)$")
_SUB_TYPED = re.compile(r"\b(CHARTER TOWNSHIP|TOWNSHIP|TOWN|PLANTATION) OF\s+")
_SUB_KIND = {"TOWN": {"TOWN"}, "TOWNSHIP": {"TOWNSHIP", "CHARTER TOWNSHIP"}, "TWP": {"TOWNSHIP", "CHARTER TOWNSHIP"},
             "CHARTER TOWNSHIP": {"CHARTER TOWNSHIP"}, "PLANTATION": {"PLANTATION"}}
_COUNTY_BODY = re.compile(r"\b(FIRE|HOSPITAL|LIBRARY|AUTHORITY|PORT|TRANSIT|WATER|SEWER|SANITARY|SANITATION|IRRIGATION|"
                          r"CEMETERY|DRAINAGE|LEVEE|CONSERVANCY|CONSERVATION|AIRPORT|MOSQUITO|CITY|CITIES|TOWN|"
                          r"TOWNSHIP|TWP|VILLAGE|BOROUGH|MUNICIPAL|MUNICIPALITY|WARD|PRECINCT|ZONE|AREA|BOARD|HEALTH|"
                          r"EDUCATION|EDUCATIONAL|UNINCORPORATED)\b")
_COUNTY_OWN_BOARD = re.compile(r"BOARD OF (COUNTY )?COMMISSIONERS|BOARD OF SUPERVISORS|COUNTY BOARD( OF [A-Z]+)?|"
                               r"BOARD OF COUNTY [A-Z]+")
_COUNTY_GOV = re.compile(r"\b(COUNTY|PARISH) OF\b|COUNTY COMMISSION|COMMISSIONERS|BOARD OF SUPERVISORS|POLICE JURY|"
                         r"PARISH COUNCIL\b|COUNTY COUNCIL\b|FISCAL COURT|COMMISSIONERS COURT|COUNTY LEGISLATURE|"
                         r"COUNTY BOARD|COUNTY GOVERNMENT|PARISH GOVERNMENT")
_SPECIAL = re.compile(r"\b(FIRE|HOSPITAL|LIBRARY|PORT|TRANSIT|WATER|SEWER|SANITARY|SANITATION|IRRIGATION|CEMETERY|"
                      r"AUTHORITY|AREA|REGIONAL|JOINT|CONSOLIDATED|PARK|RECREATION|UTILITY|UTILITIES|AMBULANCE|EMS|"
                      r"DRAINAGE|LEVEE|CONSERVANCY|AIRPORT|HEALTH|MOSQUITO)\b")
_OREGON_NO = re.compile(r"^\d+-\d+\s*:?\s*")
_AFTER_HYPHEN = re.compile(r"(QUESTION|PROP|PROPOSITION|MEASURE|ISSUE|BOND|REFERENDUM|SPECIAL|\d)")


def _plain(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return " ".join(s.upper().replace("'S", "S").split())


_cache = {}


def load():
    if "p" in _cache:
        return _cache["p"]
    places = collections.defaultdict(dict)
    county_names = collections.defaultdict(dict)
    with open(PATH_PLACES, encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("|")
        if head != ["STATE", "STATEFP", "COUNTYFP", "COUNTYNAME", "PLACEFP", "PLACENS", "PLACENAME", "TYPE",
                    "CLASSFP", "FUNCSTAT"]:
            raise SystemExit(f"places: the Census file's columns are not those read: {head}")
        for line in f:
            st, sfp, cfp, cname, pfp, _pns, pname, typ, _cls, fs = line.rstrip("\n").split("|")
            base_c = re.sub(r" (County|Parish|Borough|Census Area|Municipality|City and Borough|city)$", "", cname)
            county_names[st][_plain(base_c)] = sfp + cfp
            if typ != "INCORPORATED PLACE" or fs != "A":
                continue
            m = _LSAD.match(re.sub(r"\s*\(.*\)$", "", pname))
            name, kind = (m.group(1), m.group(2)) if m else (re.sub(r"\s*\(.*\)$", "", pname), "")
            p = places[st].setdefault((_plain(name), kind.upper()), {"geoid": sfp + pfp, "census_name": pname,
                                                                    "counties": {}})
            if p["geoid"] != sfp + pfp:
                p["ambiguous"] = True
            p["counties"][sfp + cfp] = cname
    subs = collections.defaultdict(lambda: collections.defaultdict(set))
    county_full = {}
    with open(PATH_COUSUB, encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("|")
        if head != ["STATE", "STATEFP", "COUNTYFP", "COUNTYNAME", "COUSUBFP", "COUSUBNS", "COUSUBNAME", "CLASSFP",
                    "FUNCSTAT"]:
            raise SystemExit(f"places: the Census county subdivision file's columns are not those read: {head}")
        for line in f:
            st, sfp, cfp, cname, cofp, _ns, sname, _cls, fs = line.rstrip("\n").split("|")
            base_c = re.sub(r" (County|Parish|Borough|Census Area|Municipality|City and Borough|city)$", "", cname)
            county_names[st].setdefault(_plain(base_c), sfp + cfp)
            county_full[sfp + cfp] = cname
            if fs != "A":
                continue
            m = _SUB_LSAD.match(sname)
            subs[st][_plain(m.group(1) if m else sname)].add((sfp + cfp, _plain(sname), (m.group(2) if m else "").upper(),
                                                              sfp + cfp + cofp, sname))
    _cache["p"] = (places, county_names, subs, None)
    _cache["county_full"] = county_full
    return _cache["p"]


def match(office, state, county):
    t = _OREGON_NO.sub("", _plain(office))
    if _NOT_PLACE.search(t):
        return None, "the title names a district or a school"
    if _COUNTY_WORD.search(t):
        return _county(t, state, county)
    if _TOWNSHIP_WORD.search(t):
        return _sub(t, state, county)
    found, why = _place(t, state, county)
    if found is None and (why.startswith("the title names no incorporated place") or why.startswith("the name is also")):
        f2, why2 = _sub(t, state, county)
        if f2 is not None or not why2.startswith("the title names no "):
            return f2, why2
        return None, "the title names no incorporated place or county subdivision of the state"
    return found, why


def _goes_on(n, rest, state):
    places, _, subs, _ = load()
    w = rest.replace(":", " ").replace(",", " ").split()[:1]
    if not w or not w[0][:1].isalpha():
        return None
    longer = f"{n} {w[0]}"
    names = {pn for pn, _ in places.get(state, {})} | set(subs.get(state, {}))
    return next((o for o in sorted(names) if o != n and o.startswith(longer)), None)


def _county(t, state, county):
    _, county_names, _, _ = load()
    tt = t.replace(".", "")
    own = [n.replace(".", "") for n, f in county_names[state].items() if f == county]
    hit = next((n for n in own if re.search(rf"\b{re.escape(n)}\s+(COUNTY|PARISH)\b|\b(COUNTY|PARISH) OF\s+"
                                             rf"{re.escape(n)}\b", tt)), None)
    if hit is None:
        return None, "the title names a county or parish, but not the record's own"
    part = re.search(rf"\b(NORTH|SOUTH|EAST|WEST|NORTHERN|SOUTHERN|EASTERN|WESTERN|CENTRAL|UPPER|LOWER)\s+"
                     rf"{re.escape(hit)}\s+(COUNTY|PARISH)\b", tt)
    if part:
        return None, f"the title names a part of the county ('{part.group(0)}')"
    rest = re.sub(rf"\b{re.escape(hit)}\s+(COUNTY|PARISH)\b|\b(COUNTY|PARISH) OF\s+{re.escape(hit)}\b", " ", tt)
    rest_words = " " + " ".join(re.sub(rf"\b{re.escape(hit)}\b", " ", rest).replace(",", " ").replace("(", " ")
                                .replace(")", " ").replace("-", " ").split()) + " "
    places, _, subs, _ = load()
    inside = {pn.replace(".", "") for (pn, _), v in places.get(state, {}).items() if county in v["counties"]}
    inside |= {n.replace(".", "") for n, xs in subs.get(state, {}).items() if any(x[0] == county for x in xs)}
    named = sorted(n for n in inside if len(n) >= 4 and f" {n} " in rest_words)
    if named:
        return None, f"the title names a place or town in the county as well ('{named[0]}')"
    for n, f in county_names[state].items():
        n = n.replace(".", "")
        if f != county and len(n) > 2 and re.search(rf"\b{re.escape(n)}\s+(COUNTY|PARISH)\b", rest):
            return None, "the title names another county or parish as well"
    paren = re.search(rf"\b{re.escape(hit)}\s+(COUNTY|PARISH)\s*\(([^)]*[A-Z][^)]*)\)", tt)
    if paren:
        return None, f"the title names something in parentheses after the county ('{paren.group(0)}')"
    body = _COUNTY_BODY.search(_COUNTY_OWN_BOARD.sub(" ", rest))
    if body:
        return None, f"the title names another body than the county ('{body.group(0)}')"
    name = _cache["county_full"].get(county, hit.title())
    return {"unit": "county", "place": name, "geoid": county, "county": county, "county_name": name,
            "how": f"the title names the record's own {'parish' if 'PARISH' in tt else 'county'}, {name}, and no "
                   f"other body", "mark": "stated" if _COUNTY_GOV.search(tt) else "inferred"}, None


def _sub(t, state, county):
    places, county_names, subs, _ = load()
    mine = subs.get(state, {})
    hit = None
    for m in _SUB_TYPED.finditer(t):
        words = t[m.end():].split()
        for n in range(min(6, len(words)), 0, -1):
            name = " ".join(words[:n]).strip(" .,-:;()")
            if name in mine:
                hit = ("stated", f"the title says '{m.group(1)} OF {name}'", name, _SUB_KIND[m.group(1)])
                break
        if hit:
            break
    if hit is None:
        m = re.match(r"^(.*?)\s+(CHARTER TOWNSHIP|TOWNSHIP|TWP|TOWN|PLANTATION)\b", t)
        if m and m.group(1).strip(" .,-:;()") in mine:
            name = m.group(1).strip(" .,-:;()")
            hit = ("stated", f"the title says '{name} {m.group(2)}'", name, _SUB_KIND[m.group(2)])
    if hit is None and not _TOWNSHIP_WORD.search(t):
        for n in sorted(mine, key=len, reverse=True):
            if any(cf == county for cf, *_ in mine[n]) and (t == n or t.startswith(n + " ") or t.startswith(n + ",")
                                                            or t.startswith(n + ":") or t.startswith(n + " -")
                                                            or t.startswith(n + "- ")):
                hit = ("inferred", f"the title begins with the town's or township's name '{n}'", n, None)
                break
        if hit:
            rest = t[len(hit[2]):]
            if _SPECIAL.search(rest):
                return None, f"the title names a special body after the name ('{_SPECIAL.search(rest).group(0)}')"
            w = rest.replace(":", " ").replace(",", " ").split()[:2]
            if len(w) == 2 and w[1] in _KIND_WORDS | {"TOWNSHIP"} and w[0] not in _KIND_WORDS:
                return None, f"the name goes on past the subdivision's ('{hit[2]} {w[0]} {w[1]}')"
            other = _goes_on(hit[2], rest, state)
            if other:
                return None, f"the name may go on into another's ('{other}')"
            if county_names[state].get(hit[2]) == county:
                return None, "a county of the same name is the record's county, so the county's own question is likelier"
    if hit is None:
        return None, "the title names no county subdivision of the state with a government of its own"
    mark, how, name, kinds = hit
    cands = [x for x in mine[name] if kinds is None or x[2] in kinds]
    here = [x for x in cands if x[0] == county]
    if not here:
        return None, "the town or township lies in another county than the record's"
    if len(here) > 1:
        return None, "the name is more than one town or township in the county"
    cf, full, kind, geoid, census_name = here[0]
    if kinds is None:
        pl = [v for (pn, _), v in places.get(state, {}).items() if pn == name and county in v["counties"]]
        if any(_plain(v["census_name"]) != full for v in pl):
            return None, ("the name is both a place's and a town's or township's in the county, and the title does "
                          "not say which")
    return {"unit": "county subdivision", "place": census_name, "geoid": geoid, "county": county,
            "county_name": _cache["county_full"].get(county, county), "how": how, "mark": mark}, None


def _place(t, state, county):
    places, county_names, subs, _ = load()
    mine = places.get(state, {})
    names = collections.defaultdict(list)
    for k, v in mine.items():
        names[k[0]].append((k, v))
    hit = None
    for m in _TYPED.finditer(t):
        kind, words = m.group(1), t[m.end():].split()
        for n in range(min(6, len(words)), 0, -1):
            name = " ".join(words[:n]).strip(" .,-:;()")
            if n == 1 and name not in names and "-" in name:
                name = name.split("-")[0]
            same = [(k, v) for k, v in names.get(name, ()) if k[1] == kind or (kind == "CITY" and k[1] == "")]
            if same:
                hit = ("stated", f"the title says '{kind} OF {name}'", same)
            elif names.get(name) and not (kind == "TOWN" and state in MCD_TOWNS):
                hit = ("inferred", f"the title says '{kind} OF {name}'; the Census calls it a "
                       f"{names[name][0][0][1].lower() or 'place'}", names[name])
            if hit:
                break
        if hit:
            break
    if hit is None:
        for n in sorted(names, key=len, reverse=True):
            if t == n or t.startswith(n + " ") or t.startswith(n + ",") or t.startswith(n + ":"):
                hit = ("inferred", f"the title begins with the place's name '{n}'", names[n])
                break
            if t.startswith(n + "- ") or t.startswith(n + " -"):
                hit = ("inferred", f"the title begins with the place's name '{n}'", names[n])
                break
            if t.startswith(n + "-"):
                if not _AFTER_HYPHEN.match(t[len(n) + 1:].strip()):
                    return None, f"the place's name '{n}' is joined by a hyphen to another name"
                hit = ("inferred", f"the title begins with the place's name '{n}'", names[n])
                break
        if hit is None:
            return None, "the title names no incorporated place of the state"
        n = hit[2][0][0][0]
        rest = t[len(n):]
        if _SPECIAL.search(rest):
            return None, f"the title names a special body after the place's name ('{_SPECIAL.search(rest).group(0)}')"
        w = rest.replace(":", " ").replace(",", " ").split()[:2]
        if w and w[0] in _KIND_WORDS and len(hit[2]) == 1 and w[0] != hit[2][0][0][1]:
            return None, f"the title's word '{w[0]}' after the name is not the place's kind"
        if len(w) == 2 and w[1] in _KIND_WORDS and w[0] not in _KIND_WORDS:
            return None, f"the name goes on past the place's ('{n} {w[0]} {w[1]}')"
        other = _goes_on(n, rest, state)
        if other:
            return None, f"the name may go on into another's ('{other}')"
        other = {full for cf, full, *_ in subs[state].get(n, ()) if cf == county} - {_plain(x[1]["census_name"])
                                                                                     for x in hit[2]}
        if other and not (w and len(hit[2]) == 1 and w[0] == hit[2][0][0][1]):
            return None, (f"the name is also a town's or township's in the county ({', '.join(sorted(other))}), "
                          "so the title does not show which holds the question")
        if county_names[state].get(n) == county:
            return None, "a county of the same name is the record's county, so the county's own question is likelier"
    mark, how, cands = hit
    if len(cands) > 1 or any(v.get("ambiguous") for _, v in cands):
        return None, "the name is more than one place in the state"
    (name, kind), p = cands[0]
    if len(p["counties"]) > 1:
        return None, f"the place lies in {len(p['counties'])} counties"
    if county not in p["counties"]:
        return None, "the place lies in another county than the record's"
    return {"unit": "place", "place": p["census_name"], "geoid": p["geoid"], "county": county,
            "county_name": p["counties"][county], "how": how, "mark": mark}, None
