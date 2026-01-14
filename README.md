# Tretec Quote System

Ett komplett offertsystem för Tretec Larm AB, byggt med Python och Flask.

## 🎯 Funktioner

### Kundhantering
- **JSON-baserat kundregister** - Lagrar kunder med komplett information
- **Kunduppgifter** - Namn, organisationsnummer, telefon, e-post
- **Fakturainformation** - Dedikerade fält för fakturamejl och fakturaadress
- **Varningar för saknad information** - Automatisk kontroll av ofullständiga kunduppgifter
- **CRUD-operationer** - Skapa, visa, redigera och ta bort kunder

### Offerthantering
- **Spara och ladda offerter** - Persistent lagring i JSON-format
- **Offerteditor** - Komplett gränssnitt för att skapa och redigera offerter
- **Produktval** - Lägg till produkter och tjänster med sökning och filtrering
- **Automatiska beräkningar** - Summor, moms och totaler beräknas automatiskt
- **Rabattsystem** - Individuella rabatter per produkt
- **Anteckningar** - Lägg till kommentarer och noteringar till offerten

### PDF-generering
- **Professionell layout** - Välformaterade PDF-offerter
- **Integrerad logotyp** - Tretec Larm-logotypen inkluderas automatiskt
- **Komplett kundinfo** - Visar alla kunduppgifter, markerar saknade fält i rött
- **Produkttabell** - Tydlig presentation av produkter, priser, rabatter och summor
- **Anpassningsbart affärsavtal** - Egen text för villkor, betalningsvillkor och garantier
- **Standardtext** - Förifylld text som kan anpassas vid behov
- **Signaturssektion** - Plats för underskrift och datum

### Produkthantering
- **Produktkatalog** - Förkonfigurerad med larm- och tjänsteprodukter
- **Kategorier** - Larm, Ellås, Tjänster
- **Sök och filter** - Hitta produkter snabbt
- **Timbaserade tjänster** - Stöd för installation och service per timme

### Användargränssnitt
- **Fliksystem** - Överskådlig navigation mellan funktioner
- **Responsiv design** - Fungerar på både desktop och mobil
- **Realtidsvalidering** - Kontrollerar och varnar för saknade uppgifter
- **Visuell feedback** - Tydliga meddelanden och statusindikationer

## 🚀 Installation

1. **Klona repositoryt**
   ```bash
   git clone https://github.com/marcuswanerskog-lab/tretec-quote-system.git
   cd tretec-quote-system
   ```

2. **Installera dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Eller manuellt:
   ```bash
   pip install flask flask-cors reportlab requests beautifulsoup4
   ```

3. **Kör servern**
   ```bash
   python server.py
   ```

4. **Öppna webbläsaren**
   ```
   http://localhost:5000
   ```

## 📖 Användning

### Skapa en kund
1. Gå till fliken "Kunder"
2. Klicka på "Lägg till ny kund"
3. Fyll i kunduppgifter (namn, fakturamejl och fakturaadress är viktiga)
4. Klicka "Skapa Kund"

### Skapa en offert
1. Gå till fliken "Ny Offert"
2. Välj eller skapa en kund
3. Lägg till produkter/tjänster
4. Justera antal och rabatter
5. Lägg till anteckningar och anpassad avtalstext (valfritt)
6. Klicka "Spara Offert" för att spara
7. Klicka "Generera PDF" för att skapa PDF-fil

### Redigera befintlig offert
1. Gå till fliken "Sparade Offerter"
2. Klicka "Ladda" på den offert du vill redigera
3. Gör dina ändringar
4. Spara igen

## 🗂️ Datalagring

Systemet använder JSON-filer för datalagring:
- `customers.json` - Kundregister
- `quotes.json` - Sparade offerter
- `products.json` - Produktkatalog

Filerna skapas automatiskt vid första körningen.

## 📋 API-endpoints

### Kunder
- `GET /api/customers` - Hämta alla kunder
- `POST /api/customers` - Skapa ny kund
- `GET /api/customers/<id>` - Hämta specifik kund
- `PUT /api/customers/<id>` - Uppdatera kund
- `DELETE /api/customers/<id>` - Ta bort kund

### Offerter
- `GET /api/quotes` - Hämta alla offerter
- `POST /api/quotes` - Skapa ny offert
- `GET /api/quotes/<id>` - Hämta specifik offert
- `PUT /api/quotes/<id>` - Uppdatera offert
- `DELETE /api/quotes/<id>` - Ta bort offert

### Produkter
- `GET /api/products` - Hämta produkter (med filter: ?category=Larm&search=term)
- `POST /api/products` - Lägg till produkt

### PDF
- `POST /api/generate-pdf` - Generera PDF från offertdata

## 🔄 Uppdateringar
- **V3.0 (2026-01)**: Kundregister, offertlagring, förbättrad PDF-generering
  - JSON-baserad kundatabas med fakturainformation
  - Spara, ladda och redigera offerter
  - Varningar för saknade kunduppgifter i UI och PDF
  - Anpassningsbart affärsavtal i PDF
  - Integrerad logotyp i PDF
  - Komplett webb-UI med flikar
- V2.1: Ellås-kategori tillagd
- V2.0: Smarta tjänsteberäkningar och extra rabatter

## 🛠️ Teknisk stack
- **Backend**: Python 3, Flask
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **PDF**: ReportLab
- **Data**: JSON-filbaserad lagring

## 📝 Licens
Copyright © 2026 Tretec Larm AB
