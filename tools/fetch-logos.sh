#!/usr/bin/env bash
# Downloads institution logos from Wikimedia Commons into assets/img/logos/
# (Commons renders SVGs to PNG at the requested width; PNG/JPG are just resized).
# Run from anywhere:  bash tools/fetch-logos.sh
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$REPO_DIR/assets/img/logos"
mkdir -p "$OUT"

# Wikimedia requires a descriptive User-Agent, otherwise it returns 403.
UA="josegzzv.github.io logo fetch (https://josegzzv.github.io; josegzzv@msn.com)"
WIDTH=400

# name|Commons file title (verified to exist on 2026-09-05)
LOGOS=(
  "ut-mccombs|McCombs_School_of_Business_logo.svg"
  "mit|Massachusetts_Institute_of_Technology_logo.svg"
  "tec|Logo_del_ITESM.svg"
  "tecmilenio|Logo_Tecmilenio_2014.png"
  "ur|Universidad_Regiomontana.png"
  "egade|EGADE_Business_School_logo.JPG"   # large JPG on Commons; check quality, replace from brandcenter.tec.mx if needed
)

for entry in "${LOGOS[@]}"; do
  name="${entry%%|*}"
  file="${entry##*|}"
  url="https://commons.wikimedia.org/wiki/Special:FilePath/${file}?width=${WIDTH}"
  printf '%-12s <- %s\n' "$name" "$file"
  curl -fsSL -A "$UA" -o "$OUT/$name.png" "$url"
done

echo
echo "Not available on Wikimedia Commons (download manually and save with these names):"
echo "  $OUT/management30.png  ->  https://management30.com  (press / media kit)"
echo "  $OUT/iafci.png         ->  https://www.iafci.org"
echo
echo "Done. Files in $OUT:"
ls -la "$OUT"
