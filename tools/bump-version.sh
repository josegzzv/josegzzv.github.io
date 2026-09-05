#!/usr/bin/env bash
# Cache-busting: stamps a fresh ?v= on custom.css and i18n.js. Run before each commit that touches them.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
V=$(date +%Y%m%d%H%M)
sed -i.bak -E "s#(styles/custom\.css)(\?v=[0-9]+)?\"#\1?v=$V\"#; s#(js/i18n\.js)(\?v=[0-9]+)?\"#\1?v=$V\"#" index.html && rm -f index.html.bak
grep -n 'custom.css\|i18n.js' index.html
