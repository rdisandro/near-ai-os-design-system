"""Contrast floors for the Near AI OS Design System.

Glass shows whatever is behind it, so every text role is measured over the
worst desktop the glass can show: a white desktop under dark glass, #333333
under light glass (trace-commons' FlatThemeContrastTests model). A ground is
built bottom-up: desktop, glass-veil, pane-fill, then the tier's own fill.
"""
from colorkit import contrast, cr, flatten, hex_to_rgba

TEXT_ROLES = ['text-primary', 'text-secondary', 'text-tertiary', 'text-placeholder', 'accent-text',
              'positive-text', 'caution-text', 'critical-text', 'destructive-text']
MARK_ROLES = ['positive', 'caution', 'critical', 'neutral', 'accent-soft', 'tab-ember']


def theme_values(src, tid):
    return {name: role['values'][tid] for name, role in src['color'].items()}


def grounds(src, theme):
    """The grounds text is drawn on, each as a bottom-up list of layers."""
    v = theme_values(src, theme['id'])
    desk = src['contrast']['worstDesktop'][theme['appearance']]
    pane = [desk, v['glass-veil'], v['pane-fill']]
    return {
        'pane': pane,
        'card': pane + [v['card']],
        'card-quiet': pane + [v['card-quiet']],
        'field': pane + [v['field']],
        'control': pane + [v['control']],
        'popover': [desk, v['popover']],
        'menu': [desk, v['menu']],
        'pane-opaque': [v['pane-opaque']],
        'card-on-opaque': [v['pane-opaque'], v['card-on-opaque']],
        'card-quiet-on-opaque': [v['pane-opaque'], v['card-quiet-on-opaque']],
        'scene-card': [v['scene'], v['scene-card']],
    }


OPAQUE = ('pane-opaque', 'card-on-opaque', 'card-quiet-on-opaque')


def _pair(fg, bg):
    return contrast(hex_to_rgba(fg), hex_to_rgba(bg))


def checks(src):
    """Every contrast check, as (theme, token, label, ratio, floor)."""
    floors = src['contrast']['floors']
    out = []
    for theme in src['themes']:
        tid = theme['id']
        v = theme_values(src, tid)
        gr = grounds(src, theme)
        tfloor = floors['textIncreased'] if theme['contrast'] == 'increased' else floors['text']

        def add(token, label, ratio, floor):
            out.append((tid, token, label, round(ratio, 2), floor))

        for t in TEXT_ROLES:
            ratio, where = min((cr(v[t], *g), n) for n, g in gr.items())
            add(t, '%s on %s (worst ground)' % (t, where), ratio, tfloor)
        ratio, where = min((cr(v['text-placeholder-on-opaque'], *gr[n]), n) for n in OPAQUE)
        add('text-placeholder-on-opaque', 'text-placeholder-on-opaque on %s (opaque grounds only)' % where, ratio, tfloor)
        add('proof-text', 'proof-text on proof-tint', _pair(v['proof-text'], v['proof-tint']), tfloor)
        add('text-on-accent', 'text-on-accent on accent', _pair(v['text-on-accent'], v['accent']), tfloor)
        add('text-on-accent', 'text-on-accent on accent-pressed', _pair(v['text-on-accent'], v['accent-pressed']), tfloor)
        hover = flatten(*(gr['menu'] + [v['menu-hover']]))
        add('menu-hover', 'text-on-accent on menu-hover over menu',
            contrast(hex_to_rgba(v['text-on-accent']), hover), tfloor)
        add('text-on-status', 'text-on-status on badge-fill', _pair(v['text-on-status'], v['badge-fill']), tfloor)
        for token in ('accent', 'focus-ring'):
            ratio, where = min((cr(v[token], *g), n) for n, g in gr.items())
            add(token, '%s (a state on its own) on %s' % (token, where), ratio, floors['mark'])
        for s in MARK_ROLES:
            add(s, '%s mark on pane-opaque' % s, cr(v[s], v['pane-opaque']), floors['mark'])
        for i in range(1, 9):
            add('data-%d' % i, 'data-%d on surface-chart' % i, cr(v['data-%d' % i], v['surface-chart']), floors['mark'])
        if theme['appearance'] == 'dark':
            ratio, where = min((cr(v['toggle-knob-off'], *(gr[n] + [v['toggle-track-off']])), n)
                               for n in ('pane', 'card', 'pane-opaque'))
            add('toggle-knob-off', 'toggle-knob-off on toggle-track-off over %s' % where, ratio, floors['mark'])
        ratio = min(cr(v['toolbar-glyph-off'], *(gr['pane'] + [v['control']])), cr(v['toolbar-glyph-off'], v['pane-opaque']))
        add('toolbar-glyph-off', 'toolbar-glyph-off on control', ratio, floors['mark'])
        if theme['contrast'] == 'increased':
            ratio, where = min((cr(v['edge-hc'], *g), n) for n, g in gr.items())
            add('edge-hc', 'edge-hc on %s' % where, ratio, floors['mark'])
    return out


def failures(src):
    return [c for c in checks(src) if c[3] < c[4] - 1e-9]
