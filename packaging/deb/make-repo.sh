#!/usr/bin/env bash
set -euo pipefail
umask 022

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$HERE/repo"
SUITE="stable"; COMP="main"
ARCHS="amd64 arm64 armhf i386"      # пакет arch:all попадает во все индексы
export GNUPGHOME="$HERE/.gnupg"     # закрытый ключ — только здесь, в .gitignore
KEY_UID="Calculator Repo <g.artem1902@gmail.com>"
PKG_DIR_LETTER="c"                  # первая буква имени пакета
NAME="calculator"

shopt -s nullglob
debs=("$HERE"/dist/*.deb)
[ ${#debs[@]} -gt 0 ] || { echo "Сначала ./build.sh" >&2; exit 1; }

if [ ! -d "$GNUPGHOME" ]; then
    mkdir -m 700 "$GNUPGHOME"
    gpg --batch --pinentry-mode loopback --passphrase '' \
        --quick-generate-key "$KEY_UID" rsa3072 sign 5y >/dev/null 2>&1
fi

rm -rf "$REPO" && mkdir -p "$REPO/pool/$COMP/$PKG_DIR_LETTER/$NAME"
cp "${debs[@]}" "$REPO/pool/$COMP/$PKG_DIR_LETTER/$NAME/"

cd "$REPO"
for a in $ARCHS; do
    d="dists/$SUITE/$COMP/binary-$a"; mkdir -p "$d"
    dpkg-scanpackages --arch "$a" pool 2>/dev/null > "$d/Packages"
    gzip -9nk "$d/Packages"
done

rel="dists/$SUITE/Release"
{
    echo "Origin: $NAME"; echo "Label: $NAME"
    echo "Suite: $SUITE"; echo "Codename: $SUITE"
    echo "Date: $(LC_ALL=C date -Ru)"
    echo "Architectures: $ARCHS"; echo "Components: $COMP"
    echo "Description: $NAME apt repository"
    echo "SHA256:"
    ( cd "dists/$SUITE" && find "$COMP" -type f | sort | while read -r f; do
        printf ' %s %16d %s\n' "$(sha256sum "$f" | cut -d' ' -f1)" "$(stat -c %s "$f")" "$f"
      done )
} > "$rel"

gpg --batch --yes --pinentry-mode loopback --passphrase '' \
    --clearsign -o "dists/$SUITE/InRelease" "$rel"
gpg --batch --yes --pinentry-mode loopback --passphrase '' \
    --armor --detach-sign -o "dists/$SUITE/Release.gpg" "$rel"

gpg --export > "$REPO/$NAME-repo.gpg"          # для signed-by=
gpg --armor --export > "$REPO/$NAME-repo.asc"
echo "Репозиторий готов: $REPO"
