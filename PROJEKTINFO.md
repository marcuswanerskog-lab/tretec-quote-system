# Tretec Quote System - Projektöversikt

## Projektstruktur

```
tretec-quote-system/
├── scripts/
│   └── server.py          # Flask-server med API och PDF-generering
├── templates/
│   ├── index.html         # Webbgränssnitt
│   ├── agreement_terms.py # Avtalsvillkor och mallar
│   └── README_AGREEMENT_TERMS.md  # Guide för anpassning av avtal
├── static/
│   └── Treteclogo.jpg     # Företagslogga
├── requirements.txt       # Python-beroenden
├── .gitignore            # Git-ignoreringar
├── PROJEKTINFO.md        # Teknisk dokumentation (denna fil)
└── README.md             # Huvuddokumentation
```

## Nyckelfunktioner

### Backend (server.py)
- **Flask-applikation** med CORS-stöd
- **Produktdatabas** med tre kategorier (larm, kamera, ellås)
- **Tjänstedatabas** med timbaserade priser
- **PDF-generering** för både offerter och affärsavtal
- **Webbskrapning** av ellås-produkter (med felhantering)
- **API-endpoints**:
  - `GET /api/products` - Hämta produkter (med sök och filter)
  - `GET /api/services` - Hämta tjänster
  - `POST /api/generate-pdf` - Generera PDF
- **Felhantering**:
  - HTTP 404, 500 och generella fel
  - Omfattande loggning
  - Graceful degradation vid webbskrapningsfel

### Frontend (index.html)
- **Flikanvändargränssnitt** för offerter och affärsavtal
- **Produktsökning** och kategorifiltrering
- **Varukorg** med rabattsystem
- **Dynamisk prisberäkning**
- **Responsiv design** med moderna CSS-gradients
- **Felmeddelanden** med automatisk timeout

## PDF-generering

### Offert-PDF
- Företagsinformation (header)
- Kundinformation
- Produkter/tjänster i tabellformat
- Rabatter per artikel
- Totalsumma med moms
- Villkor (giltighet, betalning)

### Affärsavtal-PDF
- **Multi-sida professionellt dokument** (4 sidor)
- **Fullständiga juridiska villkor** med 11 paragrafer
- **Anpassningsbara fält**:
  - Kundinformation (namn, företag, telefon, email)
  - Avtalsnummer (auto-genererat eller manuellt)
  - Avtalsperiod (12/24/36 månader med automatiska datum)
  - Installationsdatum
  - Betalningsplan (5 fördefinierade alternativ):
    - 100% vid leverans
    - 50/50 förskott/installation
    - 30/70 förskott/installation  
    - 3 delbetalningar
    - 4 delbetalningar
  - Garantiperiod (24/36/60 månader)
  - Supportnivå (Bas/Standard/Premium)
  - Särskilda villkor (fritext)
- **Automatisk beräkning**:
  - Totalsumma exkl. moms
  - Moms (25%)
  - Totalt inkl. moms
  - Avtalsdatum (start/slut)
- **Avtalsstruktur**:
  - Sida 1: Försättssida, parter, omfattning
  - Sida 2: Specifikation, priser, leverans, betalning
  - Sida 3: Avtalstid, garanti, support
  - Sida 4: Övriga villkor, signaturer
- **Signatursektion** för båda parter med datum

### Avtalsmall (agreement_terms.py)
- Separerat innehåll från kod för enkel anpassning
- Fullständiga svenska avtalsvillkor
- Dynamiska fält för automatisk ifyllning
- Se `templates/README_AGREEMENT_TERMS.md` för anpassningsguide

## Säkerhet

### Implementerade åtgärder
- ✅ Flask debug-läge avstängt som standard
- ✅ Felhantering som inte läcker känslig information
- ✅ Loggning av alla fel och varningar
- ✅ CORS korrekt konfigurerad

### Rekommendationer för produktion
- [ ] Implementera autentisering (OAuth2, JWT)
- [ ] Använd HTTPS med giltiga certifikat
- [ ] Konfigurera rate limiting
- [ ] Använd produktions-WSGI-server (gunicorn, uWSGI)
- [ ] Implementera sessionshantering
- [ ] Lägg till datavalidering på serversidan
- [ ] Konfigurera loggning till fil i stället för stdout

## Anpassning

### Uppdatera företagsinformation
Redigera `COMPANY_INFO` i `scripts/server.py`:
```python
COMPANY_INFO = {
    'name': 'Ditt Företag AB',
    'address': 'Din Adress',
    'postal': 'Postnummer Ort',
    'phone': 'Telefonnummer',
    'email': 'info@dittforetag.se',
    'org_nr': 'Organisationsnummer',
}
```

### Lägga till produkter
Redigera `PRODUCTS` i `scripts/server.py`:
```python
PRODUCTS = {
    'din_kategori': [
        {'id': X, 'name': 'Produktnamn', 'price': XXXX, 'category': 'din_kategori'},
    ]
}
```

### Lägga till tjänster
Redigera `SERVICES` i `scripts/server.py`:
```python
SERVICES = [
    {'id': X, 'name': 'Tjänst', 'hourly_rate': XXX, 'estimated_hours': X},
]
```

### Lägga till logotyp
1. Placera logotyp som `static/logo.png`
2. Uppdatera PDF-funktionerna för att inkludera logotypen:
```python
c.drawImage('static/logo.png', x*mm, y*mm, width=30*mm, height=15*mm)
```

## Testning

### Manuell testning
1. Starta servern: `cd scripts && python server.py`
2. Öppna webbläsare: `http://localhost:5000`
3. Testa funktioner:
   - Sök och filtrera produkter
   - Lägg till i varukorg
   - Justera antal och rabatt
   - Generera offert-PDF
   - Byt till affärsavtal-flik
   - Generera affärsavtal-PDF

### API-testning
```bash
# Hämta produkter
curl http://localhost:5000/api/products

# Hämta tjänster
curl http://localhost:5000/api/services

# Generera PDF
curl -X POST http://localhost:5000/api/generate-pdf \
  -H "Content-Type: application/json" \
  -d '{"type":"quote","customer":{"name":"Test"},"items":[]}'
```

## Felsökning

### Servern startar inte
- Kontrollera att port 5000 är ledig: `lsof -i :5000`
- Verifiera Python-version: `python --version` (behöver 3.8+)
- Installera om dependencies: `pip install -r requirements.txt`

### PDF genereras inte
- Kolla serverloggar för felmeddelanden
- Verifiera att ReportLab är installerat: `pip show reportlab`
- Testa med minimal data först

### Ellås-produkter saknas
- Detta är normalt om webbskrapning misslyckas
- Systemet fortsätter fungera med larm- och kameraprodukter
- Kontrollera internetanslutning och serverloggar

## Framtida förbättringar

### Möjliga funktioner att lägga till
- [ ] Databas för att spara offerter och avtal
- [ ] Autentisering och användarhantering
- [ ] E-postsändning av PDF-filer
- [ ] Offerthistorik och statusuppföljning
- [ ] Kundregister
- [ ] Mallar för olika typer av avtal
- [ ] Stöd för flera språk
- [ ] Export till Excel/CSV
- [ ] Anpassningsbara PDF-mallar

### Tekniska förbättringar
- [ ] Flytta från JSON till SQLite/PostgreSQL
- [ ] Implementera caching för webbskrapning
- [ ] Lägg till enhetstester
- [ ] CI/CD-pipeline
- [ ] Docker-containerisering
- [ ] API-dokumentation med Swagger/OpenAPI

## Support och underhåll

### Vanliga underhållsuppgifter
- Uppdatera dependencies: `pip install --upgrade -r requirements.txt`
- Kontrollera säkerhetsuppdateringar: `pip list --outdated`
- Granska loggar regelbundet
- Backup av produktdata om modifierad

### Kontakt
- GitHub Issues: https://github.com/marcuswanerskog-lab/tretec-quote-system/issues
- Email: info@treteclarm.se

---
Senast uppdaterad: 2026-01-13
Version: 3.0
