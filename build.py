#!/usr/bin/env python3
"""Builds the JFC Construction & Groundwork site. Words live in content.py.
Run:  python3 build.py   (writes the index.html files, sitemap.xml and robots.txt next to this script)."""
import os, json
from PIL import Image as _Img
from content import *

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------- icons ----------
def svg(body, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'
I = {
    'arrow': svg('<path d="M5 12h14M13 6l6 6-6 6"/>', 'arr'),
    'phone': svg('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>'),
    'mail': svg('<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>'),
    'pin': svg('<path d="M12 22s-8-6.6-8-12a8 8 0 0 1 16 0c0 5.4-8 12-8 12z"/><circle cx="12" cy="10" r="3"/>'),
    'check': svg('<path d="M20 6L9 17l-5-5"/>'),
    'chev': svg('<path d="M6 9l6 6 6-6"/>'),
    'x': svg('<path d="M18 6L6 18M6 6l12 12"/>'),
    'left': svg('<path d="M15 18l-6-6 6-6"/>'),
    'right': svg('<path d="M9 18l6-6-6-6"/>'),
    'shield': svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>'),
    'quote': svg('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>'),
    'star': svg('<path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>'),
    'clock': svg('<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>'),
    'house': svg('<path d="M3 11l9-8 9 8"/><path d="M5 9.5V21h14V9.5"/><path d="M10 21v-6h4v6"/>'),
    'layers': svg('<path d="M12 2l10 5-10 5L2 7z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/>'),
    'drop': svg('<path d="M12 2.7l5.7 5.6a8 8 0 1 1-11.4 0z"/>'),
    'hammer': svg('<path d="M15 12l-8.5 8.5a2.1 2.1 0 0 1-3-3L12 9"/><path d="M17.6 15L22 10.6M20.9 11.7l-4.6-4.6a3 3 0 0 0-2.1-.9h-1.8L10 4l1.8-1.8h3.5a6 6 0 0 1 4.2 1.8l2.6 2.6"/>'),
    'chat': svg('<path d="M21 11.5a8.4 8.4 0 0 1-12.3 7.4L3 21l2-5.4A8.4 8.4 0 1 1 21 11.5z"/>'),
    'search': svg('<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>'),
    'broom': svg('<path d="M19.4 2.6l-7.8 7.8"/><path d="M11 9l4 4-3.5 8.5L3 13z"/><path d="M7 17l-2 2"/>'),
    'users': svg('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>'),
    'leaf': svg('<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.4 5.1-6"/>'),
    'sun': svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>'),
    'sparkle': svg('<path d="M12 3l1.9 5.8L20 11l-6.1 2.2L12 19l-1.9-5.8L4 11l6.1-2.2z"/>'),
    'attic': svg('<path d="M2 20L12 4l10 16z"/><path d="M8 20v-5h8v5"/><path d="M12 9v2"/>'),
    'ext': svg('<path d="M2 11l7-6 7 6"/><path d="M4 9.5V20h10V9.5"/><path d="M14 13h8v7h-8"/>'),
    'reno': svg('<path d="M3 11l9-8 9 8"/><path d="M5 9.5V21h14V9.5"/><path d="M9 14l2 2 4-4"/>'),
    'camera': svg('<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>'),
    'map': svg('<path d="M1 6v16l7-4 8 4 7-4V2l-7 4-8-4z"/><path d="M8 2v16M16 6v16"/>'),
    'gauge': svg('<path d="M12 14l4-4"/><path d="M3.3 19a10 10 0 1 1 17.4 0"/>'),
    'award': svg('<circle cx="12" cy="8" r="6"/><path d="M8.2 13.2L7 22l5-3 5 3-1.2-8.8"/>'),
    'calendar': svg('<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>'),
}
WA = '<svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.7c-2 0-4-.5-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.7 10.7 0 1 1 16 26.7zm5.9-8c-.3-.2-1.9-1-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.8 8.8 0 0 1-4.4-3.8c-.3-.6.3-.5 1-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6a1.2 1.2 0 0 0-.9.4 3.7 3.7 0 0 0-1.1 2.7 6.4 6.4 0 0 0 1.3 3.4 14.7 14.7 0 0 0 5.7 5c2.1.9 2.9 1 4 .8a3.4 3.4 0 0 0 2.2-1.6 2.8 2.8 0 0 0 .2-1.6c0-.2-.3-.3-.6-.5z"/></svg>'
WA_ICON = WA.replace('<svg', '<svg width="22" height="22"')
HOUSE_SVG = '<svg class="house" viewBox="0 0 400 260" fill="none" stroke="#fff" stroke-width="22" stroke-linejoin="miter"><path d="M10 250L170 40l160 210"/><path d="M215 60l45-35 130 225"/><path d="M290 70V20h34v95"/></svg>'

ALLSUBS = [(g, s) for g in GROUPS for s in g['subs']]
def url(g, s=None): return f"{g['slug']}/" + (f"{s['slug']}/" if s else '')
def esc(t): return t.replace('&', '&amp;').replace('&amp;amp;', '&amp;')

# ---------- images ----------
_DIM = {}
def dims(f):
    if f not in _DIM: _DIM[f] = _Img.open(os.path.join(ROOT, 'img', f)).size
    return _DIM[f]
def pic(p, f, alt, chip='', cls=''):
    w, h = dims(f)
    return f'<div class="ph fit {cls}" style="aspect-ratio:{w}/{h}" data-clip><img src="{p}img/{f}" alt="{alt}" width="{w}" height="{h}" loading="lazy">{chip}</div>'

# ---------- head / header / footer ----------
def head(p, title, desc, path, extra_ld='', kw=''):
    canon = SITE + '/' + path.rstrip('/')
    ld = {"@context": "https://schema.org", "@type": "GeneralContractor", "name": NAME, "url": SITE + "/",
          "telephone": "+353851910576", "email": EMAIL, "image": SITE + "/img/extension-blockwork-hero.jpg", "logo": SITE + "/img/logo.png",
          "address": {"@type": "PostalAddress", "addressLocality": "Dublin", "addressCountry": "IE"},
          "areaServed": [{"@type": "City", "name": "Dublin"}, {"@type": "AdministrativeArea", "name": "County Dublin"}] + [{"@type": "Place", "name": t} for ts in AREAS.values() for t in ts[:6]],
          "knowsAbout": [g['name'] for g in GROUPS] + [s['name'] for g, s in ALLSUBS[:12]], "priceRange": "Free quotes",
          "aggregateRating": {"@type": "AggregateRating", "ratingValue": GOOGLE[0], "bestRating": "5", "reviewCount": GOOGLE[1]}}
    fonts = 'https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap'
    return f'''<!doctype html>
<html lang="en-IE">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{(kw + ' Dublin, ') if kw else ''}home extensions Dublin, groundworks Dublin, groundwork contractors Dublin, driveways Dublin, renovations Dublin, landscaping Dublin, foundations Dublin, JFC Construction">
<meta name="geo.region" content="IE-D"><meta name="geo.placename" content="Dublin">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#0a1630">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/img/og.jpg"><meta property="og:url" content="{canon}"><meta property="og:locale" content="en_IE">
<link rel="icon" href="{p}img/icon-192.png"><link rel="apple-touch-icon" href="{p}img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin><link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preload" as="style" href="{fonts}" onload="this.onload=null;this.rel='stylesheet'"><noscript><link rel="stylesheet" href="{fonts}"></noscript>
<link rel="stylesheet" href="{p}assets/style.css?v=1"><link rel="stylesheet" href="{p}assets/jfc.css?v=1">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>{extra_ld}'''

def header(p, active):
    def on(k): return ' class="on" aria-current="page"' if k == active else ''
    def dd(g, label=None):
        items = ''.join(f'<a href="{p}{url(g, s)}"><i>{I[s["icon"]]}</i>{s["name"]}</a>' for s in g['subs'])
        two = ' two' if len(g['subs']) > 6 else ''
        c = ' class="on"' if active == g['slug'] else ''
        return f'<div class="dd"><a href="{p}{url(g)}"{c}>{label or g["short"]} {I["chev"]}</a><div class="menu{two}">{items}<a class="all" href="{p}{url(g)}"><i>{I["arrow"]}</i>All {g["name"].lower()}</a></div></div>'
    G = {g['slug']: g for g in GROUPS}
    out_items = ''.join(f'<span class="mh">{g["name"]}</span>' + ''.join(f'<a href="{p}{url(g, s)}"><i>{I[s["icon"]]}</i>{s["name"]}</a>' for s in g['subs']) for g in (G['paving-driveways'], G['landscaping']))
    oc = ' class="on"' if active in ('paving-driveways', 'landscaping') else ''
    msubs = lambda g: ''.join(f'<a href="{p}{url(g, s)}">{s["name"]}</a>' for s in g['subs']) + f'<a href="{p}{url(g)}"><b>All {g["name"].lower()}</b></a>'
    macc = ''.join(f'<div class="macc"><button class="ml mtog" type="button" aria-expanded="false">{g["name"]} <i>{I["right"]}</i></button><div class="subs">{msubs(g)}</div></div>' for g in GROUPS)
    return f'''<div class="topbar"><div class="wrap"><span><span class="dot"></span><span>Serving Dublin &amp; surrounding areas · 20+ years</span></span>
<span class="tb-r"><a href="mailto:{EMAIL}">{I['mail']}{EMAIL}</a><a href="{TEL}">{I['phone']}Free quote: <b>{PHONE}</b></a></span></div></div>
<header class="hdr"><div class="wrap">
<a class="brand" href="{p}" aria-label="{NAME} home"><img src="{p}img/logo.png" alt="{NAME}" width="166" height="144"></a>
<nav class="nav" aria-label="Main">
{dd(G['extensions'])}{dd(G['renovations'])}{dd(G['groundworks'])}
<div class="dd"><a href="{p}paving-driveways/"{oc}>Driveways &amp; Gardens {I['chev']}</a><div class="menu two">{out_items}</div></div>
<a href="{p}our-projects/"{on('projects')}>Projects</a>
<a href="{p}about-us/"{on('about')}>About</a>
<a href="{p}contact-us/"{on('contact')}>Contact</a>
</nav>
<button class="btn btn-blue qbtn" type="button" data-qdrop aria-expanded="false" aria-controls="qdrop">Get a free quote {I['chev']}</button>
<button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span></button>
</div>{qdrop(p)}</header>
<nav class="mnav" aria-label="Mobile">
<a class="ml" href="{p}">Home <small>01</small></a>
{macc}
<a class="ml" href="{p}our-projects/">Projects <small>02</small></a>
<a class="ml" href="{p}about-us/">About Us <small>03</small></a>
<a class="ml" href="{p}reviews/">Reviews <small>04</small></a>
<a class="ml" href="{p}contact-us/">Contact <small>05</small></a>
<a class="btn btn-blue" href="#quote" data-qdrop>Get a free quote</a>
<a class="btn btn-ghost" href="{TEL}" style="margin-top:12px">{I['phone']} Call {PHONE}</a>
<div class="mfoot">Serving Dublin &amp; surrounding areas</div>
</nav>'''

OPTS = [s['name'] for g in GROUPS for s in g['subs']] + ['Other']
def form(p, title='Get a Free Quote', sub='Free site visit. No-obligation quote.', compact=False, svc=None):
    sel = ''.join(f'<optgroup label="{esc(g["name"])}">' + ''.join(f'<option{" selected" if s["name"] == svc else ""}>{esc(s["name"])}</option>' for s in g['subs']) + '</optgroup>' for g in GROUPS) + '<option>Other</option>'
    return f'''<form class="formcard{' compact' if compact else ''}" data-form novalidate>
<h3>{title}</h3><p class="sub">{sub}</p>
<div class="fmsg" role="status"></div>
<div class="fgrid">
<label class="f"><span>Phone *</span><input name="phone" type="tel" autocomplete="tel" required></label>
<label class="f"><span>Eircode *</span><input name="eircode" autocomplete="postal-code" required maxlength="8" pattern="[A-Za-z][0-9][0-9Ww] ?[0-9A-Za-z]{{4}}" placeholder="e.g. D15 RY6R" style="text-transform:uppercase" title="Your Eircode, e.g. D15 RY6R"></label>
<label class="f"><span>Name (optional)</span><input name="name" autocomplete="name"></label>
<label class="f"><span>Email (optional)</span><input name="email" type="email" autocomplete="email"></label>
<label class="f full"><span>Service (optional)</span><select name="service"><option value="">Choose a service</option>{sel}</select></label>
<label class="f full"><span>Tell us about the project (optional)</span><textarea name="message" placeholder="e.g. single-storey rear extension, about 20 m²"></textarea></label>
</div>
<input class="hp" name="botcheck" tabindex="-1" autocomplete="off" aria-hidden="true">
<button class="btn btn-blue" type="submit">Send enquiry {I['arrow']}</button>
<p class="fnote">Prefer WhatsApp? <a href="{WAURL}" target="_blank" rel="noopener">Send us photos of the job</a> · <a href="{p}privacy-policy/">Privacy</a></p>
</form>'''

def hero_form(p):
    sel = ''.join(f'<option>{esc(g["name"])}</option>' for g in GROUPS)
    return f'''<form class="hform" data-form novalidate><div class="fmsg" role="status"></div>
<div class="row"><label class="f"><input name="name" autocomplete="name" placeholder="Your name" aria-label="Your name"></label>
<label class="f"><input name="phone" type="tel" autocomplete="tel" required placeholder="Phone number *" aria-label="Phone number"></label>
<label class="f"><input name="area" placeholder="Your area" aria-label="Your area"></label>
<label class="f"><select name="service" aria-label="Service"><option value="">Service (optional)</option>{sel}</select></label></div>
<input class="hp" name="botcheck" tabindex="-1" autocomplete="off" aria-hidden="true">
<button class="btn btn-blue" type="submit">Get my free quote {I['arrow']}</button>
<p class="fnote">Free site visit, no obligation. <a href="{p}privacy-policy/">Privacy policy</a></p></form>'''

def wizard(p):
    svc = ''.join(f'<button type="button" class="wopt" data-v="{esc(g["name"])}"><i>{I[g["icon"]]}</i>{g["name"]}</button>' for g in GROUPS) + f'<button type="button" class="wopt" data-v="Something else"><i>{I["chat"]}</i>Something else</button>'
    def opts(items): return ''.join(f'<button type="button" class="wopt" data-v="{v}"><i>{I[ic]}</i><span>{v}<small>{d}</small></span></button>' for ic, v, d in items)
    prop = opts([('house', 'House', 'Semi, detached or terrace'), ('reno', 'Bungalow', 'Single storey'), ('users', 'Commercial', 'Business or landlord'), ('map', 'Development site', 'New build or site works')])
    urg = opts([('clock', 'As soon as possible', 'Ready to go'), ('calendar', 'Next 1–3 months', 'Getting quotes'), ('quote', 'Later this year', 'Planning ahead'), ('search', 'Just exploring', 'Advice for now')])
    return f'''<div class="wiz" id="wiz" role="dialog" aria-modal="true" aria-label="Free quote wizard"><div class="scrim" data-wclose></div>
<div class="wcard"><button class="x" type="button" data-wclose aria-label="Close">{I['x']}</button>
<div class="whead"><span class="wcount">Step 1 of 4</span><div class="wbar"><i></i></div></div>
<div class="wstep on" data-key="service"><h3>What are you planning?</h3><p>Pick the closest match. You can add details at the end.</p><div class="wgrid">{svc}</div></div>
<div class="wstep" data-key="property"><h3>What type of property?</h3><div class="wgrid two">{prop}</div></div>
<div class="wstep" data-key="urgency"><h3>When would you like to start?</h3><div class="wgrid two">{urg}</div></div>
<div class="wstep" data-key="details"><h3>Where should we send your free quote?</h3><div class="wsum"></div>
<form novalidate><div class="fgrid">
<label class="f"><span>Phone *</span><input name="phone" type="tel" autocomplete="tel" required></label>
<label class="f"><span>Eircode *</span><input name="eircode" autocomplete="postal-code" required maxlength="8" pattern="[A-Za-z][0-9][0-9Ww] ?[0-9A-Za-z]{{4}}" placeholder="e.g. D15 RY6R" style="text-transform:uppercase" title="Your Eircode, e.g. D15 RY6R"></label>
<label class="f"><span>Name (optional)</span><input name="name" autocomplete="name"></label>
<label class="f"><span>Town / area (optional)</span><input name="town" placeholder="e.g. Lucan, Swords"></label>
<label class="f full"><span>Anything else? (optional)</span><textarea name="details" placeholder="e.g. rear kitchen extension, roughly 5m x 4m"></textarea></label>
</div>
<div class="wbtns"><button class="btn wwa" type="button">{WA_ICON} Send on WhatsApp</button><button class="btn btn-line wmail" type="button">{I['mail']} Send request</button></div>
<p class="fnote">{I['camera'].replace('<svg', '<svg width="16" height="16" style="display:inline;vertical-align:-3px"')} Tip: on WhatsApp you can attach photos or drawings. It speeds up your quote.</p></form>
<div class="wdone"><span class="ico">{I['check']}</span><h3>Thanks, nearly done!</h3><p>Just press send in WhatsApp or your email app. We’ll come back to you to arrange your free site visit. In a hurry? Call <a href="{TEL}">{PHONE}</a>.</p></div>
</div>
<button class="wback" type="button">{I['left'].replace('<svg', '<svg width="18" height="18"')} Back</button>
</div></div>'''

def qdrop(p):
    f = form(p, 'Get a free quote', 'We aim to reply the same day.', compact=True).replace('<form class="formcard compact"', '<form class="formcard compact" id="qdform"')
    perks = '<ul class="qperks">' + ''.join(f'<li>{I["check"]}{t}</li>' for t in ['Free site visit', 'No-obligation quote', '15-year guarantee', '20+ years’ experience']) + '</ul>'
    f = f.replace('<div class="fmsg"', perks + '<div class="fmsg"', 1)
    return f'''<div class="qdrop" id="qdrop" aria-hidden="true" data-lenis-prevent><div class="wrap qdgrid">
<div class="qdside"><span class="eyebrow">Free site visit · no obligation</span><h3>Tell us about your project.</h3>
<p>A free site visit and a detailed, no-obligation quote with honest pricing. Serving Dublin &amp; surrounding areas.</p>
<a class="qdl" href="{TEL}">{I['phone']}<span><b>Call {PHONE}</b><small>Talk to the team directly</small></span></a>
<a class="qdl wa" href="{WAURL}" target="_blank" rel="noopener">{WA_ICON}<span><b>WhatsApp photos</b><small>Quickest way to a price</small></span></a>
<a class="qdl" href="#quote-wizard" data-wizard>{I['quote']}<span><b>Step-by-step quote</b><small>4 quick questions</small></span></a>
<button class="qdx" type="button" data-qclose>{I['x']} Close</button></div>
{f}</div></div>'''

def quote_drawer(p):
    f = form(p).replace('<form class="formcard"', '<form class="formcard" id="quote"').replace('<h3>', f'<button class="x" type="button" data-close aria-label="Close">{I["x"]}</button><h3>', 1)
    return f'<div class="qd" id="qd" role="dialog" aria-modal="true" aria-label="Request a quote"><div class="scrim" data-close></div>{f}</div>'

CREDIT = '<div class="almlab-credit-row" style="display:flex;justify-content:center;padding:12px 16px 4px"><a class="almlab-credit" href="https://almlabmarketing.com" target="_blank" rel="noopener" aria-label="Website by AlmLab" style="display:inline-flex;align-items:center;gap:3px;color:rgba(255,255,255,.55);font-size:11px;letter-spacing:.06em;line-height:1;text-decoration:none;white-space:nowrap"><span>Website by</span><img src="https://almlabmarketing.com/almlab-credit.png" alt="AlmLab" width="74" height="28" loading="lazy" style="height:28px;width:auto;display:block"></a></div>'

def gstrip():
    items = [('award', '20+ years', 'Trusted in Dublin'), ('shield', '15-year guarantee', 'On every job'), ('star', f'{GOOGLE[0]} on Google', f'From {GOOGLE[1]} reviews'), ('layers', 'Foundations to finish', 'One team, start to end')]
    return '<section class="gstrip"><div class="wrap">' + ''.join(f'<div>{I[a]}<span><b>{b}</b><span>{c}</span></span></div>' for a, b, c in items) + '</div></section>'

def footer(p):
    popular = [(g, s) for g, s in ALLSUBS if s['slug'] in ('home-extensions', 'kitchen-extensions', 'attic-conversions', 'foundations', 'drainage', 'driveways', 'patios', 'decking')]
    cols = '<div><h4>Services</h4><ul>' + ''.join(f'<li><a href="{p}{url(g)}">{g["name"]}</a></li>' for g in GROUPS) + f'<li><a href="{p}planning-check/">Planning Check</a></li><li><a href="{p}our-projects/">Our Projects</a></li><li><a href="{p}reviews/">Reviews</a></li><li><a href="{p}about-us/">About Us</a></li></ul></div>'
    cols += '<div><h4>Popular</h4><ul>' + ''.join(f'<li><a href="{p}{url(g, s)}">{s["name"]}</a></li>' for g, s in popular) + '</ul></div>'
    return f'''{gstrip()}
<footer class="ftr"><div class="wrap">
<div class="cols">
<div><img class="fl" src="{p}img/logo.png" alt="{NAME}" width="166" height="144" loading="lazy">
<p>Extensions, renovations, groundworks, driveways and landscaping across Dublin, from the foundations up. Over 20 years’ experience, free site visits and a 15-year guarantee on every job.</p></div>
{cols}
<div><h4>Contact</h4><ul class="ci">
<li>{I['phone']}<a href="{TEL}" data-cfg="phone">{PHONE}</a></li>
<li>{I['mail']}<a href="mailto:{EMAIL}" data-cfg="email">{EMAIL}</a></li>
<li>{I['pin']}<span>Dublin<br>Serving Dublin &amp; surrounding areas</span></li></ul>
</div>
</div>
<div class="base"><span>Copyright © <span data-cfg="year">2026</span> {NAME}. All Rights Reserved.</span>
<nav><a href="{p}privacy-policy/">Privacy Policy</a></nav></div>
</div>{CREDIT}
</footer>
<div class="fab"><a class="wa" href="{WAURL}" data-href="whatsapp" target="_blank" rel="noopener" aria-label="WhatsApp us">{WA}</a></div>
<div class="mbar"><a href="{TEL}">{I['phone']}<span>Call</span></a><a href="{WAURL}" target="_blank" rel="noopener">{WA_ICON}<span>WhatsApp</span></a><a href="#quote" data-qdrop class="q">{I['quote']}<span>Free quote</span></a></div>'''

def scripts(p):
    return f'''<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.18/dist/lenis.min.js" defer></script>
<script src="{p}assets/site.js?v=1" defer></script><script src="{p}assets/tools.js?v=1" defer></script>'''

PAGES = []
def page(path, active, title, desc, body, intro=False, extra_ld='', kw=''):
    p = '../' * path.count('/')
    h = head(p, title, desc, path, extra_ld, kw)
    loader = ''
    if intro:
        h += '\n<script>try{if(!sessionStorage.getItem("jfc_intro")||/[?&]intro/.test(location.search))document.documentElement.classList.add("intro")}catch(e){document.documentElement.classList.add("intro")}</script>'
        loader = f'''<div id="loader" class="build" aria-hidden="true"><i class="gate l"></i><i class="gate r"></i><i class="halo"></i>
<div class="stage"><div class="site"><div class="wall"></div><div class="logo"><img src="{p}img/logo.png" alt=""></div></div>
<div class="ground"><i></i></div><div class="lt">Built from the foundations up</div></div></div>'''
    intro_js = ('<script>' + open(os.path.join(ROOT, 'assets', 'intro.js'), encoding='utf-8').read() + '</script>') if intro else ''
    out = f'''{h}
</head>
<body>
{loader}{intro_js}
{header(p, active)}
<main>
{body(p)}
</main>
{footer(p)}
{quote_drawer(p)}
{wizard(p)}
{scripts(p)}
</body>
</html>
'''
    fn = os.path.join(ROOT, path, 'index.html')
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    open(fn, 'w', encoding='utf-8').write(out)
    PAGES.append(path.rstrip('/'))

# ---------- sections ----------
def stars(): return '<span class="stars" aria-label="5 stars">★★★★★</span>'
def trustlist(): return '<ul class="trust">' + ''.join(f'<li>{I["check"]}{t}</li>' for t in TRUST) + '</ul>'

def phero(p, crumb, h1, sub, img, extra=''):
    trail = ''.join(f'<span>/</span><a href="{p}{u}">{t}</a>' for t, u in crumb[:-1])
    return f'''<section class="phero" data-rain>
<img class="bg" src="{p}img/{img}" alt="" fetchpriority="high">
<div class="wrap phero-grid">
<div><div class="crumb"><a href="{p}">Home</a>{trail}<span>/</span><b>{crumb[-1][0]}</b></div>
<h1>{h1}</h1>
<p class="lead">{sub}</p>
<div class="rate">{stars()} <b>{GOOGLE[0]}</b> on Google · {GOOGLE[1]} reviews</div>
{trustlist()}
<div class="btn-row"><a class="btn btn-blue" href="#quote" data-qdrop{extra}>Get a free quote {I['arrow']}</a><a class="btn btn-ghost" href="{TEL}">{I['phone']} {PHONE}</a></div>
</div></div></section>'''

def marquee():
    items = ['Home extensions', 'Kitchen extensions', 'Attic conversions', 'Renovations', 'Site clearance', 'Excavations', 'Foundations', 'Drainage', 'Driveways', 'Patios', 'Landscaping', 'Dublin & surrounding areas']
    s = ''.join(f'<span>{t}</span>' for t in items)
    return f'<div class="marquee" aria-hidden="true"><div class="track">{s}{s}</div></div>'

def compare(p, b, a, t='', sub=''):
    w, h = dims(b)
    return f'''<figure class="ba"><div class="compare" style="aspect-ratio:{w}/{h}"><img class="after" src="{p}img/{a}" alt="{t or 'Project'} after, by JFC Construction" loading="lazy"><img class="before" src="{p}img/{b}" alt="{t or 'Project'} before" loading="lazy">
<span class="tag l">Before</span><span class="tag r">After</span><span class="handle"></span>
<input type="range" min="0" max="100" value="50" aria-label="Drag to compare before and after"></div>
{f'<figcaption>{t}<span>{sub}</span></figcaption>' if t else ''}</figure>'''

def ba_section(p, soft=True, title='Recent Dublin jobs.'):
    items = ''.join(compare(p, b, a, esc(t), c) for b, a, t, c in BA)
    return f'''<section class="sec{' soft' if soft else ''}"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">Before &amp; after</span><h2 data-split>{title}</h2></div>
<a class="btn btn-line" href="{p}our-projects/">See all projects {I['arrow']}</a></div>
<div class="ba-grid g3" data-reveal="group">{items}</div></div></section>'''

def group_cards(p):
    return '<div class="sgrid" data-reveal="group">' + ''.join(f'''<a class="scard" href="{p}{url(g)}"><img src="{p}img/{g['card']}" alt="{esc(g['name'])} in Dublin by JFC Construction" loading="lazy">
<span class="num">{I[g['icon']]}</span><span class="go">{I['arrow']}</span><h3>{g['name']}</h3><p>{g['lead'][:140].rsplit(' ', 1)[0]}…</p><span class="tlink">{len(g['subs'])} services {I['arrow']}</span></a>''' for g in GROUPS) + '</div>'

def sub_cards(p, g, items=None):
    items = items or g['subs']
    return '<div class="sgrid" data-reveal="group">' + ''.join(f'''<a class="scard" href="{p}{url(g, s)}"><img src="{p}img/{s['img']}" alt="{esc(s['name'])} in Dublin" loading="lazy">
<span class="num">{I[s['icon']]}</span><span class="go">{I['arrow']}</span><h3>{s['name']}</h3><p>{s['blurb']}</p><span class="tlink">Read more {I['arrow']}</span></a>''' for s in items) + '</div>'

def subgrid(p, g, skip=None):
    return '<div class="subgrid" data-reveal="group">' + ''.join(f'<a href="{p}{url(g, s)}"><i>{I[s["icon"]]}</i><span>{s["name"]}<small>{s["blurb"][:70].rsplit(" ", 1)[0]}…</small></span></a>' for s in g['subs'] if s is not skip) + '</div>'

def process(p, soft=True):
    st = ''.join(f'<div class="step"><div class="n">0{i}</div><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(STEPS, 1))
    return f'''<section class="sec{' soft' if soft else ''}"><div class="wrap">
<div class="center" style="margin-bottom:48px"><span class="eyebrow">How we get the job done</span><h2 data-split>Simple steps, no surprises.</h2></div>
<div class="steps s4" data-reveal="group">{st}</div></div></section>'''

def why():
    c = ''.join(f'<div class="card"><span class="ico">{I[a]}</span><h3>{b}</h3><p>{t}</p></div>' for a, b, t in WHY)
    return f'''<section class="sec deep"><div class="wrap" style="position:relative;z-index:2">
<div class="sec-head"><div><span class="eyebrow">Why choose JFC</span><h2 data-split>Why Dublin homeowners choose JFC.</h2></div>
<p>An extension is a big investment and a big disruption to daily life. Dublin homeowners choose us for clear communication, careful workmanship and a team that looks after the job from the first dig to the final clean-up.</p></div>
<div class="cards c4" data-reveal="group">{c}</div></div></section>'''

def review_cards(rs, cls='rgrid'):
    return f'<div class="{cls}" data-reveal="group">' + ''.join(f'''<div class="review"><div class="stars">★★★★★</div><q>{t}</q>
<div class="who"><span class="av">{n[0]}</span><div><b>{n}</b><span>Google review</span></div></div></div>''' for n, t in rs) + '</div>'

def reviews_sec(p, rs=None):
    rs = rs or REVIEWS[:3]
    return f'''<section class="sec dark"><div class="wrap" style="position:relative;z-index:2">
<div class="sec-head"><div><span class="eyebrow">What our customers say</span><h2 data-split>Rated {GOOGLE[0]} from {GOOGLE[1]} Google reviews.</h2></div>
<a class="btn btn-ghost" href="{p}reviews/">Read more reviews {I['arrow']}</a></div>
{review_cards(rs, 'rgrid r3' if len(rs) == 3 else 'rgrid')}</div></section>'''

def area_box(dark=False):
    return f'''<form class="areabox{' dark' if dark else ''}" data-area><label for="areain"><b>{I['map']} Do we cover your area?</b><span>Type your town</span></label>
<div class="arow"><input id="areain" list="areas" placeholder="e.g. Lucan, Swords, Dundrum" autocomplete="off"><button class="btn btn-blue" type="submit">Check</button></div>
<datalist id="areas"></datalist><div class="area-out" aria-live="polite"></div></form>'''

def areas_sec(p, soft=False):
    cols = ''.join(f'<div class="area"><h3>{I["pin"]}{c}</h3><div class="chips">{"".join(f"<span>{t}</span>" for t in ts)}</div></div>' for c, ts in AREAS.items())
    return f'''<section class="sec{' soft' if soft else ''}"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">Areas we cover</span><h2 data-split>Working across Dublin’s council areas.</h2></div>
<p>Extensions, renovations, groundworks, driveways and landscaping across Dublin city and county, north, south and west, and the surrounding areas.</p></div>
<div class="areas" data-reveal="group">{cols}</div>
<div style="margin-top:28px;max-width:560px">{area_box()}</div>
</div></section>'''

def planning_teaser(p):
    return f'''<section class="sec deep hteaser"><div class="wrap split" style="position:relative;z-index:2">
<div><span class="eyebrow">Free online tool</span><h2 data-split>Do you need planning permission? Take the 60-second check.</h2>
<p class="lead">Answer six quick questions about your extension, garden room or conversion and see whether it sounds like exempted development, borderline or a planning application. Then book a free site visit to be sure.</p>
<a class="btn btn-blue" href="{p}planning-check/">Start the planning check {I['arrow']}</a></div>
<div class="gaugecard" data-reveal><div class="gauge"><svg viewBox="0 0 200 120"><path d="M20 110a80 80 0 0 1 160 0" fill="none" stroke="rgba(255,255,255,.1)" stroke-width="18" stroke-linecap="round"/><path d="M20 110a80 80 0 0 1 160 0" fill="none" stroke="url(#gg)" stroke-width="18" stroke-linecap="round" stroke-dasharray="251" stroke-dashoffset="70"/><defs><linearGradient id="gg"><stop offset="0" stop-color="#35c46a"/><stop offset=".5" stop-color="#ffb81c"/><stop offset="1" stop-color="#f28a2e"/></linearGradient></defs><line x1="100" y1="110" x2="150" y2="60" stroke="#fff" stroke-width="5" stroke-linecap="round"/><circle cx="100" cy="110" r="9" fill="#fff"/></svg></div>
<div class="glabels"><span>Exempt</span><span>Borderline</span><span>Planning</span></div></div>
</div></section>'''

def cta(p, h='Ready to plan your Dublin project?'):
    return f'''<section class="cta">{HOUSE_SVG}<div class="wrap">
<div><span class="eyebrow">Free site visit · no-obligation quote</span><h2 data-split>{h}</h2>
<p>Free site visit. No-obligation quote. 15-year guarantee on every job.</p></div>
<div class="btn-row"><a class="btn btn-white" href="#quote" data-qdrop>Request a free quote {I['arrow']}</a><a class="btn btn-ghost" href="{TEL}">{I['phone']} {PHONE}</a></div>
</div></section>'''

def faq_block(p, faqs):
    return '<div class="faqs">' + ''.join(f'<details class="faq"><summary>{q}<i>{I["chev"]}</i></summary><p>{a.replace("{p}", p)}</p></details>' for q, a in faqs) + '</div>'

def faq_ld(faqs):
    import re
    return '\n<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', a)}} for q, a in faqs]}, ensure_ascii=False) + '</script>'

def tiles(p, files, alt):
    return '<div class="boxes b3" data-reveal="group">' + ''.join(f'<a class="tile" href="{p}img/{f}"><img src="{p}img/{f}" alt="{alt}" loading="lazy"></a>' for f in files) + '</div>'

def quote_sec(p, svc=None, title='Tell us about your project.'):
    return f'''<section class="sec"><div class="wrap split" style="align-items:start">
<div><span class="eyebrow">Free quote</span><h2 data-split>{title}</h2><p>Free site visit and a detailed, no-obligation quote with honest pricing. We look at access, ground conditions and any drawings you have.</p>
{area_box()}<div class="contactmini"><a href="{TEL}">{I['phone']}{PHONE}</a><a href="{WAURL}" target="_blank" rel="noopener">{WA_ICON}WhatsApp photos</a></div></div>
<div data-reveal>{form(p, 'Get a Free Quote', 'We aim to reply the same day.', svc=svc)}</div></div></section>'''

# ---------- pages ----------
def home(p):
    G = {g['slug']: g for g in GROUPS}
    return f'''<section class="hero hjfc">
<div class="wrap">
<div>
<div class="gbadge">{stars()}<b>{GOOGLE[0]}</b> on Google · {GOOGLE[1]} reviews</div>
<span class="eyebrow">Serving Dublin &amp; surrounding areas</span>
<h1>Home extensions in Dublin, <span class="blue">built from the foundations up.</span></h1>
<p class="lead">From first excavation to final finish, we build extensions, renovations, driveways and gardens across Dublin. Because we handle the groundworks ourselves, your project starts on solid foundations and stays under one team’s control.</p>
{hero_form(p)}
<div class="btn-row"><a class="btn btn-ghost" href="{TEL}">{I['phone']} Call {PHONE}</a><span class="guar">{I['shield']}15-year guarantee on every job</span></div>
</div>
<div class="hphoto" data-reveal><span class="chip">Recent work · Dublin</span><img src="{p}img/extension-blockwork-hero.jpg" alt="Single-storey extension blockwork by JFC Construction in Dublin" width="1600" height="1600" fetchpriority="high">
<div class="float">{I['award'].replace('<svg', '<svg width="34" height="34" style="color:var(--blue);flex:none"')}<div><b>20+ years</b><span>of construction &amp; groundwork in Dublin</span></div></div></div>
</div>
<div class="scroll">Scroll</div>
</section>
{marquee()}
<section class="sec"><div class="wrap split">
<div><span class="eyebrow">Extension specialists in Dublin</span>
<h2 data-split>Foundations to finish, one team.</h2>
<p class="lead" style="color:var(--ink)">Whether you want a bigger kitchen, an extra bedroom in the attic, a converted garage or a garden room, we build extensions across Dublin with the same care we give to the foundations underneath.</p>
<p>For over 20 years, JFC Construction &amp; Groundwork has delivered groundwork and construction services in Dublin for homeowners, businesses and property developers. Our commitment to quality workmanship, reliable service and attention to detail has made us a trusted contractor, completing every project to the highest standards.</p>
<ul class="ticks cols2">{''.join(f'<li>{I["check"]}{t}</li>' for t in ['Free site visit & quote', '15-year guarantee', 'Groundworks done in-house', 'Clear, honest pricing'])}</ul>
<div class="btn-row" style="margin-top:24px"><a class="btn btn-line" href="{p}about-us/">About us {I['arrow']}</a><a class="btn btn-blue" href="#quote" data-qdrop>Get a free quote {I['arrow']}</a></div></div>
{pic(p, 'extension-slab.jpg', 'Extension floor slab with steel mesh ready for concrete, Dublin', f'<span class="chip">{I["pin"]}Extension slab, Dublin</span>')}
</div></section>
<section class="sec soft"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">Our extension services</span><h2 data-split>Here’s what we can build for your home.</h2></div>
<p>Rear and side extensions, kitchens, attics, garages and garden rooms, all starting on foundations we dig and pour ourselves.</p></div>
{sub_cards(p, G['extensions'], G['extensions']['subs'] + [])}
<div class="btn-row" style="margin-top:28px"><a class="btn btn-line" href="{p}extensions/">All extension services {I['arrow']}</a></div></div></section>
{ba_section(p, soft=False)}
<section class="sec soft"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">Everything we do</span><h2 data-split>Construction &amp; groundwork, under one roof.</h2></div>
<p>From the ground under your feet to the rooms inside your home, one team for the whole job.</p></div>
{group_cards(p)}</div></section>
{why()}
{process(p, soft=False)}
{planning_teaser(p)}
{areas_sec(p, soft=True)}
{reviews_sec(p)}
{cta(p)}'''

def group_page(g):
    def body(p):
        return f'''{phero(p, [(g['name'], url(g))], g['h1'], g['lead'], g['hero'])}
{marquee()}
<section class="sec"><div class="wrap split">
<div><span class="eyebrow">{g['eyebrow']}</span><h2 data-split>{g['name']} done properly.</h2>{''.join(f'<p>{x}</p>' for x in g['intro'])}
<div class="callrow"><a class="btn btn-blue" href="#quote" data-qdrop>Get a free quote {I['arrow']}</a><div><small>Prefer to call?</small><a class="num" href="{TEL}">{PHONE}</a></div></div></div>
{pic(p, g['photos'][0], g['name'] + ' in Dublin by JFC Construction & Groundwork')}
</div></section>
<section class="sec soft"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">{g['name']} services</span><h2 data-split>What we cover.</h2></div><p>Choose a service to find out more, or get in touch and tell us about the whole project.</p></div>
{sub_cards(p, g)}</div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Recent work</span><h2 data-split>From our Dublin jobs.</h2></div><a class="btn btn-line" href="{p}our-projects/">See all projects {I['arrow']}</a></div>
{tiles(p, g['photos'][1:], g['name'] + ' by JFC Construction, Dublin')}</div></section>
{why()}
{reviews_sec(p)}
<section class="sec"><div class="wrap split" style="align-items:start">
<div><span class="eyebrow">FAQs</span><h2 data-split>{g['name']}: your questions.</h2>{faq_block(p, g['faq'])}</div>
<div data-reveal>{form(p, 'Get a Free Quote', 'Free site visit. No-obligation quote.')}</div></div></section>
{process(p)}
{cta(p)}'''
    return body

def sub_page(g, s):
    def body(p):
        others = [o for o in g['subs'] if o is not s]
        items = ''.join(f'<li>{I["check"]}{x}</li>' for x in s['items'])
        gal = [f for f in g['photos'] if f != s['img']][:3]
        return f'''{phero(p, [(g['name'], url(g)), (s['name'], url(g, s))], s['name'] + ' <span class="blue">in Dublin.</span>', s['blurb'], g['hero'], f' data-svc="{esc(s["name"])}"')}
{marquee()}
<section class="sec"><div class="wrap split">
<div><span class="eyebrow">{s['name']} Dublin</span><h2 data-split>{s['name']}, from the foundations up.</h2>
<p>{s['blurb']}</p>
<p>JFC Construction &amp; Groundwork has over 20 years’ experience across Dublin. Because we do our own groundworks, the parts you never see, like levels, drainage and the base underneath, are done right, and your project isn’t passed between different contractors.</p>
<h3 style="margin-top:28px">What’s included</h3><ul class="ticks cols2">{items}</ul>
<div class="callrow"><a class="btn btn-blue" href="#quote" data-qdrop data-svc="{esc(s['name'])}">Get a free quote {I['arrow']}</a><div><small>Prefer to call?</small><a class="num" href="{TEL}">{PHONE}</a></div></div></div>
{pic(p, s['img'], s['name'] + ' in Dublin by JFC Construction & Groundwork')}
</div></section>
<section class="sec soft"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Recent work</span><h2 data-split>From our Dublin jobs.</h2></div><a class="btn btn-line" href="{p}our-projects/">See all projects {I['arrow']}</a></div>
{tiles(p, gal, g['name'] + ' by JFC Construction, Dublin')}</div></section>
{why()}
{reviews_sec(p, [REVIEWS[(GROUPS.index(g) * 2 + g['subs'].index(s) + i) % len(REVIEWS)] for i in range(3)])}
{quote_sec(p, s['name'])}
<section class="sec soft"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">More {g['name'].lower()}</span><h2 data-split>More ways we can help.</h2></div><a class="btn btn-line" href="{p}{url(g)}">All {g['name'].lower()} {I['arrow']}</a></div>
{subgrid(p, g, s)}</div></section>
<section class="sec"><div class="wrap split" style="align-items:start"><div><span class="eyebrow">FAQs</span><h2 data-split>Your questions.</h2></div>{faq_block(p, g['faq'])}</div></section>
{process(p)}
{cta(p)}'''
    return body

def about(p):
    return f'''{phero(p, [('About Us', 'about-us/')], 'Over 20 years of trusted construction &amp; groundwork <span class="blue">in Dublin.</span>', 'Professional groundwork and construction services in Dublin for homeowners, businesses and property developers.', 'ai-foundations-sunset.jpg')}
<section class="sec"><div class="wrap split">
<div><span class="eyebrow">About us</span><h2 data-split>About JFC Construction &amp; Groundwork.</h2>
<p class="lead" style="color:var(--ink)">For over 20 years, JFC Construction &amp; Groundwork has been delivering professional groundwork and construction services in Dublin for homeowners, businesses, and property developers.</p>
<p>Our commitment to quality workmanship, reliable service, and attention to detail has made us a trusted groundwork contractor in Dublin, completing every project to the highest industry standards.</p>
<p>Our experienced team specialises in site clearance, site preparation, excavations, foundations, drainage, concrete works, driveways, patios, paving, fencing, landscaping, and external construction services across Dublin. No matter the size of the project, we focus on delivering safe, efficient, and long-lasting results.</p>
<a class="btn btn-blue" href="{p}contact-us/">Contact us {I['arrow']}</a></div>
{pic(p, 'blockwork-3.jpg', 'JFC Construction team building extension blockwork in Dublin')}
</div></section>
<section class="sec soft"><div class="wrap split rev">
<div><h2 data-split>Building strong foundations, creating lasting results.</h2>
<p>At JFC Construction &amp; Groundwork, we take pride in providing dependable construction and groundwork services throughout Dublin. From preparing development sites and installing drainage systems to building foundations and transforming outdoor spaces, we deliver practical solutions tailored to every client’s needs.</p>
<p>As experienced groundwork specialists in Dublin, we combine skilled craftsmanship, modern equipment, and over 20 years of industry expertise to complete residential and commercial projects with precision and professionalism.</p>
<p>Whether you need excavation, foundations, concrete works, an extension or complete landscaping, you can rely on our team to deliver results that stand the test of time.</p></div>
{pic(p, 'concrete-pour.jpg', 'Concrete pour for a new base by JFC Construction')}
</div></section>
<section class="sec deep"><div class="wrap"><div class="jstats">
<div><b>20+</b><span>Years’ experience</span></div><div><b>15yr</b><span>Guarantee on every job</span></div><div><b>{GOOGLE[0]}★</b><span>From {GOOGLE[1]} Google reviews</span></div><div><b>42</b><span>Services, one team</span></div></div></div></section>
{ba_section(p)}
{why()}
{reviews_sec(p, REVIEWS[3:])}
{process(p)}
{cta(p)}'''

GALLERY = [('extension-blockwork-hero.jpg', 'ext'), ('blockwork-1.jpg', 'ext'), ('blockwork-2.jpg', 'ext'), ('blockwork-3.jpg', 'ext'), ('blockwork-4.jpg', 'ext'), ('extension-slab.jpg', 'ext ground'), ('garden-room-base.jpg', 'ext ground'),
           ('foundations-after.jpg', 'ground'), ('foundations-before.jpg', 'ground'), ('concrete-pour.jpg', 'ground'), ('concrete-slab.jpg', 'ground'), ('floor-drain.jpg', 'reno'),
           ('open-plan-after.jpg', 'reno'), ('open-plan-before.jpg', 'reno'), ('stud-wall-stairs.jpg', 'reno'), ('interior-fitout.jpg', 'reno'), ('floor-joists.jpg', 'reno'), ('first-fix-after.jpg', 'reno'),
           ('tanking-1.jpg', 'reno'), ('tanking-2.jpg', 'reno'), ('tanking-3.jpg', 'reno'), ('tanking-4.jpg', 'reno'),
           ('porcelain-patio.jpg', 'outdoor'), ('patio-artificial-grass.jpg', 'outdoor'), ('patio-slabs-turf.jpg', 'outdoor'), ('patio-turf-tall.jpg', 'outdoor'), ('patio-garden-walls.jpg', 'outdoor'), ('garden-wall-render.jpg', 'outdoor'),
           ('garden-prep-gravel.jpg', 'outdoor ground'), ('side-passage.jpg', 'outdoor'), ('side-passage-wall.jpg', 'outdoor'), ('decking-1.jpg', 'outdoor'), ('decking-2.jpg', 'outdoor'), ('decking-3.jpg', 'outdoor'), ('decking-frame.jpg', 'outdoor')]
def projects(p):
    g = ''.join(f'<a class="tile" href="{p}img/{f}" data-cat="{c}"><img src="{p}img/{f}" alt="Construction and groundwork project by JFC Construction, Dublin" loading="lazy"></a>' for f, c in GALLERY)
    fb = ''.join(f'<button type="button" data-f="{k}"{" class=\"on\"" if k == "all" else ""}>{v}</button>' for k, v in [('all', 'All work'), ('ext', 'Extensions'), ('reno', 'Renovations'), ('ground', 'Groundworks'), ('outdoor', 'Driveways & gardens')])
    sl = ''.join(compare(p, b, a, esc(t), c) for b, a, t, c in BA)
    return f'''{phero(p, [('Our Projects', 'our-projects/')], 'Our projects <span class="blue">across Dublin.</span>', 'Our portfolio shows the quality and care we bring to every project: the foundations, structural work and renovations that sit behind a successful build.', 'blockwork-3.jpg')}
<section class="sec soft"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Drag to compare</span><h2 data-split>Before &amp; after.</h2></div><p>Drag the slider across each photo to see the difference.</p></div>
<div class="ba-grid g3" data-reveal="group">{sl}</div></div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Project gallery</span><h2 data-split>Our work.</h2></div><p>Tap any photo to see it full size.</p></div>
<div class="filters" data-filters="#galgrid">{fb}</div>
<div class="boxes" id="galgrid">{g}</div></div></section>
{reviews_sec(p)}
{cta(p)}'''

def reviews(p):
    return f'''{phero(p, [('Reviews', 'reviews/')], 'What our <span class="blue">customers say.</span>', f'Rated {GOOGLE[0]} out of 5 from {GOOGLE[1]} Google reviews. Here’s what some of our customers have to say.', 'porcelain-patio.jpg')}
<section class="sec"><div class="wrap">
<div class="revtop"><div class="big5"><b>{GOOGLE[0]}</b>{stars()}<span>Based on {GOOGLE[1]} Google reviews</span></div></div>
<div id="revwall">{review_cards(REVIEWS, 'rwall')}</div></div></section>
{ba_section(p)}
{cta(p)}'''

def contact(p):
    return f'''<section class="phero chero" data-rain>
<img class="bg" src="{p}img/blockwork-1.jpg" alt="" fetchpriority="high">
<div class="wrap chgrid">
<div data-reveal>{form(p, 'Get a Free Quote', 'Free site visit. No-obligation quote. We aim to reply the same day.')}</div>
<div><div class="crumb"><a href="{p}">Home</a><span>/</span><b>Contact Us</b></div>
<h1>Contact <span class="blue">JFC Construction &amp; Groundwork.</span></h1>
<p class="lead">Tell us what you would like to build and we will arrange a free site visit to talk it through. Fill out the form and we’ll get back to you as soon as possible.</p>
<ul class="clist">
<li><a href="{TEL}">{I['phone']}<span><small>Call</small><b data-cfg="phone">{PHONE}</b></span></a></li>
<li><a href="mailto:{EMAIL}">{I['mail']}<span><small>Email</small><b data-cfg="email">{EMAIL}</b></span></a></li>
<li><a href="{WAURL}" target="_blank" rel="noopener">{WA_ICON}<span><small>WhatsApp</small><b>Send us photos of the job</b></span></a></li>
<li><span class="nolink">{I['pin']}<span><small>Location</small><b>Dublin &amp; surrounding areas</b></span></span></li>
</ul></div>
</div></section>
<section class="sec"><div class="wrap split" style="align-items:start">
<div><span class="eyebrow">Service areas</span><h2 data-split>Working across Dublin.</h2>
<p>We work across Dublin’s council areas, north, south and west, and the surrounding areas.</p>
{area_box()}</div>
<div class="map"><iframe title="JFC Construction & Groundwork: Dublin" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=Dublin%2C%20Ireland&amp;z=10&amp;output=embed"></iframe></div>
</div></section>
{cta(p)}'''

def planning(p):
    qs = ''.join(f'<div class="hq"><span class="hn">0{i}</span><h3>{q}</h3><div class="hopts">{"".join(f"<button type=button data-s={s}>{t}</button>" for t, s in o)}</div></div>' for i, (q, o) in enumerate(PQ, 1))
    return f'''{phero(p, [('Planning Check', 'planning-check/')], 'Do I need planning permission <span class="blue">for my extension?</span>', 'Answer six quick questions about your extension, garden room or conversion. We’ll tell you what it sounds like, then you can book a free site visit to be sure.', 'ai-new-build.jpg')}
<section class="sec"><div class="wrap health" id="health">
<div class="hqs"><div class="hhead"><span class="hcount">0 of 6 answered</span><div class="hprog"><i></i></div><button class="hreset" type="button">Start again</button></div>{qs}</div>
<aside class="hside"><div class="hres"><span class="eyebrow">Your result</span><h3></h3><div class="hscore"><i></i></div><div class="glabels"><span>Exempt</span><span>Borderline</span><span>Planning</span></div><p></p>
<div class="btn-row"><a class="btn btn-blue" href="#quote" data-qdrop>Book a free site visit {I['arrow']}</a><a class="btn btn-line hlink" data-base="{p}" href="{p}extensions/home-extensions/">About home extensions</a></div>
<p class="fnote" style="text-align:left">A guide only, based on the exempted development rules for houses. It isn’t legal advice; for certainty, check with your local council or ask for a Section 5 declaration.</p></div>
<div class="hwait"><span class="ico">{I['gauge']}</span><h3>Your result appears here</h3><p>Answer all six questions to see whether your project sounds exempt, borderline or likely to need planning permission.</p></div></aside>
</div></section>
{cta(p)}'''

def privacy(p):
    secs = [('What information do you hold on me?', 'Whenever you use one of the forms on this website to contact us, we keep a record of the details you send, such as your name, phone number, Eircode, email and message, in our email inbox.'),
            ('Why do you keep my personal data?', 'We keep a record of your personal data so we can contact you about your original request. We will not use it for any other purpose, such as newsletters, and we will not sell or give it to third parties.'),
            ('Who has access to my personal data?', f'Only people working at {esc(NAME)} who need it to respond to your enquiry.'),
            ('What happens in case of a security breach?', 'In the unlikely event your data is lost, stolen or accessed without authority, you and the Data Protection Commission will be notified within 72 hours.'),
            ('How can I control my personal data?', f'To see the information we hold on you, email <a class="blue" href="mailto:{EMAIL}">{EMAIL}</a> and we will send you a copy. You can also ask us to delete it completely.'),
            ('Cookies and technical information', 'This website does not use advertising or tracking cookies. It stores one item in your browser’s session storage so the opening animation only plays once per visit. The map on the contact page is provided by Google, which may set its own cookies. Our hosting provider may log technical details of visits for security purposes.'),
            ('Security', 'Your personal data is held securely. We cannot guarantee the security of information sent over the internet, but we take all reasonable technical and organisational steps to protect it.')]
    return f'''{phero(p, [('Privacy Policy', 'privacy-policy/')], 'Privacy policy.', 'How we handle your personal data.', 'porcelain-patio.jpg')}
<section class="sec"><div class="wrap article"><p>This policy explains how {esc(NAME)} handles personal data, in line with the EU General Data Protection Regulation (GDPR).</p>
{''.join(f'<h2>{a}</h2><p>{b}</p>' for a, b in secs)}</div></section>
{cta(p)}'''

if __name__ == '__main__':
    page('', 'home', 'Home Extensions & Groundworks Dublin | JFC Construction & Groundwork', 'Home extensions, renovations, groundworks, driveways and landscaping across Dublin, built from the foundations up. 20+ years, 15-year guarantee, free site visit and quote.', home, intro=True, extra_ld='')
    for g in GROUPS:
        page(url(g), g['slug'], f"{g['name']} Dublin | JFC Construction & Groundwork", esc(g['lead']), group_page(g), extra_ld=faq_ld(g['faq']), kw=g['name'])
        for s in g['subs']:
            page(url(g, s), g['slug'], f"{s['name']} Dublin | JFC Construction & Groundwork", esc(s['blurb'])[:155], sub_page(g, s), kw=s['name'])
    page('about-us/', 'about', 'About Us | JFC Construction & Groundwork Dublin', 'Over 20 years of trusted construction and groundwork services in Dublin for homeowners, businesses and property developers.', about)
    page('our-projects/', 'projects', 'Our Projects | JFC Construction & Groundwork Dublin', 'Before and after photos of extensions, renovations, groundworks, patios, decking and driveways by JFC Construction & Groundwork in Dublin.', projects)
    page('reviews/', 'reviews', 'Reviews | JFC Construction & Groundwork Dublin', f'Rated {GOOGLE[0]} from {GOOGLE[1]} Google reviews. Read what Dublin customers say about JFC Construction & Groundwork.', reviews)
    page('contact-us/', 'contact', 'Contact Us | JFC Construction & Groundwork Dublin', f'Contact JFC Construction & Groundwork for a free site visit and quote. Call {PHONE} or email {EMAIL}.', contact)
    page('planning-check/', 'extensions', 'Do I Need Planning Permission for an Extension? | JFC Construction', 'Free 60-second check: answer six questions to see whether your extension or garden room sounds exempt, borderline or likely to need planning permission.', planning)
    page('privacy-policy/', '', 'Privacy Policy | JFC Construction & Groundwork', 'How JFC Construction & Groundwork handles your personal data.', privacy)
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{SITE}/{u}</loc></url>\n' for u in PAGES) + '</urlset>\n')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
    print('built', len(PAGES), 'pages')
