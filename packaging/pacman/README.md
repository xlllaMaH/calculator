# Установочный пакет pacman (Arch Linux)

Сборка установочного пакета `calculator` для менеджера пакетов **pacman** с помощью `makepkg`.

## Состав

| Файл | Назначение |
|------|------------|
| `PKGBUILD` | Скрипт сборки: метаданные пакета, источники, правила установки файлов |
| `calculator-1.0.tar.gz` | Архив исходников (Source0), на который ссылается PKGBUILD |
| `calculator.desktop` | Пункт меню приложений (Desktop Entry) |
| `calculator.svg` | Иконка приложения |

## Сборка

```bash
cd packaging/pacman
makepkg -f          # -f пересобрать, даже если пакет уже есть
```

Результат: `calculator-1.0-1-any.pkg.tar.zst`.

Промежуточные каталоги `src/` и `pkg/` и готовый `.pkg.tar.zst` в git не коммитятся (см. `.gitignore`).

## Проверка без установки

```bash
pacman -Qip calculator-1.0-1-any.pkg.tar.zst   # метаданные пакета
pacman -Qlp calculator-1.0-1-any.pkg.tar.zst   # список файлов пакета
```

## Установка и удаление

```bash
sudo pacman -U calculator-1.0-1-any.pkg.tar.zst   # установка
calculator                                        # запуск
sudo pacman -Rns calculator                       # удаление пакета
```
