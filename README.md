# Tretec Quote System

Ett professionellt offertsystem för Tretec Larm AB, byggt med Python och Flask.

## Funktioner
- **Produkthantering** - Sök och filtrera produkter i kategorier (larm, kamera, ellås)
- **PDF-generering** - Skapa både offerter och omfattande affärsavtal med juridiska villkor
- **Affärsavtal** - Professionella avtal med 11 paragrafer, betalningsplaner, garantier och support
- **Ellås-produkter** - Automatisk skrapning från Låsgiganten (med felhantering)
- **Rabattsystem** - Rabatter per produkt och kund
- **Tjänstehantering** - Timbaserade beräkningar för installation och service
- **Responsivt gränssnitt** - Flikanvändargränssnitt för offerter och affärsavtal
- **Robust felhantering** - HTTP-felhantering (404, 500) med loggning
- **Anpassningsbara avtalsvillkor** - Enkelt redigerbara mallar i `templates/agreement_terms.py`

## Projektstruktur
```
tretec-quote-system/
├── scripts/
│   └── server.py          # Flask-server med API och PDF-generering
├── templates/
│   └── index.html         # Webbgränssnitt
├── static/
│   └── Treteclogo.jpg     # Företagslogga
├── requirements.txt       # Python-beroenden
├── PROJEKTINFO.md         # Teknisk dokumentation
├── .gitignore            # Git-ignoreringar
└── README.md             # Denna fil
```

## Installation

### Förutsättningar
- Python 3.8 eller senare
- pip (Python package manager)

### Steg-för-steg
1. **Klona repositoryt**
   ```bash
   git clone https://github.com/marcuswanerskog-lab/tretec-quote-system.git
   cd tretec-quote-system
   ```

2. **Installera beroenden**
   ```bash
   pip install -r requirements.txt
   ```
   
   Eller manuellt:
   ```bash
   pip install flask flask-cors reportlab requests beautifulsoup4
   ```

3. **Starta servern**
   ```bash
   cd scripts
   python server.py
   ```

4. **Öppna i webbläsare**
   - Navigera till: http://localhost:5000
   - Servern körs på alla nätverksgränssnitt (0.0.0.0:5000)

## Användning

### Skapa en offert
1. Gå till fliken "Ny Offert"
2. Fyll i kundinformation (namn, företag, email)
3. Sök och lägg till produkter/tjänster i varukorgen
4. Ange kvantitet och eventuell rabatt per artikel
5. Klicka på "Generera PDF" för att skapa offerten

### Skapa ett affärsavtal
1. Gå till fliken "Nytt Affärsavtal"
2. Fyll i kundinformation (namn, företag, email, telefon)
3. Välj avtalsdetaljer:
   - Avtalsperiod (12, 24 eller 36 månader)
   - Planerat installationsdatum
   - Betalningsplan (5 alternativ från förskott till delbetalningar)
   - Garantiperiod (Standard 24, Utökad 36, Premium 60 månader)
   - Supportnivå (Bas, Standard eller Premium)
   - Särskilda villkor (valfri fritext)
4. Lägg till produkter/tjänster från katalogen
5. Klicka på "Generera Affärsavtal (PDF)" för att skapa ett komplett juridiskt dokument

**Avtalet innehåller:**
- Försättssida med parter och avtalsinformation
- Fullständig specifikation med priser (inkl. moms)
- 11 juridiska paragrafer:
  - §1 Avtalets omfattning
  - §2 Leverans och installation
  - §3 Betalningsvillkor
  - §4 Avtalstid och uppsägning
  - §5 Garanti och ansvar
  - §6 Support och underhåll
  - §7 Ändringar och tillägg
  - §8 Force majeure
  - §9 Sekretess
  - §10 Tvister
  - §11 Särskilda villkor
- Signatursektion för båda parter

### API-endpoints
- `GET /api/products?category=larm&search=grundpaket` - Hämta produkter
- `GET /api/services` - Hämta tillgängliga tjänster
- `POST /api/generate-pdf` - Generera PDF (offert eller avtal)

## Konfiguration

### Miljövariabler
- `FLASK_DEBUG=1` - Aktivera debug-läge (endast utveckling)
- Standard: `FLASK_DEBUG=0` (produktion)

### Företagsinformation
Redigera företagsuppgifter i `scripts/server.py`:
```python
COMPANY_INFO = {
    'name': 'Tretec Larm AB',
    'address': 'Exempelgatan 123',
    'postal': '123 45 Stockholm',
    'phone': '08-123 45 67',
    'email': 'info@treteclarm.se',
    'org_nr': '556123-4567',
}
```

## Felsökning

### Problem: Servern startar inte
- Kontrollera att alla beroenden är installerade: `pip install -r requirements.txt`
- Kontrollera att port 5000 inte används av annan applikation

### Problem: Ellås-produkter laddas inte
- Detta är normalt om webbskrapning misslyckas
- Servern fortsätter fungera med de andra produktkategorierna
- Kontrollera loggar för mer information

### Problem: PDF genereras inte
- Kontrollera att alla required fält är ifyllda
- Kontrollera webbläsarens konsol för felmeddelanden
- Se serverlogs för detaljerad felinformation

## Säkerhet
- Server körs **INTE** i debug-läge i produktion som standard
- CORS är konfigurerad för utveckling (anpassa för produktion)
- Ingen autentisering implementerad (lägg till för produktionsmiljö)
- Validera all användarinput innan produktion

## Utveckling

Se `PROJEKTINFO.md` för:
- Detaljerad teknisk översikt
- Anpassningsguide
- Underhållsinstruktioner
- Arkitekturdetaljer

## Versionshistorik
- **V3.0** (2026-01-14): Omfattande affärsavtalsfunktionalitet med fullständiga avtalsvillkor
  - Komplett affärsavtalsmall med 11 juridiska paragrafer
  - Anpassningsbara betalningsplaner (5 fördefinierade alternativ)
  - Garantiperioder (Standard 24, Utökad 36, Premium 60 månader)
  - Supportnivåer (Bas, Standard, Premium)
  - Dynamiska avtalsvillkor med kundinformation
  - Multi-sida PDF-generering för professionella avtal
  - Särskilda villkor (fritext-fält)
  - Signatursektion för båda parter
- **V2.2** (2026-01-14): Organiserad filstruktur, grundläggande affärsavtal-stöd, förbättrad felhantering
- **V2.1**: Ellås-kategori tillagd
- **V2.0**: Smarta tjänsteberäkningar och extra rabatter

## Support
För frågor eller problem, kontakta utvecklingsteamet eller skapa en issue på GitHub.
