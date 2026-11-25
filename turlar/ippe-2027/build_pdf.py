#!/usr/bin/env python3
"""IPPE Atlanta 2027 (5 gece) teklif PDF'ini üretir: python3 build_pdf.py

1, 2, 4 ve 5. sayfalar HTML'den Chromium ile basılır (form alanları Chromium'un
<input name> alanlarından oluşur). 3. sayfa (Atlanta Hakkında, haritalar) ilk
teklif PDF'inden aynen alınır; yalnızca alt bilgideki "4 gece" ibaresi "5 gece"
olarak yenilenir. Gerekenler: Playwright (Node), pymupdf, Inter fontu.
"""
import pathlib, subprocess, json, pymupdf

H = pathlib.Path(__file__).resolve().parent
SRC = H / "IPPE-Atlanta-2027-Fuar-Turu-5-Gece.html"
OUT = H / "IPPE-Atlanta-2027-Fuar-Turu-5-Gece.pdf"
ORIG = H / "IPPE-Atlanta-2027-Fuar-Turu-4-Gece-ilk-teklif.pdf"
TMP = H / ".render.pdf"
INTER = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"

JS = f"""
const {{chromium}} = require('playwright');
(async () => {{
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://{SRC}'); await p.evaluate(() => document.fonts.ready);
  await p.emulateMedia({{media: 'print'}});
  const f = await p.evaluate(() => [...document.querySelectorAll('input,textarea')].map(e => {{
    const r = e.getBoundingClientRect(), pg = e.closest('section'), q = pg.getBoundingClientRect();
    return {{name: e.name, type: e.type, req: e.required, multi: e.tagName == 'TEXTAREA',
      page: [...document.querySelectorAll('section')].indexOf(pg), x: r.left - q.left, y: r.top - q.top, w: r.width, h: r.height}}; }}));
  require('fs').writeFileSync('{TMP}.json', JSON.stringify(f));
  await p.pdf({{path: '{TMP}', format: 'A4', printBackground: true, preferCSSPageSize: true}});
  await b.close();
}})();"""
subprocess.run(["node", "-e", JS], check=True)

doc = pymupdf.open(TMP)
orig = pymupdf.open(ORIG)
p3 = orig[2]
# alt bilgi solundaki "IPPE Atlanta 2027 Fuar Turu · 4 gece" metnini yenile
hits = p3.search_for("IPPE Atlanta 2027 Fuar Turu · 4 gece")
assert hits, "3. sayfa alt bilgisi bulunamadı"
r = hits[0]
p3.add_redact_annot(r + (-1, -1, 1, 1), fill=(1, 1, 1))
p3.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)
p3.insert_font(fontname="inter", fontfile=INTER)
p3.insert_text((r.x0, r.y1 - 1.6), "IPPE Atlanta 2027 Fuar Turu · 5 gece",
               fontname="inter", fontsize=7.4, color=(0.42, 0.45, 0.5))

doc.delete_page(2)
doc.insert_pdf(orig, from_page=2, to_page=2, start_at=2)
# doldurulabilir form alanları (CSS px → pt: ×0,75)
for e in json.loads(pathlib.Path(f"{TMP}.json").read_text()):
    w = pymupdf.Widget()
    w.field_name = e["name"]
    w.rect = pymupdf.Rect(e["x"], e["y"], e["x"] + e["w"], e["y"] + e["h"]) * 0.75
    if e["type"] == "checkbox":
        w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
        w.field_value = False
    else:
        w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
        w.text_fontsize = 0 if e["multi"] else 9
        w.text_font = "Helv"
    w.field_flags = (2 if e["req"] else 0) | (4096 if e["multi"] else 0)
    w.border_width = 0
    doc[e["page"]].add_widget(w)

doc.set_metadata({"title": "IPPE Atlanta 2027 Fuar Turu – Fuartour", "author": "Fuartour"})
doc.save(OUT, garbage=3, deflate=True)
TMP.unlink(); pathlib.Path(f"{TMP}.json").unlink()
print("yazıldı:", OUT)
