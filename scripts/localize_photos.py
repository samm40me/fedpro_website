#!/usr/bin/env python3
"""Download and locally store illustrative oil-and-gas imagery.
Images are illustrative, not representations of FEDPRO projects.
"""
import json, pathlib, urllib.parse, urllib.request
from PIL import Image
from io import BytesIO

ROOT=pathlib.Path(__file__).resolve().parents[1]
ASSETS=ROOT/"assets"
ASSETS.mkdir(exist_ok=True)
UA="FEDPROWebsite/1.0 (website asset curation; info@fedpro.com)"
SEARCHES={
 "offshore-platform":"offshore oil platform",
 "exploration":"offshore oil exploration vessel",
 "asset-management":"petroleum engineer control room",
 "well-intervention":"offshore drilling rig",
}
def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,image/*"})
    with urllib.request.urlopen(req,timeout=35) as r:
        return r.read(),r.headers.get("Content-Type","")
def commons(query):
    params=urllib.parse.urlencode({"action":"query","generator":"search","gsrsearch":"filetype:bitmap "+query,"gsrnamespace":6,"gsrlimit":25,"prop":"imageinfo","iiprop":"url|size|extmetadata","iiurlwidth":1600,"format":"json"})
    data,_=get("https://commons.wikimedia.org/w/api.php?"+params)
    pages=json.loads(data).get("query",{}).get("pages",{})
    for page in sorted(pages.values(),key=lambda p:p.get("index",999)):
        info=(page.get("imageinfo") or [{}])[0]
        meta=info.get("extmetadata",{})
        license_name=meta.get("LicenseShortName",{}).get("value","")
        if not (license_name.startswith("CC BY") or license_name in ("CC0","Public domain")):continue
        if info.get("width",0)<900 or info.get("height",0)<500:continue
        url=info.get("thumburl") or info.get("url")
        if not url:continue
        try:
            content,mime=get(url)
            im=Image.open(BytesIO(content)).convert("RGB")
            if im.width<700:continue
            return im,{"source":info.get("descriptionurl",url),"title":page.get("title"),"license":license_name,"artist":meta.get("Artist",{}).get("value","")}
        except Exception as ex:print("Skipping candidate:",ex)
    raise RuntimeError("No suitable openly licensed photo found for "+query)

credits=[]
for name,query in SEARCHES.items():
    try:
        im,credit=commons(query)
        im.thumbnail((1800,1100),Image.Resampling.LANCZOS)
        dest=ASSETS/(name+".webp")
        im.save(dest,"WEBP",quality=82,method=6)
        credits.append({"file":dest.name,**credit})
        print("Saved",dest,im.size)
    except Exception as ex:
        print("FAILED",name,str(ex))
(ASSETS/"PHOTO_CREDITS.json").write_text(json.dumps(credits,indent=2)+"\n")
if len(credits)<4:raise SystemExit("Incomplete photography set; stylesheet left unchanged")
css=ROOT/"styles.css"
text=css.read_text()
start="/* Locally hosted illustrative photography: managed by scripts/localize_photos.py */"
block=start+"""
.hero{background-image:linear-gradient(90deg,rgba(3,17,37,.96) 0%,rgba(7,27,48,.83) 40%,rgba(7,28,50,.38) 68%,rgba(7,28,50,.72) 100%),url("assets/offshore-platform.webp")}
.service-visual-01{background-image:linear-gradient(0deg,rgba(5,28,51,.17),rgba(5,28,51,.17)),url("assets/exploration.webp")}
.service-visual-02{background-image:linear-gradient(120deg,rgba(6,29,53,.1),rgba(6,29,53,.36)),url("assets/asset-management.webp")}
.service-visual-04{background-image:linear-gradient(120deg,rgba(6,29,53,.12),rgba(6,29,53,.38)),url("assets/well-intervention.webp")}
"""
if start in text:text=text[:text.index(start)]
css.write_text(text.rstrip()+"\n\n"+block)
