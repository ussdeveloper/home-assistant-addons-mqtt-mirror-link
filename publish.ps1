# Skrypt automatycznej publikacji do GitHub
# Użycie: .\publish.ps1

Write-Host "🚀 MQTT Mirror Link - Publikacja na GitHub" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Sprawdź czy git jest zainstalowany
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git nie jest zainstalowany!" -ForegroundColor Red
    Write-Host "Pobierz z: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Sprawdź czy jesteśmy w katalogu projektu
if (-not (Test-Path "custom_components\mqtt_link\manifest.json")) {
    Write-Host "❌ Nie znaleziono plików projektu!" -ForegroundColor Red
    Write-Host "Uruchom ten skrypt z katalogu projektu." -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Git jest zainstalowany" -ForegroundColor Green
Write-Host ""

# Pytaj o nazwę użytkownika GitHub
Write-Host "📝 Podaj swoją nazwę użytkownika GitHub:" -ForegroundColor Yellow
$githubUser = Read-Host

if ([string]::IsNullOrWhiteSpace($githubUser)) {
    Write-Host "❌ Nazwa użytkownika jest wymagana!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔧 Inicjalizacja repozytorium Git..." -ForegroundColor Cyan

# Inicjalizuj git jeśli nie istnieje
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✅ Git zainicjalizowany" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Git już zainicjalizowany" -ForegroundColor Gray
}

# Dodaj wszystkie pliki
Write-Host ""
Write-Host "📦 Dodawanie plików..." -ForegroundColor Cyan
git add .

# Commit
Write-Host ""
Write-Host "💾 Tworzenie commitu..." -ForegroundColor Cyan
git commit -m "Initial commit: MQTT Mirror Link v1.0.0

- Synchronizacja dwukierunkowa MQTT
- Konfiguracja przez UI Home Assistant
- Filtrowanie tematów
- Uwierzytelnianie MQTT
- Dokumentacja PL/EN"

# Ustaw gałąź main
Write-Host ""
Write-Host "🌿 Ustawianie gałęzi main..." -ForegroundColor Cyan
git branch -M main

# Sprawdź czy remote już istnieje
$remoteExists = git remote | Select-String -Pattern "origin" -Quiet

if (-not $remoteExists) {
    # Dodaj remote
    Write-Host ""
    Write-Host "🔗 Dodawanie zdalnego repozytorium..." -ForegroundColor Cyan
    $repoUrl = "https://github.com/$githubUser/home-assistant-addons-mqtt-mirror-link.git"
    git remote add origin $repoUrl
    Write-Host "✅ Remote dodany: $repoUrl" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "ℹ️  Remote 'origin' już istnieje" -ForegroundColor Gray
}

# Wypchnij
Write-Host ""
Write-Host "🚀 Wypychanie do GitHub..." -ForegroundColor Cyan
Write-Host "⚠️  Jeśli to pierwsze wypychanie, będziesz musiał się zalogować do GitHub" -ForegroundColor Yellow
Write-Host ""

$pushResult = git push -u origin main 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Kod został wypchnięty na GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Następne kroki:" -ForegroundColor Cyan
    Write-Host "1. Przejdź do: https://github.com/$githubUser/home-assistant-addons-mqtt-mirror-link" -ForegroundColor White
    Write-Host "2. Utwórz Release (v1.0.0)" -ForegroundColor White
    Write-Host "3. Dodaj repozytorium do HACS w Home Assistant" -ForegroundColor White
    Write-Host ""
    Write-Host "📖 Szczegóły w pliku: PUBLICATION_GUIDE.md" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "❌ Błąd podczas wypychania!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Możliwe przyczyny:" -ForegroundColor Yellow
    Write-Host "- Repozytorium nie istnieje na GitHub (utwórz je najpierw)" -ForegroundColor White
    Write-Host "- Brak uprawnień (sprawdź login)" -ForegroundColor White
    Write-Host "- Repozytorium nie jest puste (usuń README/LICENSE przy tworzeniu)" -ForegroundColor White
    Write-Host ""
    Write-Host "Błąd:" -ForegroundColor Red
    Write-Host $pushResult -ForegroundColor Gray
}

Write-Host ""
Write-Host "Naciśnij Enter aby zakończyć..."
Read-Host
