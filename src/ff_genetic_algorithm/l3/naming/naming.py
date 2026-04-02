"""
DNA bit-string to Hangul name encoder/decoder.

Hangul syllables (0xAC00~0xD7A3) cover 11,172 codepoints.
Each character encodes 13 bits (2^13 = 8,192 < 11,172),
providing lossless compression of arbitrary DNA bit-strings.
"""

_BASE = 0xAC00  # '가'
_BITS_PER_CHAR = 13
_GROUP_SIZE = 8


def _bits_to_chars(bits):
    chars = []
    for i in range(0, len(bits), _BITS_PER_CHAR):
        chunk = bits[i:i + _BITS_PER_CHAR]
        if len(chunk) < _BITS_PER_CHAR:
            chunk = chunk.ljust(_BITS_PER_CHAR, '0')
        chars.append(chr(_BASE + int(chunk, 2)))
    return chars


def dna_to_name(dna):
    """DNA -> Hangul name (8 chars per group, dash-separated)."""
    chars = _bits_to_chars(dna.to_bits())
    parts = []
    for i in range(0, len(chars), _GROUP_SIZE):
        parts.append(''.join(chars[i:i + _GROUP_SIZE]))
    return '-'.join(parts)


def bits_to_name(bits):
    """Bit-string -> Hangul name."""
    chars = _bits_to_chars(bits)
    parts = []
    for i in range(0, len(chars), _GROUP_SIZE):
        parts.append(''.join(chars[i:i + _GROUP_SIZE]))
    return '-'.join(parts)


def name_to_bits(name):
    """Hangul name -> bit-string."""
    chars = name.replace('-', '')
    bits = ''
    for ch in chars:
        val = ord(ch) - _BASE
        bits += format(val, f'0{_BITS_PER_CHAR}b')
    return bits


def name_to_short(name):
    """Short display name (first group only)."""
    return name.split('-')[0] if '-' in name else name[:_GROUP_SIZE]
