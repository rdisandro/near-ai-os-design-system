"""Colour helpers for the Near AI parent system: sRGB <-> OKLCH, alpha
compositing, WCAG 2 contrast. Pure stdlib."""
import math


def hex_to_rgba(h):
    h = h.lstrip('#')
    if len(h) in (3, 4):
        h = ''.join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
    return r, g, b, a


def rgb_to_hex(r, g, b, a=None):
    c = lambda v: max(0, min(255, round(v * 255)))
    s = '#%02x%02x%02x' % (c(r), c(g), c(b))
    if a is not None and a < 0.999:
        s += '%02x' % c(a)
    return s


def over(fg, bg):
    """Composite fg (r,g,b,a) over opaque bg (r,g,b)."""
    r, g, b, a = fg
    return tuple(a * f + (1 - a) * k for f, k in zip((r, g, b), bg[:3]))


def flatten(*layers):
    """layers bottom-up as hex strings; the first must be opaque."""
    base = hex_to_rgba(layers[0])[:3]
    for h in layers[1:]:
        base = over(hex_to_rgba(h), base)
    return base


def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gam(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def luminance(rgb):
    r, g, b = (_lin(c) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def srgb_to_oklab(rgb):
    r, g, b = (_lin(c) for c in rgb[:3])
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def oklab_to_srgb(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return tuple(_gam(v) if v > 0 else 0.0 for v in (r, g, bb))


def to_oklch(h):
    L, a, b = srgb_to_oklab(hex_to_rgba(h))
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def in_gamut(rgb, eps=1e-4):
    return all(-eps <= v <= 1 + eps for v in rgb)


def oklch_hex(L, C, H):
    """OKLCH -> hex, reducing chroma until it fits sRGB."""
    while C > 0:
        a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
        l_ = L + 0.3963377774 * a + 0.2158037573 * b
        m_ = L - 0.1055613458 * a - 0.0638541728 * b
        s_ = L - 0.0894841775 * a - 1.2914855480 * b
        l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
        lin = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
               -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
               -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)
        if in_gamut(lin):
            return rgb_to_hex(*(_gam(max(0, v)) for v in lin))
        C -= 0.002
    return rgb_to_hex(*oklab_to_srgb(L, 0, 0))


def cr(fg_hex, *ground_layers):
    """Contrast of fg (may carry alpha) over a stack of ground layers."""
    ground = flatten(*ground_layers)
    fg = hex_to_rgba(fg_hex)
    return contrast(over(fg, ground), ground)
