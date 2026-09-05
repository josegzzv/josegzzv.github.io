# josegzzv.github.io

Personal presentation page of **José Antonio González Villalón** — CIO / Senior IT Director.
Live at <a href="https://josegzzv.github.io" target="_blank">josegzzv.github.io</a>.

## Structure

| Path | Purpose |
|------|---------|
| `index.html` | Single-page site (hero, profile, expertise, career, education, lab, contact) |
| `styles/style.css` | DevFolio template styles (unmodified) |
| `styles/custom.css` | Site customizations: language toggle, chips, timeline, education list |
| `js/main.js` | DevFolio template behaviour (unmodified) |
| `js/i18n.js` | EN/ES toggle (`data-en` / `data-es` attributes and `.lang-en` / `.lang-es` blocks) and hero typed titles |
| `assets/` | Images and vendor libraries (Bootstrap, Bootstrap Icons, GLightbox, Swiper, Typed.js, PureCounter) |

## Editing content

- Short strings: edit both `data-en` and `data-es` on elements with class `t`.
- Paragraphs: edit the paired `.lang-en` / `.lang-es` blocks.
- Hero rotating titles: `data-typed-en` / `data-typed-es` on `.typed-exec` (comma-separated).
- Language is auto-detected from the browser and remembered in `localStorage` (`jagv.lang`).

## Credits

Built on the DevFolio template.

Template Name: DevFolio<br>
Template URL: https://bootstrapmade.com/devfolio-bootstrap-portfolio-html-template/<br>
Author: BootstrapMade.com<br>
License: https://bootstrapmade.com/license/
