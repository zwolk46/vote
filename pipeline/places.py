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
                "codes2020 reference files), read only to hold a title whose name is also a town's or township's")

KINDS = ("city and borough", "city", "town", "village", "borough", "municipality", "township")
_LSAD = re.compile(r"^(.*?) (city and borough|city|town|village|borough|municipality|township)$")
_TYPED = re.compile(r"\b(CITY|TOWN|VILLAGE|BOROUGH) OF\s+")
_KIND_WORDS = {"CITY", "TOWN", "VILLAGE", "BOROUGH"}
# the body that holds the question is not the place
_NOT_PLACE = re.compile(r"\bSCHOOLS?\b|\bDISTRICT\b|\bDIST\b|\bUSD\b|\bISD\b|\bCISD\b|\bESD\b|\bHSD\b|\bUHSD\b|"
                        r"\bUNION (#|HSD|HS\b|NO\b)|\bBOE\b|BOARD OF EDUCATION|\bUNIFIED\b|\bCOLLEGE\b|"
                        r"\bCOUNTY\b|\bPARISH\b|\bTOWNSHIP\b|\bTWP\b")
# a special body named after a place (read only for a title that says no "CITY OF")
_SPECIAL = re.compile(r"\b(FIRE|HOSPITAL|LIBRARY|PORT|TRANSIT|WATER|SEWER|SANITARY|SANITATION|IRRIGATION|CEMETERY|"
                      r"AUTHORITY|AREA|REGIONAL|JOINT|CONSOLIDATED|PARK|RECREATION|UTILITY|UTILITIES|AMBULANCE|EMS|"
                      r"DRAINAGE|LEVEE|CONSERVANCY|AIRPORT|HEALTH|MOSQUITO)\b")
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
    subs = collections.defaultdict(lambda: collections.defaultdict(set))   # st -> name -> {(county fips, full name)}
    with open(path, encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("|")
        if head != ["STATE", "STATEFP", "COUNTYFP", "COUNTYNAME", "COUSUBFP", "COUSUBNS", "COUSUBNAME", "CLASSFP",
                    "FUNCSTAT"]:
            raise SystemExit(f"places: the Census county subdivision file's columns are not those read: {head}")
        for line in f:
            st, sfp, cfp, _cname, _cfp, _ns, sname, _cls, fs = line.rstrip("\n").split("|")
            if fs != "A":
                continue
            m = _LSAD.match(sname)
            subs[st][_plain(m.group(1) if m else sname)].add((sfp + cfp, _plain(sname)))
    src = [F.source_for(NAME, TITLE, LICENCE, mark="measured"),
           F.source_for(NAME_COUSUB, TITLE_COUSUB, LICENCE, mark="measured")]
    _cache["p"] = (places, county_names, subs, src)
    return _cache["p"]


def match(office, state, county):
    """(found, why): found is {"place", "census_name", "geoid", "county", "how", "mark"} where the title names one
    incorporated place lying wholly in `county` (5-digit FIPS); else None and why it is held."""
    places, county_names, subs, _ = load()
    t = _plain(office)
    t = _OREGON_NO.sub("", t)
    mine = places.get(state, {})
    if _NOT_PLACE.search(t):
        return None, "the title names a district, a county, a parish or a township"
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
        other = {full for cf, full in subs[state].get(n, ()) if cf == county} - {_plain(x[1]["census_name"])
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
    return {"place": p["census_name"], "geoid": p["geoid"], "county": county, "county_name": p["counties"][county],
            "how": how, "mark": mark}, None


def source_blocks():
    return load()[3]
