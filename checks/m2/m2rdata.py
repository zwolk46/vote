"""m2rdata: a reader of R's serialization format (RData, 'RDX2' / 'RDX3', XDR) for data frames, written for M2's checks
so that Algara and Amlani's county returns (an .Rdata of one data frame) can be read with nothing from pipeline/
imported. Reads what a data frame needs: lists, atomic vectors (logical, integer, double, character), attributes,
symbols, the string pool and references; factors are turned into their labels. Anything else raises.

Format (R Internals, 'Serialization Formats'): the file is gzip (or plain), begins with 'RDX2\\n' or 'RDX3\\n', then
'X\\n' (XDR, big-endian), three 4-byte ints (format version, R version, min R version; version 3 adds the native
encoding string), then a pairlist of (symbol, value) pairs: the saved objects. Each item begins with a 4-byte flags
word: type in bits 0-7, has-attributes bit 9, has-tag bit 10, is-object bit 8, levels in bits 12+.
"""
import gzip
import struct

NILVALUE_SXP, REFSXP, GLOBALENV_SXP, EMPTYENV_SXP, BASEENV_SXP, MISSINGARG_SXP, UNBOUNDVALUE_SXP = 254, 255, 253, 242, 241, 251, 252
NAMESPACESXP, PACKAGESXP, PERSISTSXP, ALTREP_SXP, BASENAMESPACE_SXP = 249, 248, 247, 238, 247
SYMSXP, LISTSXP, CLOSXP, ENVSXP, PROMSXP, LANGSXP, SPECIALSXP, BUILTINSXP, CHARSXP, LGLSXP = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
INTSXP, REALSXP, CPLXSXP, STRSXP, DOTSXP, VECSXP, EXPRSXP, RAWSXP, S4SXP = 13, 14, 15, 16, 17, 19, 20, 24, 25
NA_INT = -2147483648


class Reader:
    def __init__(self, data):
        self.b = data
        self.i = 0
        self.refs = []

    def int(self):
        v = struct.unpack_from(">i", self.b, self.i)[0]
        self.i += 4
        return v

    def double(self):
        v = struct.unpack_from(">d", self.b, self.i)[0]
        self.i += 8
        return v

    def raw(self, n):
        v = self.b[self.i:self.i + n]
        self.i += n
        return v

    def string(self):   # a CHARSXP's body after its flags: length, bytes (-1 is NA)
        n = self.int()
        if n == -1:
            return None
        return self.raw(n).decode("utf-8", "replace")

    def item(self):
        flags = self.int()
        t = flags & 0xFF
        has_attr = bool(flags & (1 << 9))
        has_tag = bool(flags & (1 << 10))
        if t == NILVALUE_SXP:
            return None
        if t == REFSXP:
            idx = flags >> 8
            if idx == 0:
                idx = self.int()
            return self.refs[idx - 1]
        if t in (GLOBALENV_SXP, EMPTYENV_SXP, BASEENV_SXP, MISSINGARG_SXP, UNBOUNDVALUE_SXP, BASENAMESPACE_SXP):
            return ("env", t)
        if t == SYMSXP:
            s = self.item()   # a CHARSXP
            sym = ("sym", s)
            self.refs.append(sym)
            return sym
        if t in (LISTSXP, LANGSXP, PROMSXP, DOTSXP):
            attr = self.item() if has_attr else None
            tag = self.item() if has_tag else None
            car = self.item()
            cdr = self.item()
            return ("pair", tag, car, cdr, attr)
        if t == CHARSXP:
            return self.string()
        if t == LGLSXP:
            n = self.int()
            v = [None if x == NA_INT else bool(x) for x in struct.unpack_from(f">{n}i", self.b, self.i)]
            self.i += 4 * n
            return self.attrs(("vec", "lgl", v), has_attr)
        if t == INTSXP:
            n = self.int()
            v = [None if x == NA_INT else x for x in struct.unpack_from(f">{n}i", self.b, self.i)]
            self.i += 4 * n
            return self.attrs(("vec", "int", v), has_attr)
        if t == REALSXP:
            n = self.int()
            v = list(struct.unpack_from(f">{n}d", self.b, self.i))
            self.i += 8 * n
            return self.attrs(("vec", "dbl", v), has_attr)
        if t == STRSXP:
            n = self.int()
            v = [self.item() for _ in range(n)]
            return self.attrs(("vec", "str", v), has_attr)
        if t in (VECSXP, EXPRSXP):
            n = self.int()
            v = [self.item() for _ in range(n)]
            return self.attrs(("vec", "list", v), has_attr)
        if t == RAWSXP:
            n = self.int()
            return self.attrs(("vec", "raw", self.raw(n)), has_attr)
        if t in (ENVSXP, NAMESPACESXP, PACKAGESXP, PERSISTSXP, ALTREP_SXP, S4SXP, CLOSXP, SPECIALSXP, BUILTINSXP, CPLXSXP):
            raise ValueError(f"R object type {t} is not read here")
        raise ValueError(f"unknown R object type {t}")

    def attrs(self, vec, has_attr):
        if not has_attr:
            return vec
        a = self.item()   # a pairlist of (tag, value)
        d = {}
        while a is not None:
            _, tag, car, cdr, _ = a
            d[tag[1] if tag else None] = car
            a = cdr
        return vec + (d,)


def load(path):
    """{name: object} of the saved objects; a data frame comes back as {"columns": [names], "data": {name: [values]},
    "nrow": n} with factors as their labels."""
    with open(path, "rb") as f:
        head = f.read(2)
    opener = gzip.open if head == b"\x1f\x8b" else open
    with opener(path, "rb") as f:
        data = f.read()
    if data[:5] not in (b"RDX2\n", b"RDX3\n"):
        raise ValueError("not an RData file (no RDX2/RDX3 header)")
    r = Reader(data)
    r.i = 5
    if r.raw(2) != b"X\n":
        raise ValueError("not XDR")
    version = r.int()
    r.int()
    r.int()
    if version == 3:
        n = r.int()
        r.raw(n)   # the native encoding
    out = {}
    node = r.item()
    while node is not None:
        _, tag, car, cdr, _ = node
        out[tag[1] if tag else None] = frame(car)
        node = cdr
    return out


def _values(col):
    kind, v = col[1], col[2]
    attrs = col[3] if len(col) > 3 else {}
    if kind == "int" and attrs.get("levels"):
        labels = attrs["levels"][2]
        return [None if x is None else labels[x - 1] for x in v]
    if kind == "dbl":
        return [None if x != x else x for x in v]   # NaN as None
    return v


def frame(obj):
    """A data frame (a list with names and class data.frame) as columns; any other object as read."""
    if not (isinstance(obj, tuple) and obj[0] == "vec" and obj[1] == "list" and len(obj) > 3):
        return obj
    attrs = obj[3]
    cls = attrs.get("class")
    if not cls or "data.frame" not in cls[2]:
        return obj
    names = attrs["names"][2]
    cols = {n: _values(c) for n, c in zip(names, obj[2])}
    nrow = len(next(iter(cols.values()))) if cols else 0
    return {"columns": names, "data": cols, "nrow": nrow}
