#!/usr/bin/env python3
"""Build the FENtastic Plus Kodi repository into ./docs/repo.

GitHub Pages for this repo serves the ./docs folder, so the Kodi repository is
generated straight into ./docs/repo and committed. Kodi then reads it from
https://jtcozart.github.io/fentastic-skin/repo/ :

  docs/repo/addons.xml          -> Kodi repository index
  docs/repo/addons.xml.md5      -> checksum of addons.xml
  docs/repo/<id>/<id>-<ver>.zip -> installable add-on zips (skin + repository)
  docs/repo/<id>/icon.png|fanart.jpg -> art for the Kodi repo browser
  docs/repo/index.html          -> friendly page for browser visitors

The skin <version> is single-sourced from skin.fentastic's addon.xml.
Run this before tagging a release, then commit ./docs/repo.
"""

import hashlib
import os
import shutil
import xml.etree.ElementTree as ET
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS = os.path.join(ROOT, "docs")
REPO = os.path.join(DOCS, "repo")

SKIN_ID = "skin.fentastic"
REPO_ID = "repository.fentastic"
HELPER_ID = "script.fentastic.helper"

# Top-level entries never shipped inside the skin zip.
SKIN_EXCLUDE_TOP = {
    ".git", ".github", ".gitignore", "docs",
    REPO_ID, HELPER_ID, "COPYING", "LICENSE-CC-BY-SA-4.0.txt",
}


def addon_version(addon_dir):
    xml_path = os.path.join(addon_dir, "addon.xml")
    return ET.parse(xml_path).getroot().get("version")


def zip_addon(addon_id, src_dir, exclude_top=None):
    """Zip src_dir into docs/repo/<addon_id>/<addon_id>-<ver>.zip.

    Everything is placed under a top-level <addon_id>/ folder, as Kodi requires.
    """
    exclude_top = exclude_top or set()
    version = addon_version(src_dir)
    out_dir = os.path.join(REPO, addon_id)
    os.makedirs(out_dir, exist_ok=True)
    zip_path = os.path.join(out_dir, f"{addon_id}-{version}.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for base, dirs, files in os.walk(src_dir):
            rel = os.path.relpath(base, src_dir)
            if rel == ".":
                dirs[:] = [d for d in sorted(dirs) if d not in exclude_top]
                files = [f for f in files if f not in exclude_top]
            for f in sorted(files):
                abs_path = os.path.join(base, f)
                rel_path = f if rel == "." else os.path.join(rel, f)
                z.write(abs_path, os.path.join(addon_id, rel_path))

    print(f"  built {os.path.relpath(zip_path, ROOT)}")
    return version, out_dir


def copy_art(addon_dir, out_dir):
    for name, src in (
        ("icon.png", os.path.join(addon_dir, "resources", "icon.png")),
        ("fanart.jpg", os.path.join(addon_dir, "resources", "fanart.jpg")),
    ):
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(out_dir, name))


def addon_block(addon_dir):
    """Return the <addon>...</addon> text of an add-on, without XML declaration."""
    with open(os.path.join(addon_dir, "addon.xml"), encoding="utf-8") as fh:
        text = fh.read()
    start = text.index("<addon")
    return text[start:].rstrip()


def write_addons_xml(addon_dirs):
    blocks = "\n".join(addon_block(d) for d in addon_dirs)
    content = '<?xml version="1.0" encoding="UTF-8"?>\n<addons>\n{}\n</addons>\n'.format(blocks)
    addons_path = os.path.join(REPO, "addons.xml")
    with open(addons_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
    digest = hashlib.md5(content.encode("utf-8")).hexdigest()
    with open(addons_path + ".md5", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(digest)
    print(f"  wrote addons.xml ({len(content)} bytes) md5={digest}")


def write_repo_index():
    """Friendly page for humans visiting /repo/ (Kodi uses addons.xml directly)."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>FENtastic Plus - Kodi Repository</title>
<style>
  body { font-family: -apple-system, Segoe UI, Roboto, sans-serif; background:#0d1117;
    color:#e6edf3; max-width:720px; margin:60px auto; padding:0 20px; line-height:1.6; }
  a { color:#17b2e7; } code { background:#010409; border:1px solid #21262d;
    border-radius:6px; padding:2px 7px; }
  .box { background:#161b22; border:1px solid #21262d; border-radius:10px; padding:16px 20px; }
</style>
</head>
<body>
  <h1>FENtastic Plus - Kodi Repository</h1>
  <p>This is the add-on repository Kodi uses to install and auto-update the
     FENtastic Plus skin. Add it in Kodi via <strong>Settings &rarr; File manager
     &rarr; Add source</strong> with this URL:</p>
  <p class="box"><code>https://jtcozart.github.io/fentastic-skin/repo/</code></p>
  <p>Full instructions are on the <a href="../">project page</a>. Repository index:
     <a href="addons.xml">addons.xml</a> (<a href="addons.xml.md5">md5</a>).</p>
</body>
</html>
"""
    with open(os.path.join(REPO, "index.html"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)


def main():
    # Rebuild docs/repo from scratch so stale versions don't linger.
    if os.path.isdir(REPO):
        shutil.rmtree(REPO)
    os.makedirs(REPO, exist_ok=True)

    # GitHub Pages (branch /docs) runs Jekyll by default; disable it so nothing
    # in docs/ gets mangled or skipped.
    open(os.path.join(DOCS, ".nojekyll"), "w").close()

    # The repository add-on needs an icon: reuse the skin icon.
    repo_dir = os.path.join(ROOT, REPO_ID)
    shutil.copy2(
        os.path.join(ROOT, "resources", "icon.png"),
        os.path.join(repo_dir, "icon.png"),
    )

    print("Packaging add-ons:")
    _, skin_out = zip_addon(SKIN_ID, ROOT, exclude_top=SKIN_EXCLUDE_TOP)
    copy_art(ROOT, skin_out)

    _, repo_out = zip_addon(REPO_ID, repo_dir)
    shutil.copy2(os.path.join(repo_dir, "icon.png"), os.path.join(repo_out, "icon.png"))

    helper_dir = os.path.join(ROOT, HELPER_ID)
    _, helper_out = zip_addon(HELPER_ID, helper_dir)
    copy_art(helper_dir, helper_out)

    print("Building repository index:")
    write_addons_xml([ROOT, repo_dir, helper_dir])
    write_repo_index()

    print("Done. Kodi repository is in ./docs/repo")


if __name__ == "__main__":
    main()
