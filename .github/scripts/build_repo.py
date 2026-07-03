#!/usr/bin/env python3
"""Build the FENtastic Plus GitHub Pages site + Kodi repository.

Outputs everything into ./_site :

  _site/                     -> copy of ./docs (marketing landing page)
  _site/repo/addons.xml      -> Kodi repository index
  _site/repo/addons.xml.md5  -> checksum of addons.xml
  _site/repo/<id>/<id>-<ver>.zip  -> installable add-on zips (skin + repository)
  _site/repo/<id>/icon.png / fanart.jpg -> art for the Kodi repo browser

The Kodi add-on <version> values are read from each add-on's addon.xml, so the
skin version is single-sourced from the skin's addon.xml.
"""

import hashlib
import os
import shutil
import xml.etree.ElementTree as ET
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = os.path.join(ROOT, "_site")
REPO = os.path.join(SITE, "repo")

SKIN_ID = "skin.fentastic"
REPO_ID = "repository.fentastic"

# Top-level entries never shipped inside the skin zip.
SKIN_EXCLUDE_TOP = {
    ".git", ".github", ".gitignore", "docs", "_site",
    REPO_ID, "COPYING", "LICENSE-CC-BY-SA-4.0.txt",
}


def addon_version(addon_dir):
    xml_path = os.path.join(addon_dir, "addon.xml")
    return ET.parse(xml_path).getroot().get("version")


def zip_addon(addon_id, src_dir, exclude_top=None):
    """Zip src_dir into _site/repo/<addon_id>/<addon_id>-<ver>.zip.

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


def main():
    if os.path.isdir(SITE):
        shutil.rmtree(SITE)
    os.makedirs(REPO, exist_ok=True)

    # 1. Landing page: copy ./docs -> _site (so Pages root is the marketing page).
    docs = os.path.join(ROOT, "docs")
    if os.path.isdir(docs):
        for entry in os.listdir(docs):
            src = os.path.join(docs, entry)
            dst = os.path.join(SITE, entry)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
    # Disable Jekyll processing on Pages.
    open(os.path.join(SITE, ".nojekyll"), "w").close()

    # 2. Repository add-on needs an icon: reuse the skin icon.
    repo_dir = os.path.join(ROOT, REPO_ID)
    shutil.copy2(
        os.path.join(ROOT, "resources", "icon.png"),
        os.path.join(repo_dir, "icon.png"),
    )

    # 3. Package add-ons and copy their art into the repo tree.
    print("Packaging add-ons:")
    _, skin_out = zip_addon(SKIN_ID, ROOT, exclude_top=SKIN_EXCLUDE_TOP)
    copy_art(ROOT, skin_out)

    _, repo_out = zip_addon(REPO_ID, repo_dir)
    shutil.copy2(os.path.join(repo_dir, "icon.png"), os.path.join(repo_out, "icon.png"))

    # 4. Repository index.
    print("Building repository index:")
    write_addons_xml([ROOT, repo_dir])

    print("Done. Site is in ./_site")


if __name__ == "__main__":
    main()
