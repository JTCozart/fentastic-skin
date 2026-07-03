# FENtastic Plus (Kodi Skin)

[![AI Honesty](https://img.shields.io/badge/AI%20honesty-Claude--assisted-8A2BE2?logo=anthropic&logoColor=white)](#ai-transparency)
[![License](https://img.shields.io/badge/license-CC%20BY--SA%204.0%20%2B%20GPL%20v2-blue.svg)](LICENSE.txt)
[![Kodi](https://img.shields.io/badge/Kodi-Omega%20(21%2B)-17B2E7?logo=kodi&logoColor=white)](https://kodi.tv)
[![Release](https://img.shields.io/github/v/release/JTCozart/fentastic-skin?label=release)](https://github.com/JTCozart/fentastic-skin/releases/latest)

FENtastic Plus is a modern, customizable Kodi skin — a modded version of the default **Estuary** skin. This repository is a **fork** maintained by [JTCozart](https://github.com/JTCozart), continuing the work of the original authors with ongoing UI/UX improvements and a proper release + auto-update pipeline.

> This is a community fork. It is **not** affiliated with or endorsed by the original authors. See [Credits & Attribution](#credits--attribution).

- **Landing page & install guide:** https://jtcozart.github.io/fentastic-skin/
- **Downloads:** [Releases](https://github.com/JTCozart/fentastic-skin/releases/latest)
- **Issues / requests:** [GitHub Issues](https://github.com/JTCozart/fentastic-skin/issues)

---

## Features

- Modern, redesigned UI experience
- Extra viewtypes ("WideWall" and "WideInfoWall") plus adjustments to the built-in views
- Customizable movie and show main-menu items
- Customizable widgets and category widgets for movies, tvshows, and episodes
- Custom stacked widgets for movies, tvshows, and episodes
- Ratings displayed for movies, tvshows, seasons, and episodes
- InfoPanel for widgets, with optional ratings
- Custom multi-category search window (incl. Trakt lists)
- Watched/unwatched progress shown for movies, tvshows, seasons, and episodes

Designed for use with the FEN family of add-ons (Fen Light, Red Light, The Gears, Umbrella, POV, TMDbH).

---

## Installation

### Option A — Repository (recommended, enables auto-updates)

Installing the repository add-on lets Kodi keep the skin up to date automatically.

1. In Kodi: **Settings → File manager → Add source**, and enter:

   ```
   https://jtcozart.github.io/fentastic-skin/repo/
   ```

   Give it a name such as `FENtastic Plus`.
2. **Settings → Add-ons → Install from zip file →** `FENtastic Plus` → `repository.fentastic` → `repository.fentastic-x.x.x.zip`.
3. **Install from repository → FENtastic Plus Repository → Look and feel → Skin → FENtastic Plus → Install.**

Kodi will now auto-update the skin whenever a new version is published.

### Option B — Direct zip (manual, no auto-updates)

1. Download the latest `skin.fentastic-x.x.x.zip` from the [Releases page](https://github.com/JTCozart/fentastic-skin/releases/latest).
2. In Kodi: **Settings → Add-ons → Install from zip file** and select the downloaded file.

> If Kodi blocks the install, enable **Settings → System → Add-ons → Unknown sources**.

---

## Setup Guide

On first install the home screen is intentionally empty — the Movie and Show sections are hidden until you assign menu paths.

1. **Settings → Interface → Skin → Configure skin… → Main menu items.**
2. Toggle a section (e.g. Movies/Shows) on. Note: a section stays hidden until you set its **main menu path**.
3. Click **Set main menu path** and choose any path within FEN (for example your Trakt collection).
4. Click **Set widgets** to configure up to 10 movie and 10 TV-show widgets. Each widget can have a label and display type (Poster, Landscape, LandscapeInfo, Category). Category widgets can be set up as stacked widgets.
5. To rearrange, rename, remake, change display type, or remove a widget, click it and pick from the pop-up options. You can reconfigure as often as you like.

A condensed version of this guide is also available in-skin under **Configure skin… → Extra info → Setup Guide**.

---

## Building / Releasing (maintainers)

Releases are fully automated via GitHub Actions (`.github/workflows/release.yml`):

1. Bump `version` in [`addon.xml`](addon.xml) (and add a `changelog.txt` entry).
2. Commit, then tag and push:

   ```bash
   git tag v$(grep -oP 'version="\K[^"]+' addon.xml | head -1)
   git push origin --tags
   ```

3. The workflow packages the skin, (re)builds the Kodi repository index (`addons.xml` + `.md5`), attaches the zips to a GitHub Release, and deploys the landing page + repo to GitHub Pages.

**One-time setup:** in the repo settings, set **Pages → Source → GitHub Actions**.

---

## AI Transparency

In the spirit of honest disclosure: parts of this fork — tooling, docs, the release pipeline, and some UI/UX changes — were developed with the assistance of an AI coding assistant ([Claude](https://www.anthropic.com/claude-code)). All changes are human-reviewed before release. This badge is here so users and contributors know exactly how the work was made.

---

## Credits & Attribution

- **Original skin:** FENtastic / FENtastic Plus by **Ivar Brandt** and **Zaxxon709** (an Estuary MOD).
- **Based on:** the default **Estuary** skin by Team Kodi.
- **This fork:** maintained by **JTCozart**.

Attribution is required by the license and is retained here and in [`addon.xml`](addon.xml).

## License

- **Artwork:** Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)
- **Code:** GNU General Public License, Version 2.0 (GPL-2.0)

See [`LICENSE.txt`](LICENSE.txt) for details.
