# JFC Construction & Groundwork website

Static multi-page site for jfcconstruction.ie, built in the same style as the Kiely and Vantage sites (navy + JFC orange, serif headlines, quote form in the hero). No build step needed to host it: upload this folder as-is (Vercel, Netlify, any web host).

- **54 pages.** Home, 5 category pages (`/extensions`, `/renovations`, `/groundworks`, `/paving-driveways`, `/landscaping`), all 42 service pages at the **same addresses as the old site** (e.g. `/extensions/home-extensions`) so Google rankings carry over, plus About, Our Projects, Reviews, Contact, Planning Check and Privacy.
- **Extras:** hero quote form, drop-down quote panel, 4-step quote wizard (WhatsApp or email), "Do we cover your area?" checker (Dublin towns), extension planning-permission checker, before/after sliders, gallery filters, sticky Call / WhatsApp / Quote bar on phones, opening animation (plays once per visit; add `?intro` to replay).
- **To edit words:** change `content.py`, then run `python3 build.py` (needs Pillow). It also regenerates `sitemap.xml` and `robots.txt`.
- **Contact details** for the scripts are at the top of `assets/site.js` and `assets/tools.js`.
- **Forms:** paste JFC's own free Web3Forms access key into `formKey` in `assets/site.js` to receive enquiries by email. Until then, forms open the visitor's email app pre-filled to info@jfcconstruction.ie.

## Still to confirm with the client
- Email address `info@jfcconstruction.ie` (decoded from the old site; check it's live).
- Opening hours and street address (not on the old site, so not shown).
- Facebook / Instagram links (the old site's Facebook link was a placeholder).
- Sharper originals of the WhatsApp project photos: the old site only has 300px copies, so the before/after sliders and some cards are soft.
- Some category images are the AI-generated ones from the old site; swap in real job photos when available.
