from nicegui import ui

PALETTE = {
    "PRIMARY": "#081107",
    "ACCENT":  "#2CDD0D",
    "MUTED":   "#F1FAC0",
    "SURFACE": "#FFFFFF",
}


def setup_theme() -> None:
    css = """
<style>
:root {
  --color-primary:%s;
  --color-accent:%s;
  --color-muted:%s;
  --color-surface:%s;
  --on-primary:#F1FAC0; /* light text on dark */
  --on-accent:#081107;  /* dark text on bright */
  --on-muted:#081107;   /* dark text on pale */
  --on-surface:#081107; /* dark text on white */

  /* Quasar overrides to eliminate default blue */
  --q-primary: var(--color-accent);
  --q-secondary: var(--color-primary);
  --q-accent: var(--color-accent);
  --q-dark: var(--color-primary);
  --color-charcoal:#121212;
}

/* Background + readable text pairings */
.bg-primary { background:var(--color-primary); color:var(--on-primary); }
.bg-accent  { background:var(--color-accent);  color:var(--on-accent);  }
.bg-muted   { background:var(--color-muted);   color:var(--on-muted);   }
.bg-surface { background:var(--color-surface); color:var(--on-surface); }

/* Components */
.btn-primary, .btn-secondary { background:var(--color-accent); color:var(--color-charcoal); border-radius:12px; padding:.6rem 1rem; font-weight:600; transition:transform .15s ease, box-shadow .15s ease, filter .15s ease; }
.btn-primary:hover, .btn-secondary:hover { filter:brightness(1.02); transform:translateY(-1px); box-shadow:0 10px 18px rgba(0,0,0,.12); }
.btn-primary:active, .btn-secondary:active { transform:translateY(0); box-shadow:0 6px 12px rgba(0,0,0,.10); }

.input { background:var(--color-surface); color:var(--on-surface); border:1px solid var(--color-muted); border-radius:12px; padding:.6rem .8rem; }
.input:focus { outline:3px solid var(--color-accent); outline-offset:2px; }

.card { background:var(--color-surface); color:var(--on-surface); border:1px solid var(--color-muted); border-radius:16px; padding:1rem; transition:transform .2s ease, box-shadow .2s ease; }
.card:hover { transform:translateY(-4px); box-shadow:0 12px 24px rgba(0,0,0,.15); }
.card-charcoal { background:var(--color-charcoal); color:var(--color-accent); border:1px solid var(--color-accent); }
.table th { background:var(--color-muted); color:var(--on-muted); }
.table tr:nth-child(even) { background:color-mix(in oklab, var(--color-muted) 35%%, white); }

.alert-success { background:var(--color-accent); color:var(--on-accent); padding:.75rem 1rem; border-radius:12px; }
.alert-dark { background:var(--color-primary); color:var(--on-primary); padding:.75rem 1rem; border-radius:12px; }

/* Auto-alternating section backgrounds on every page */
.section:nth-of-type(3n+1) { background:var(--color-primary); color:var(--on-primary); }
.section:nth-of-type(3n+2) { background:var(--color-accent);  color:var(--on-accent);  }
.section:nth-of-type(3n+3) { background:var(--color-muted);   color:var(--on-muted);   }

/* Links */
a { color:var(--color-accent); }
a:hover { text-decoration:underline; }

/* Workspace background: set entire app to soft lime */
html, body { background:var(--color-muted); color:var(--on-muted); }
/* Override section alternation to unify background */
.section { background:var(--color-muted) !important; color:var(--on-muted) !important; }

/* Quasar component accents (avoid default blue) */
.q-field--focused .q-field__control { box-shadow:0 0 0 3px var(--color-accent) inset; }
.q-checkbox__inner--truthy, .q-radio__inner--truthy, .q-toggle__inner--truthy { color:var(--color-accent); }
.q-btn--standard.q-btn--rectangle.q-btn--actionable.q-focusable.q-hoverable { background:var(--color-accent); color:var(--color-charcoal); }
button, .q-btn { background:var(--color-accent) !important; color:var(--color-charcoal) !important; }
</style>
""" % (
        PALETTE['PRIMARY'],
        PALETTE['ACCENT'],
        PALETTE['MUTED'],
        PALETTE['SURFACE'],
    )
    ui.add_head_html(css)

