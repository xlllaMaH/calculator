#!/usr/bin/env bash
set -euo pipefail
umask 022

NAME="calculator"
VERSION="1.0"          # версия программы
REVISION="1"           # номер сборки пакета (аналог Release в rpm)
MAINTAINER="Shoma <g.artem1902@gmail.com>"
PYDIR="usr/lib/python3/dist-packages"
SRC_DIR="calculator"   # каталог модуля относительно корня репозитория

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"          # корень репозитория
FULL="${VERSION}-${REVISION}"
STAGE="$HERE/build/${NAME}_${FULL}_all"
OUT="$HERE/dist"
DEB="$OUT/${NAME}_${FULL}_all.deb"

rm -rf "$HERE/build" "$OUT" && mkdir -p "$STAGE" "$OUT"
cp -a "$HERE/pkg/." "$STAGE/"
rm -f "$STAGE/DEBIAN/control.in"

# код приложения: все *.py модуля, включая подпакеты, без __pycache__
install -d "$STAGE/$PYDIR/$NAME"
( cd "$ROOT/$SRC_DIR" && find . -name '*.py' -not -path '*/__pycache__/*' -print0 \
    | while IFS= read -r -d '' f; do
        install -D -m 644 "$f" "$STAGE/$PYDIR/$NAME/$f"
      done )

find "$STAGE/usr/share/man" -name '*.1' -exec gzip -9n {} \;
gzip -9n "$STAGE/usr/share/doc/$NAME/changelog.Debian"

find "$STAGE" -type d -exec chmod 755 {} +
find "$STAGE" -type f -exec chmod 644 {} +
chmod 755 "$STAGE/usr/bin/$NAME" "$STAGE/DEBIAN/postinst" "$STAGE/DEBIAN/prerm"

( cd "$STAGE" && find . -type f -not -path './DEBIAN/*' -printf '%P\0' \
    | sort -z | xargs -0 md5sum > DEBIAN/md5sums )
chmod 644 "$STAGE/DEBIAN/md5sums"

SIZE=$(du -sk --exclude=DEBIAN "$STAGE" | cut -f1)
sed -e "s|@NAME@|$NAME|" -e "s|@VERSION@|$FULL|" \
    -e "s|@SIZE@|$SIZE|" -e "s|@MAINTAINER@|$MAINTAINER|" \
    "$HERE/pkg/DEBIAN/control.in" > "$STAGE/DEBIAN/control"
chmod 644 "$STAGE/DEBIAN/control"

dpkg-deb --root-owner-group -Zxz --build "$STAGE" "$DEB"
echo "Готово: $DEB"
