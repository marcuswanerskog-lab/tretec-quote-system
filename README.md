# Tretec Quote System

Ett professionellt offertsystem för Tretec Larm AB, byggt med Python och Flask.

## Funktioner
- ✅ Produkthantering med sök och filtrering
- ✅ PDF-offertgenerering med företagsprofil
- ✅ PDF-generering för affärsavtal med samma layout som offerter
- ✅ Ellås-produkter från Låsgiganten (automatiskt skrapade)
- ✅ Rabattsystem för produkter och kunder
- ✅ Tjänster med timbaserade beräkningar
- ✅ Serverbaserad PDF-generering
- ✅ Förbättrad felhantering med loggning
- ✅ Responsiv webbgränssnitt

## Projektstruktur

```
tretec-quote-system/
├── scripts/
│   └── server.py          # Huvudserver med Flask-applikation
├── templates/
│   └── index.html         # Webbgränssnitt för offerter och avtal
├── static/
│   └── logo-placeholder.txt  # Plats för företagslogga
├── requirements.txt       # Python-dependencies
├── .gitignore            # Git-ignoreringar
└── README.md             # Denna fil
```

## Installation

### Förutsättningar
- Python 3.8 eller senare
- pip (Python package manager)

### Steg-för-steg installation

1. **Klona repositoryt**
   ```bash
   git clone https://github.com/marcuswanerskog-lab/tretec-quote-system.git
   cd tretec-quote-system
   ```

2. **Skapa virtuell miljö (rekommenderas)**
   ```bash
   python -m venv venv
   
   # På Windows:
   venv\Scripts\activate
   
   # På Mac/Linux:
   source venv/bin/activate
   ```

3. **Installera dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Kör servern**
   ```bash
   cd scripts
   python server.py
   ```

5. **Öppna webbläsaren**
   
   Navigera till: `http://localhost:5000`

## Användning

### Skapa en offert

1. Öppna webbgränssnittet på `http://localhost:5000`
2. Fyll i kundinformation (namn är obligatoriskt)
3. Sök och filtrera produkter efter kategori
4. Lägg till produkter och tjänster i offerten
5. Justera antal och rabatt för varje artikel
6. Klicka på "Generera Offert (PDF)" för att ladda ner PDF-filen

### Skapa ett affärsavtal

1. Klicka på fliken "Nytt Affärsavtal"
2. Fyll i kundinformation (namn och företag är obligatoriskt)
3. Ange avtalsnummer (auto-genereras om tomt)
4. Välj avtalsperiod (12, 24 eller 36 månader)
5. Lägg till produkter och tjänster
6. Klicka på "Generera Affärsavtal (PDF)"

### Produktkategorier

- **Larm**: Grundpaket, utökningspaket, sensorer
- **Kamera**: IP-kameror, NVR-system
- **Ellås**: Elektroniska lås (hämtas automatiskt från Låsgiganten)

### Tjänster

Alla tjänster är timbaserade med justerbara timantal:
- Installation larm
- Installation kamera
- Service och underhåll
- Konsultation

## API-endpoints

### GET `/api/products`
Hämta alla produkter med valfri filtrering.

**Query-parametrar:**
- `category` (optional): Filtrera efter kategori (larm, kamera, ellas)
- `search` (optional): Sök efter produktnamn

**Exempel:**
```bash
curl "http://localhost:5000/api/products?category=larm"
```

### GET `/api/services`
Hämta alla tjänster.

**Exempel:**
```bash
curl "http://localhost:5000/api/services"
```

### POST `/api/generate-pdf`
Generera PDF för offert eller affärsavtal.

**Request body:**
```json
{
  "type": "quote",  // eller "agreement"
  "customer": {
    "name": "Johan Andersson",
    "company": "Anderssons Bygg AB",
    "email": "johan@anderssonsbygg.se"
  },
  "items": [
    {
      "name": "Grundpaket Larm",
      "price": 12500,
      "quantity": 1,
      "discount": 10
    }
  ],
  "agreement_number": "AVT-001",  // Endast för affärsavtal
  "contract_period": "12 månader"  // Endast för affärsavtal
}
```

## Konfiguration

### Företagsinformation

Uppdatera företagsinformation i `scripts/server.py`:

```python
COMPANY_INFO = {
    'name': 'Tretec Larm AB',
    'address': 'Din adress',
    'postal': 'Postnummer Ort',
    'phone': 'Telefonnummer',
    'email': 'info@treteclarm.se',
    'org_nr': 'Organisationsnummer',
}
```

### Lägga till företagslogga

1. Placera din logga som `static/logo.png`
2. Uppdatera PDF-genereringsfunktionerna i `server.py` för att inkludera loggan

## Felhantering

Servern inkluderar omfattande felhantering:
- **Loggning**: Alla fel loggas med tidsstämpel och stack trace
- **HTTP-felkoder**: Korrekt 404, 500 och generell felhantering
- **Användarvänliga felmeddelanden**: Fel visas tydligt i webbgränssnittet
- **Graceful degradation**: Om ellås-skrapning misslyckas fortsätter systemet fungera

Loggar visas i konsolen där servern körs. För produktion, konfigurera loggning till fil.

## Felsökning

### Servern startar inte
- Kontrollera att alla dependencies är installerade: `pip install -r requirements.txt`
- Verifiera att port 5000 inte används av en annan process
- Kör med `python -v server.py` för detaljerad output

### PDF genereras inte
- Kontrollera att ReportLab är korrekt installerat
- Se serverloggar för specifika felmeddelanden
- Verifiera att all kundinformation är ifylld

### Ellås-produkter visas inte
- Detta är normalt vid första körningen om webbskrapningen misslyckas
- Systemet försöker hämta produkter vid serverstart
- Kontrollera internetanslutning och serverloggar

## Säkerhet

- Använd HTTPS i produktion
- Implementera autentisering för känsliga operationer
- Validera all input på serversidan
- Håll dependencies uppdaterade: `pip list --outdated`

## Utveckling

### Lägg till nya produkter

Redigera `PRODUCTS`-dictionaryn i `scripts/server.py`:

```python
PRODUCTS = {
    'ny_kategori': [
        {'id': 100, 'name': 'Ny produkt', 'price': 1000, 'category': 'ny_kategori'},
    ]
}
```

### Lägg till nya tjänster

Redigera `SERVICES`-listan i `scripts/server.py`:

```python
SERVICES = [
    {'id': 5, 'name': 'Ny tjänst', 'hourly_rate': 900, 'estimated_hours': 3},
]
```

## Uppdateringar

- **V3.0**: Strukturerad projektorganisation med scripts/, templates/, static/
- **V2.2**: Stöd för affärsavtal-mallar med samma layout som offerter
- **V2.1**: Ellås-kategori tillagd med automatisk skrapning
- **V2.0**: Smarta tjänsteberäkningar och extra rabatter
- **V1.0**: Första versionen med grundläggande funktioner

## Support

För frågor eller problem, kontakta:
- Email: info@treteclarm.se
- GitHub Issues: https://github.com/marcuswanerskog-lab/tretec-quote-system/issues

## Licens

Proprietär programvara för Tretec Larm AB. Alla rättigheter förbehållna.
