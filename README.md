# Kairon Arcade · ห้องเกม ไครอน — portal site

Static GitHub Pages user site. Games themselves live in `songyisong88/teepuan-games` (served at `/teepuan-games/<slug>/`).

- Edit games / texts in `build.py`, then run `python3 build.py`.
- Custom domain later: `SITE_URL=https://example.com python3 build.py`, add a `CNAME` file. All internal links are root-relative.
- Ads: `assets/config.js` (`adTest`, `adClient`). No ad scripts are loaded yet. `ads.txt` has a commented placeholder only.
- Fonts: Kanit (SIL OFL, `assets/fonts/OFL-Kanit.txt`), self-hosted. No external CDNs or trackers.
