"""pipeline/places.py: which MEDSL local questions held in one county can be counted whole, by the place their
title names and the Census Bureau's place-to-county relationship file.

Written 2026-11-07 by worker D3, on the orchestrator's word (item 5 of the order of 2026-11-07): "The 4,346
one-county titles: count one whole only where the place it names lies entirely within that county, by the Census
Bureau's place-to-county relationship file. Hold the rest." Reason (the orchestrator): "a question can sit in one
county's file only because another county's file is missing it." A place that lies wholly in one county cannot have
voters in another, so its question's count in that county is the whole count.

Source. U.S. Census Bureau, 2020 Census, "national_place_by_county2020.txt" (codes2020: each place, incorporated or
census designated, once for each county it lies in; pipe-delimited, UTF-8; columns STATE, STATEFP, COUNTYFP,
COUNTYNAME, PLACEFP, PLACENS, PLACENAME, TYPE, CLASSFP, FUNCSTAT), a work of the U.S. Government (17 U.S.C. 105).
Its counties are those of 2020: a place's county for a question of 2016-2024 is that [measured] for 2020 and
[inferred] for the other years (a place that annexed land across a county line after or before 2020 would not show).

How a title names a place (match()):
  stated    the title says "CITY OF X", "TOWN OF X", "VILLAGE OF X" or "BOROUGH OF X", and the state has one
            incorporated place named X of that kind (Census: "X city", "X town", ...).
  inferred  the title begins with an incorporated place's name ("SALEM - MEASURE 24-401"), after an Oregon measure
            number ("24-401:") is taken off; it says no "CITY OF", so that it is the place's question is read.
Only active incorporated places are read (TYPE "INCORPORATED PLACE", FUNCSTAT "A"): a census designated place has no
government to put a question, and a consolidated city's balance (FUNCSTAT "F") is not a place of its own.

Held, with the reason recorded (every one is a guard found in D3's trial on the 2016-2024 records, REPORT section 22):
  - a title naming a school or other district, a county, a parish or a township: the body that holds the question
    is not the place, and its lines need not be the place's ("STEVENSVILLE ELEMENTARY SCHOOL DISTRICT").
  - a title naming a special body after a place's name (fire, hospital, library, port, transit, water ...), for an
    inferred match only: such bodies often reach past the place.
  - a place's name joined to another by a hyphen ("CALDWELL-WEST CALDWELL"): a joint body of two places.
  - for an inferred match, a county of the same name as the place being the record's county ("GREENVILLE" in
    Greenville County): the county's own question is the likelier reading; or a word of kind after the name that
    is not the place's kind ("KENAI PENINSULA BOROUGH" is not Kenai city).
  - a name that is more than one place in the state.
  - a place that lies in more than one county, or in another county than the record's.
  - a retention: a judge is retained by a court's district, not a place.
"""
import collections
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch as F  # noqa: E402

URL = "https://www2.census.gov/geo/docs/reference/codes2020/national_place_by_county2020.txt"
NAME = "census/national_place_by_county2020.txt"
URL_COUSUB = "https://www2.census.gov/geo/docs/reference/codes2020/national_cousub2020.txt"
NAME_COUSUB = "census/national_cousub2020.txt"
# states whose towns are county subdivisions (minor civil divisions), not places: 'TOWN OF X' there is the town, not
# a village or city of the same name inside it (the Town of Poughkeepsie is not the City of Poughkeepsie)
MCD_TOWNS = {"CT", "MA", "ME", "NH", "NY", "RI", "VT", "WI", "MN"}
LICENCE = "a work of the U.S. Government (17 U.S.C. 105); no licence printed"
TITLE = ("U.S. Census Bureau, 2020 Census: national_place_by_county2020.txt (each place once for each county it lies "
         "in; codes2020 reference files)")
TITLE_COUSUB = ("U.S. Census Bureau, 2020 Census: national_cousub2020.txt (each county subdivision with its county; "
                "codes2020 reference files): towns and townships with a government of their own (FUNCSTAT A), which "
                "nest within their county, and the names that are both a place's and a subdivision's")

KINDS = ("city and borough", "city", "town", "village", "borough", "municipality", "township")
_LSAD = re.compile(r"^(.*?) (city and borough|city|town|village|borough|municipality|township)$")
_TYPED = re.compile(r"\b(CITY|TOWN|VILLAGE|BOROUGH) OF\s+")
_KIND_WORDS = {"CITY", "TOWN", "VILLAGE", "BOROUGH"}
# the body that holds the question is not the place
_NOT_PLACE = re.compile(r"\bSCHOOLS?\b|\bDISTRICT\b|\bDIST\b|\bUSD\b|\bISD\b|\bCISD\b|\bESD\b|\bHSD\b|\bUHSD\b|"
                        r"\bUNION (#|HSD|HS\b|NO\b)|\bBOE\b|BOARD OF EDUCATION|\bUNIFIED\b|\bCOLLEGE\b|\bESPLOST\b")
_COUNTY_WORD = re.compile(r"\bCOUNTY\b|\bPARISH\b")
_TOWNSHIP_WORD = re.compile(r"\bTOWNSHIP\b|\bTWP\b")
# a county subdivision's kinds, as the Census writes them after the name ('Avon town', 'Clinton charter township')
_SUB_LSAD = re.compile(r"^(.*?) (charter township|township|town|plantation|borough|city|village|gore|grant|location|"
                       r"purchase|reservation|unorganized territory)$")
_SUB_TYPED = re.compile(r"\b(CHARTER TOWNSHIP|TOWNSHIP|TOWN|PLANTATION) OF\s+")
_SUB_KIND = {"TOWN": {"TOWN"}, "TOWNSHIP": {"TOWNSHIP", "CHARTER TOWNSHIP"}, "TWP": {"TOWNSHIP", "CHARTER TOWNSHIP"},
             "CHARTER TOWNSHIP": {"CHARTER TOWNSHIP"}, "PLANTATION": {"PLANTATION"}}
# words of another body than the county (the orchestrator, 15:43: "district, school, hospital, fire, library, authority,
# board other than the county's own, and so on"); read on the title with the county's own name taken out
_COUNTY_BODY = re.compile(r"\b(FIRE|HOSPITAL|LIBRARY|AUTHORITY|PORT|TRANSIT|WATER|SEWER|SANITARY|SANITATION|IRRIGATION|"
                          r"CEMETERY|DRAINAGE|LEVEE|CONSERVANCY|CONSERVATION|AIRPORT|MOSQUITO|CITY|CITIES|TOWN|"
                          r"TOWNSHIP|TWP|VILLAGE|BOROUGH|MUNICIPAL|MUNICIPALITY|WARD|PRECINCT|ZONE|AREA|BOARD|HEALTH|"
                          r"EDUCATION|EDUCATIONAL|UNINCORPORATED)\b")
_COUNTY_OWN_BOARD = re.compile(r"BOARD OF (COUNTY )?COMMISSIONERS|BOARD OF SUPERVISORS|COUNTY BOARD( OF [A-Z]+)?|"
                               r"BOARD OF COUNTY [A-Z]+")
# the county government named: the mark is stated (15:43: "'County of X', 'X County Commission', 'Police Jury'")
_COUNTY_GOV = re.compile(r"\b(COUNTY|PARISH) OF\b|COUNTY COMMISSION|COMMISSIONERS|BOARD OF SUPERVISORS|POLICE JURY|"
                         r"PARISH COUNCIL\b|COUNTY COUNCIL\b|FISCAL COURT|COMMISSIONERS COURT|COUNTY LEGISLATURE|"
                         r"COUNTY BOARD|COUNTY GOVERNMENT|PARISH GOVERNMENT")
# a special body named after a place (read only for a title that says no "CITY OF")
_SPECIAL = re.compile(r"\b(FIRE|HOSPITAL|LIBRARY|PORT|TRANSIT|WATER|SEWER|SANITARY|SANITATION|IRRIGATION|CEMETERY|"
                      r"AUTHORITY|AREA|REGIONAL|JOINT|CONSOLIDATED|PARK|RECREATION|UTILITY|UTILITIES|AMBULANCE|EMS|"
                      r"DRAINAGE|LEVEE|CONSERVANCY|AIRPORT|HEALTH|MOSQUITO)\b")
# words of another body than the town, after "TOWN OF X" (the orchestrator's ruling of 2026-11-07 18:13 on M2's sixth
# pass, checks/M2-REPORT.md section 12.4 (d): "a body's word after 'Town of' means another body, so held"): the county
# guard's words for a special body (_COUNTY_BODY), less its place words, which the town rule reads itself, and less a
# board or commission, which a town has of its own (a pension board, the conservation commission) [the reading]
_TOWN_BODY = re.compile(r"\b(FIRE|HOSPITAL|LIBRARY|AUTHORITY|PORT|TRANSIT|WATER|SEWER|SANITARY|SANITATION|IRRIGATION|"
                        r"CEMETERY|DRAINAGE|LEVEE|CONSERVANCY|CONSERVATION(?! COMMISSION)|AIRPORT|MOSQUITO|HEALTH|"
                        r"EDUCATION|EDUCATIONAL)\b")
_OREGON_NO = re.compile(r"^\d+-\d+\s*:?\s*")
_AFTER_HYPHEN = re.compile(r"(QUESTION|PROP|PROPOSITION|MEASURE|ISSUE|BOND|REFERENDUM|SPECIAL|\d)")


def _plain(s):
    """upper case, accents off ('Cañon City' -> 'CANON CITY'), single spaces"""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return " ".join(s.upper().replace("'S", "S").split())


_cache = {}


def load():
    """{state: {(name, kind): {"geoid", "census_name", "counties": {fips: county name}}}}, {state: {county name
    without its word: fips}}, the source block"""
    if "p" in _cache:
        return _cache["p"]
    os.makedirs(os.path.join(F.CACHE, os.path.dirname(NAME)), exist_ok=True)
    path = F.fetch(URL, NAME)
    places = collections.defaultdict(dict)
    county_names = collections.defaultdict(dict)
    with open(path, encoding="utf-8") as f:
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
            if p["geoid"] != sfp + pfp:   # two places of one name and kind in a state: neither can be told apart
                p["ambiguous"] = True
            p["counties"][sfp + cfp] = cname
    # county subdivisions with a government of their own (FUNCSTAT A): a town or township of the same name as a place
    # in the same county may be the body that holds the question, so a title that only begins with the name is held
    path = F.fetch(URL_COUSUB, NAME_COUSUB)
    # st -> name -> {(county fips, full name, kind, geoid, the Census's name)}
    subs = collections.defaultdict(lambda: collections.defaultdict(set))
    county_full = {}
    with open(path, encoding="utf-8") as f:
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
    src = [F.source_for(NAME, TITLE, LICENCE, mark="measured"),
           F.source_for(NAME_COUSUB, TITLE_COUSUB, LICENCE, mark="measured")]
    _cache["p"] = (places, county_names, subs, src)
    _cache["county_full"] = county_full
    return _cache["p"]


def match(office, state, county):
    """(found, why): found is {"unit", "place", "geoid", "county", "county_name", "how", "mark"} where the title names
    one incorporated place lying wholly in `county` (5-digit FIPS), one of its county subdivisions (towns and
    townships, which nest within it), or the county itself (whose record must then also cover the county's whole
    file: local_medsl.one_place); else None and why it is held."""
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
    """the word after a leading name, with it, begins another place's or subdivision's name in the state ('HADDON
    HEIGHT PROPOSAL' is not Haddon township): the title may name that other one"""
    places, _, subs, _ = load()
    w = rest.replace(":", " ").replace(",", " ").split()[:1]
    if not w or not w[0][:1].isalpha():
        return None
    longer = f"{n} {w[0]}"
    names = {pn for pn, _ in places.get(state, {})} | set(subs.get(state, {}))
    return next((o for o in sorted(names) if o != n and o.startswith(longer)), None)


def _county(t, state, county):
    """A county's or parish's own question (the orchestrator, 15:43): the title names the record's own county or
    parish and no other body; whether the record covers the county's whole file is read by local_medsl.one_place."""
    _, county_names, _, _ = load()
    tt = t.replace(".", "")
    own = [n.replace(".", "") for n, f in county_names[state].items() if f == county]
    hit = next((n for n in own if re.search(rf"\b{re.escape(n)}\s+(COUNTY|PARISH)\b|\b(COUNTY|PARISH) OF\s+"
                                             rf"{re.escape(n)}\b", tt)), None)
    if hit is None:
        return None, "the title names a county or parish, but not the record's own"
    part = re.search(rf"\b(NORTH|SOUTH|EAST|WEST|NORTHERN|SOUTHERN|EASTERN|WESTERN|CENTRAL|UPPER|LOWER)\s+"
                     rf"{re.escape(hit)}\s+(COUNTY|PARISH)\b", tt)
    if part:                                   # 'SOUTH FULTON COUNTY': a part of the county, not the county
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
    if paren:                                  # 'DELAWARE COUNTY (CLEORA)': the part of the county it is held in
        return None, f"the title names something in parentheses after the county ('{paren.group(0)}')"
    body = _COUNTY_BODY.search(_COUNTY_OWN_BOARD.sub(" ", rest))
    if body:
        return None, f"the title names another body than the county ('{body.group(0)}')"
    name = _cache["county_full"].get(county, hit.title())
    return {"unit": "county", "place": name, "geoid": county, "county": county, "county_name": name,
            "how": f"the title names the record's own {'parish' if 'PARISH' in tt else 'county'}, {name}, and no "
                   f"other body", "mark": "stated" if _COUNTY_GOV.search(tt) else "inferred"}, None


def _sub(t, state, county):
    """A town's or township's own question (the orchestrator, 15:43): an active county subdivision of the record's
    county, which nests within it by the Census's definition; a name that is both a place and a subdivision in the
    county is held unless the title says which."""
    places, county_names, subs, _ = load()
    mine = subs.get(state, {})
    hit = None
    for m in _SUB_TYPED.finditer(t):   # 'TOWN OF AVON ...', 'TOWNSHIP OF X'
        words = t[m.end():].split()
        for n in range(min(6, len(words)), 0, -1):
            name = " ".join(words[:n]).strip(" .,-:;()")
            if name in mine:
                hit = ("stated", f"the title says '{m.group(1)} OF {name}'", name, _SUB_KIND[m.group(1)])
                body = _TOWN_BODY.search(" ".join(words[n:]))
                if body:
                    return None, f"the title names another body than the town after its name ('{body.group(0)}')"
                break
        if hit:
            break
    if hit is None:   # 'WHITE TOWNSHIP PUBLIC QUESTION', 'CLINTON TWP ...'
        m = re.match(r"^(.*?)\s+(CHARTER TOWNSHIP|TOWNSHIP|TWP|TOWN|PLANTATION)\b", t)
        if m and m.group(1).strip(" .,-:;()") in mine:
            name = m.group(1).strip(" .,-:;()")
            hit = ("stated", f"the title says '{name} {m.group(2)}'", name, _SUB_KIND[m.group(2)])
            body = _TOWN_BODY.search(t[m.end():])
            if body:
                return None, f"the title names another body than the town after its name ('{body.group(0)}')"
    if hit is None and not _TOWNSHIP_WORD.search(t):   # the title begins with a subdivision's name, its kind unsaid
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
    if kinds is None:   # its kind unsaid: a place of the same name in the county may hold the question instead
        pl = [v for (pn, _), v in places.get(state, {}).items() if pn == name and county in v["counties"]]
        if any(_plain(v["census_name"]) != full for v in pl):
            return None, ("the name is both a place's and a town's or township's in the county, and the title does "
                          "not say which")
    return {"unit": "county subdivision", "place": census_name, "geoid": geoid, "county": county,
            "county_name": _cache["county_full"].get(county, county), "how": how, "mark": mark}, None


def _place(t, state, county):
    places, county_names, subs, _ = load()
    mine = places.get(state, {})
    names = collections.defaultdict(list)   # a name -> its places of every kind
    for k, v in mine.items():
        names[k[0]].append((k, v))
    hit = None
    for m in _TYPED.finditer(t):   # 'CITY OF X ...': the longest X, of up to six words, that is a place's name
        kind, words = m.group(1), t[m.end():].split()
        for n in range(min(6, len(words)), 0, -1):
            name = " ".join(words[:n]).strip(" .,-:;()")
            if n == 1 and name not in names and "-" in name:   # 'CITY OF MESA-QUESTION 2'
                name = name.split("-")[0]
            same = [(k, v) for k, v in names.get(name, ()) if k[1] == kind or (kind == "CITY" and k[1] == "")]
            if same:
                hit = ("stated", f"the title says '{kind} OF {name}'", same)
            elif names.get(name) and not (kind == "TOWN" and state in MCD_TOWNS):   # the place's name, though the
                hit = ("inferred", f"the title says '{kind} OF {name}'; the Census calls it a "   # Census calls it another
                       f"{names[name][0][0][1].lower() or 'place'}", names[name])   # kind ('City of Highfill')
            if hit:
                break
        if hit:
            break
    if hit is None:
        for n in sorted(names, key=len, reverse=True):
            if t == n or t.startswith(n + " ") or t.startswith(n + ",") or t.startswith(n + ":"):
                hit = ("inferred", f"the title begins with the place's name '{n}'", names[n])
                break
            if t.startswith(n + "- ") or t.startswith(n + " -"):   # 'CAMILLA- SUNDAY SALES': a dash between
                hit = ("inferred", f"the title begins with the place's name '{n}'", names[n])
                break
            if t.startswith(n + "-"):   # 'MESA-QUESTION 2', not 'CALDWELL-WEST CALDWELL'
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
        if len(w) == 2 and w[1] in _KIND_WORDS and w[0] not in _KIND_WORDS:   # 'OGDEN VALLEY CITY' is not Ogden city,
            return None, f"the name goes on past the place's ('{n} {w[0]} {w[1]}')"   # 'KENAI PENINSULA BOROUGH' not Kenai
        other = _goes_on(n, rest, state)
        if other:
            return None, f"the name may go on into another's ('{other}')"
        other = {full for cf, full, *_ in subs[state].get(n, ()) if cf == county} - {_plain(x[1]["census_name"])
                                                                                     for x in hit[2]}
        if other and not (w and len(hit[2]) == 1 and w[0] == hit[2][0][0][1]):   # 'BORDENTOWN CITY' says which
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


def source_blocks():
    return load()[3]
