# Установочный пакет calculator (.deb) и apt-репозиторий

Пакет для Debian/Ubuntu. Архитектура `all` (чистый Python 3 + Tk),
зависимости: `python3 (>= 3.9)`, `python3-tk`.

## Установка

### а) из файла

```bash
sudo apt install ./dist/calculator_1.0-1_all.deb
calculator
```

### б) через apt-репозиторий

```bash
sudo mkdir -p /etc/apt/keyrings
sudo cp repo/calculator-repo.gpg /etc/apt/keyrings/calculator.gpg
echo "deb [signed-by=/etc/apt/keyrings/calculator.gpg] file:/путь/к/repo stable main" \
  | sudo tee /etc/apt/sources.list.d/calculator.list
sudo apt update && sudo apt install calculator
```

Репозиторий можно раздать по сети:

```bash
cd repo && python3 -m http.server 8000
# на клиенте: deb [signed-by=...] http://<адрес>:8000 stable main
```

Удаление: `sudo apt remove calculator`.

## Сборка с нуля

Нужны `dpkg-dev`, `gnupg`, `gzip` (для проверок ещё `lintian`).

```bash
cd packaging/deb
./build.sh        # -> dist/calculator_1.0-1_all.deb
./make-repo.sh    # -> repo/ (подписанный репозиторий)
```

`build.sh` копирует код из `calculator/` репозитория (все `*.py`, включая
подпакеты `operations/` и `ui/`, без `__pycache__`), поэтому код в `pkg/` не
дублируется. Скрипты нужно запускать на Linux (в WSL — из домашнего каталога
WSL, а не из `/mnt/c`: на диске Windows не сохраняются права файлов).

> **Важно.** Закрытый ключ создаётся при первом запуске `make-repo.sh` в
> `.gnupg/` (он в `.gitignore`, не коммитить!). Если пересобрать репозиторий
> на другой машине, ключ будет новым, и клиентам понадобится новый `.gpg`.

## Структура

```
packaging/deb/
├── pkg/                         файловая система пакета
│   ├── DEBIAN/{control.in,postinst,prerm}
│   └── usr/
│       ├── bin/calculator                         лаунчер
│       └── share/
│           ├── applications/calculator.desktop    пункт меню
│           ├── icons/hicolor/scalable/apps/calculator.svg
│           ├── man/man1/calculator.1, man/ru/man1/calculator.1
│           └── doc/calculator/{copyright,changelog.Debian}
├── build.sh                     сборка .deb
├── make-repo.sh                 сборка и подпись репозитория
├── dist/ build/ repo/ .gnupg/   результаты сборки (в .gitignore)
└── README.md
```

Модуль устанавливается в `/usr/lib/python3/dist-packages/calculator/`.

## Соответствие rpm ↔ deb

| rpm (`.spec`)                | deb                                          |
|------------------------------|----------------------------------------------|
| `Name`, `Version`, `Release` | `Package`, `Version: 1.0-1`                  |
| `Summary`, `%description`    | `Description`                                |
| `License`                    | `usr/share/doc/calculator/copyright`         |
| `Group`                      | `Section`                                    |
| `Requires`                   | `Depends`                                    |
| `BuildArch: noarch`          | `Architecture: all`                          |
| `%install` + `%files`        | дерево `pkg/`                                |
| `%post` / `%preun`           | `DEBIAN/postinst` / `DEBIAN/prerm`           |
| `%changelog`                 | `changelog.Debian.gz`                        |
| `rpmbuild -ba`               | `dpkg-deb --build`                           |

## Проверка

```bash
dpkg-deb -I dist/calculator_1.0-1_all.deb   # метаданные
dpkg-deb -c dist/calculator_1.0-1_all.deb   # содержимое
dpkg -L calculator                          # файлы установленного пакета
apt-cache policy calculator                 # версия и источник
lintian dist/*.deb
```

`lintian` выдаёт одно предупреждение `initial-upload-closes-no-bugs`: оно
относится к загрузке в архив Debian (нужен номер ITP-бага) и для
собственного репозитория неактуально.

В минимальных образах (контейнеры, CI) dpkg может исключать
`/usr/share/man` и `/usr/share/doc`, тогда `dpkg --verify` покажет `missing`
для man-страниц — это не ошибка пакета.
