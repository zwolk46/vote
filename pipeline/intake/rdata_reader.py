"""pipeline/intake/rdata_reader.py: read the data frames in an R .Rdata (or .rds) file, with no R and no package.

Written 2026-11-07 by worker D2 for pipeline/intake/algara_amlani.py. Algara and Amlani publish their county
returns only as .Rdata (doi:10.7910/DVN/DGUMFI), and this environment has no R; pulling in a package for one
file format would make every rerun depend on it, so the format is read here from R's own description of it
(R Internals, section 1.8 "Serialization Formats"; R's src/main/serialize.c).

What it reads: R's XDR serialization, versions 2 and 3, gzip-compressed or not, as save() and saveRDS() write
it. Logical, integer, double, string and list vectors, pairlists, attributes, symbols, references, and the
ALTREP forms R 3.5 and later write for compact sequences, wrapped vectors and deferred strings. That covers
data frames, factors, dates and tibbles. Closures, environments and byte code are read past (they are kept as
opaque objects), so a file that holds one still loads.

  load(path)          {name: object} for every object the .Rdata holds (readRDS: {"": object})
  data_frame(obj)     {column: list of Python values} with factors as their labels, NA as None
"""
import gzip
import struct

NA_INTEGER = -2147483648


class RObject:
    """An R value: its type, its data (a list, or a dict for pairlists) and its attributes."""

    def __init__(self, rtype, value, attributes=None):
        self.rtype, self.value, self.attributes = rtype, value, attributes or {}

    def attr(self, name):
        return self.attributes.get(name)

    def __repr__(self):
        return f"RObject({self.rtype}, {str(self.value)[:60]}, attrs={list(self.attributes)})"


class _Reader:
    def __init__(self, data):
        self.b, self.i, self.refs = data, 0, []

    def int(self):
        v = struct.unpack_from(">i", self.b, self.i)[0]
        self.i += 4
        return v

    def length(self):
        n = self.int()
        if n == -1:
            hi, lo = self.int(), self.int()
            n = (hi << 32) + lo
        return n

    def bytes(self, n):
        v = self.b[self.i:self.i + n]
        self.i += n
        return v

    def attributes(self, has_attr):
        if not has_attr:
            return {}
        pl = self.item()
        return dict(pl.value) if isinstance(pl, RObject) and pl.rtype == "pairlist" else {}

    def pairlist(self, flags, rtype="pairlist"):
        # pairlists are read iteratively along the CDR so that a long one does not recurse
        out, attrs, first = [], {}, True
        while True:
            has_attr, has_tag = flags & (1 << 9), flags & (1 << 10)
            a = self.attributes(has_attr)
            if first:
                attrs, first = a, False
            tag = self.item() if has_tag else None
            car = self.item()
            name = tag.value if isinstance(tag, RObject) and tag.rtype == "symbol" else None
            out.append((name, car))
            flags = self.int()
            t = flags & 0xFF
            if t == 254:            # NILVALUE: end of the list
                break
            if t not in (2, 6, 239, 240):
                # an improper list: its last CDR is some other object
                self.i -= 4
                self.item()
                break
        return RObject(rtype, out, attrs)

    def item(self):
        flags = self.int()
        t = flags & 0xFF
        has_attr = flags & (1 << 9)
        if t == 254:                                    # NILVALUE_SXP
            return None
        if t in (253, 242, 241, 251, 250, 252):        # global, empty, base env; missing arg; base namespace
            return RObject("special", t)
        if t == 255:                                    # REFSXP
            idx = flags >> 8
            if idx == 0:
                idx = self.int()
            return self.refs[idx - 1]
        if t in (248, 249, 247):                        # PACKAGESXP, NAMESPACESXP, PERSISTSXP
            self.int()                                  # 0
            n = self.int()
            names = [self.item() for _ in range(n)]
            obj = RObject("namespace", names)
            self.refs.append(obj)
            return obj
        if t == 1:                                      # SYMSXP
            ch = self.item()
            obj = RObject("symbol", ch)
            self.refs.append(obj)
            return obj
        if t in (2, 239):                               # LISTSXP, ATTRLISTSXP
            return self.pairlist(flags)
        if t in (6, 240):                               # LANGSXP, ATTRLANGSXP
            return self.pairlist(flags, "language")
        if t in (3, 5):                                 # CLOSXP, PROMSXP: written as a pairlist cell
            return self.pairlist(flags, "closure")
        if t == 4:                                      # ENVSXP
            obj = RObject("environment", None)
            self.refs.append(obj)
            self.int()                                  # locked
            self.item()                                 # enclosure
            frame, hashtab = self.item(), self.item()
            self.item()                                 # attributes
            obj.value = {"frame": frame, "hashtab": hashtab}
            return obj
        if t == 9:                                      # CHARSXP
            n = self.int()
            if n == -1:
                return None
            raw = self.bytes(n)
            levels = flags >> 12
            enc = "latin-1" if levels & (1 << 2) else "utf-8"
            return raw.decode(enc, errors="replace")
        if t in (10, 13):                               # LGLSXP, INTSXP
            n = self.length()
            vals = list(struct.unpack_from(f">{n}i", self.b, self.i))
            self.i += 4 * n
            vals = [None if v == NA_INTEGER else v for v in vals]
            if t == 10:
                vals = [None if v is None else bool(v) for v in vals]
            return RObject("logical" if t == 10 else "integer", vals, self.attributes(has_attr))
        if t == 14:                                     # REALSXP
            n = self.length()
            vals = list(struct.unpack_from(f">{n}d", self.b, self.i))
            self.i += 8 * n
            vals = [None if (v != v) else v for v in vals]   # NA and NaN both read as None
            return RObject("double", vals, self.attributes(has_attr))
        if t == 15:                                     # CPLXSXP
            n = self.length()
            vals = struct.unpack_from(f">{2 * n}d", self.b, self.i)
            self.i += 16 * n
            return RObject("complex", [complex(vals[2 * k], vals[2 * k + 1]) for k in range(n)],
                           self.attributes(has_attr))
        if t == 16:                                     # STRSXP
            n = self.length()
            vals = [self.item() for _ in range(n)]
            return RObject("character", vals, self.attributes(has_attr))
        if t in (19, 20):                               # VECSXP, EXPRSXP
            n = self.length()
            vals = [self.item() for _ in range(n)]
            return RObject("list", vals, self.attributes(has_attr))
        if t == 24:                                     # RAWSXP
            n = self.length()
            return RObject("raw", self.bytes(n), self.attributes(has_attr))
        if t == 25:                                     # S4SXP
            return RObject("S4", None, self.attributes(has_attr))
        if t == 238:                                    # ALTREP_SXP
            info, state, attr = self.item(), self.item(), self.item()
            cls = info.value[0][1].value if isinstance(info, RObject) and info.value else None
            obj = _altrep(cls, state)
            if isinstance(attr, RObject) and attr.rtype == "pairlist":
                obj.attributes = dict(attr.value)
            return obj
        raise ValueError(f"R serialization type {t} at byte {self.i - 4} is not read by this reader")


def _altrep(cls, state):
    if cls == "compact_intseq":
        n, start, step = state.value[:3]
        return RObject("integer", [int(start + k * step) for k in range(int(n))])
    if cls == "compact_realseq":
        n, start, step = state.value[:3]
        return RObject("double", [start + k * step for k in range(int(n))])
    if cls and cls.startswith("wrap_"):
        return RObject(state.value[0].rtype, state.value[0].value, dict(state.value[0].attributes))
    if cls == "deferred_string":
        src = state.value[0][1] if state.rtype == "pairlist" else state.value[0]
        vals = []
        for v in src.value:
            if v is None:
                vals.append(None)
            elif src.rtype == "integer":
                vals.append(str(v))
            else:
                vals.append(repr(float(v)) if v != int(v) else str(int(v)))
        return RObject("character", vals)
    raise ValueError(f"ALTREP class {cls} is not read by this reader")


def _open(path):
    with open(path, "rb") as f:
        raw = f.read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw


def load(path):
    raw = _open(path)
    if raw[:5] in (b"RDX2\n", b"RDX3\n"):
        body, rdata = raw[5:], True
    else:
        body, rdata = raw, False
    if body[:2] != b"X\n":
        raise ValueError("only R's XDR (binary, big-endian) format is read")
    r = _Reader(body[2:])
    version = r.int()
    r.int(), r.int()                                    # writer's R version, minimal reader version
    if version == 3:
        r.bytes(r.int())                                # native encoding
    obj = r.item()
    if rdata:
        return {name: value for name, value in obj.value}
    return {"": obj}


def data_frame(obj):
    """A data frame's columns as {name: [values]}: factors as their labels, NA as None."""
    names = obj.attr("names").value
    out = {}
    for name, col in zip(names, obj.value):
        vals = col.value
        levels = col.attr("levels")
        if levels is not None and col.rtype == "integer":
            labs = levels.value
            vals = [None if v is None else labs[v - 1] for v in vals]
        out[name] = vals
    return out


def classes(obj):
    c = obj.attr("class")
    return c.value if c is not None else []
