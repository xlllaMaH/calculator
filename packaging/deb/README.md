# Калькулятор: deb-пакет и apt-репозиторий

Пакет для Debian/Ubuntu, архитектура `all`. Зависимости: `python3 (>= 3.9)`, `python3-tk`.

## Установка

Готовый пакет лежит в `installing-package/` в корне репозитория:

```bash
sudo apt install ./installing-package/calculator_1.0-1_all.deb
calculator            # или пункт «Калькулятор» в меню
```

Удаление: `sudo apt remove calculator`.

### Через apt-репозиторий

Сначала соберите его (см. «Сборка»), в git он не хранится.

```bash
sudo mkdir -p /etc/apt/keyrings
sudo cp packaging/deb/repo/calculator-repo.gpg /etc/apt/keyrings/calculator.gpg
echo "deb [signed-by=/etc/apt/keyrings/calculator.gpg] file:$PWD/packaging/deb/repo stable main" \
  | sudo tee /etc/apt/sources.list.d/calculator.list
sudo apt update && sudo apt install calculator
```

Для раздачи по сети: `cd packaging/deb/repo && python3 -m http.server 8000`,
на клиенте вместо `file:...` указать `http://<адрес>:8000`.

## Сборка

Нужен Linux с `dpkg-dev` и `gnupg` (в WSL запускать из домашнего каталога, не из `/mnt/c`).

```bash
cd packaging/deb
./build.sh        # -> dist/calculator_1.0-1_all.deb
./make-repo.sh    # -> repo/ (подписанный репозиторий)
```

`dist/`, `build/`, `repo/` и закрытый ключ `.gnupg/` в git не попадают.
При пересборке репозитория на другой машине ключ создаётся заново, клиентам нужен новый `.gpg`.

## Устройство

- `pkg/` — дерево пакета: `DEBIAN/` (метаданные, `postinst`, `prerm`), лаунчер `usr/bin/calculator`, меню, иконка, man-страницы (en/ru), copyright, changelog.
- Код берётся из `calculator/` при сборке и ставится в `/usr/lib/python3/dist-packages/calculator/`.

| rpm (`.spec`)                | deb                                |
|------------------------------|------------------------------------|
| `Name`, `Version`, `Release` | `Package`, `Version: 1.0-1`        |
| `Summary`, `%description`    | `Description`                      |
| `License`                    | `usr/share/doc/calculator/copyright` |
| `Group`                      | `Section`                          |
| `Requires`                   | `Depends`                          |
| `BuildArch: noarch`          | `Architecture: all`                |
| `%install` + `%files`        | дерево `pkg/`                      |
| `%post` / `%preun`           | `DEBIAN/postinst` / `prerm`        |
| `%changelog`                 | `changelog.Debian.gz`              |
| `rpmbuild -ba`               | `dpkg-deb --build`                 |

## Проверка

```bash
dpkg-deb -I installing-package/*.deb    # метаданные
dpkg-deb -c installing-package/*.deb    # содержимое
dpkg -L calculator                      # файлы установленного пакета
apt-cache policy calculator             # версия и источник
lintian installing-package/*.deb        # одно W: initial-upload-closes-no-bugs — норма
```
