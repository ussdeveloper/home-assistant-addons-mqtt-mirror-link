# Konfiguracja HACS Badge

Ten plik zawiera instrukcje dotyczące badge'y wyświetlanych w README.

## Badge'y w README.md

### HACS Badge
```markdown
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
```

### GitHub Release Badge
```markdown
[![GitHub Release](https://img.shields.io/github/release/ussdeveloper/home-assistant-addons-mqtt-mirror-link.svg)](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/releases)
```
*Pamiętaj zmienić `ussdeveloper` na swoją nazwę użytkownika!*

### License Badge
```markdown
[![License](https://img.shields.io/github/license/ussdeveloper/home-assistant-addons-mqtt-mirror-link.svg)](LICENSE)
```

### Validation Badge
```markdown
[![Validate](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/actions/workflows/validate.yml/badge.svg)](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/actions/workflows/validate.yml)
```

## Zmiana nazwy użytkownika w badge'ach

Jeśli Twoja nazwa użytkownika GitHub to np. `jankowalski`, zamień wszystkie wystąpienia:

```
ussdeveloper → jankowalski
```

W plikach:
- `README.md`
- `info.md`
- `publish.ps1`
- ten plik (`BADGES.md`)
