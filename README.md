# Tretec Quote System

Ett professionellt offertsystem för Tretec Larm AB, byggt med Python och Flask.

## Funktioner

### 📋 Kundregister
- Komplett kundhantering med alla viktiga uppgifter
- Fält för: kundnamn, adress, kontaktperson, fakturamejl, fakturaadress
- Spara och hantera kunduppgifter i JSON-format
- Snabb åtkomst till alla sparade kunder
- CRUD-operationer (Create, Read, Update, Delete)

### 💼 Offertlagring
- Spara offerter med unika ID för enkel åtkomst
- Ladda och redigera befintliga offerter
- Koppla offerter till kunder från registret
- JSON-baserad lagring för portabilitet

### 📄 PDF-generering
- Professionell PDF-offert med företagslogga
- Integrerad Tretec-logotyp i alla PDF:er
- Automatisk inkludering av affärsavtal baserat på Lantmännen-avtal
- Anpassningsbara avtalsmallar med kunddata
- **Tydliga varningar för saknade uppgifter** (⚠️ märkningar)

### 🛒 Produkthantering
- Lägg till produkter och tjänster med antal och pris
- Rabattsystem med procentuell avdrag
- Automatisk totalsummering
- Flexibel produktlista

### 🎨 Modernt användargränssnitt
- Intuitivt gränssnitt med tydlig struktur
- Responsiv design
- Färgkodade knappar för olika funktioner
- Realtidsuppdatering av totalsummor

## Installation

### Förutsättningar
- Python 3.7 eller senare
- pip (Python package manager)

### Steg-för-steg
1. Klona repositoryt:
   ```bash
   git clone https://github.com/marcuswanerskog-lab/tretec-quote-system.git
   cd tretec-quote-system
   ```

2. Installera dependencies:
   ```bash
   pip install flask flask-cors reportlab
   ```

3. Starta servern:
   ```bash
   python server.py
   ```

4. Öppna webbläsaren och gå till:
   ```
   http://localhost:5000
   ```

## Användning

### Kundregister
1. Fyll i kunduppgifter i vänster panel under "Kundregister"
2. Klicka på "💾 Spara kund" för att spara kunden
3. Sparade kunder visas i listan till höger
4. Klicka på en kund i listan för att redigera
5. Använd "🗑️ Ta bort" för att radera en kund

**Viktiga fält:**
- **Kundnamn** - Obligatoriskt
- **Fakturamejl** - Viktigt för fakturering
- **Fakturaadress** - Separat fakturaadress om den skiljer sig från leveransadress

### Offerthantering
1. Välj en kund från dropdown-menyn under "Offerthantering"
2. Lägg till produkter under "Produkter & Tjänster"
3. Ange eventuell rabatt
4. Klicka "💾 Spara offert" för att spara
5. Ett unikt offert-ID genereras automatiskt

**Ladda befintlig offert:**
1. Ange offert-ID i fältet
2. Klicka "📂 Ladda"
3. Offerten laddas med alla produkter och kunduppgifter

### PDF-generering
1. Se till att en kund är vald
2. Kontrollera att alla viktiga kunduppgifter är ifyllda
3. Markera "Inkludera affärsavtal i PDF" om avtalsmallar ska inkluderas
4. Klicka "📑 Generera PDF"
5. PDF:en laddas ner automatiskt

**Varningar i PDF:**
- Saknade fält markeras tydligt med ⚠️ symbolen
- Exempel: "⚠️ FAKTURAMEJL SAKNAS"
- Detta säkerställer att inga viktiga uppgifter glöms bort

### Affärsavtal
Systemet använder två avtalsfiler:
- `kopavtal_avtal.md` - Huvudavtal
- `avtal_bilagor.md` - Bilagor till avtalet

Dessa filer kan anpassas efter era specifika behov. Följande platshållare ersätts automatiskt:
- `{KUNDNAMN}` - Kundens namn
- `{ADRESS}` - Kundens adress
- `{DATUM}` - Aktuellt datum

## Datalagring

Systemet använder JSON-filer för lagring:
- `customers.json` - Alla kunduppgifter
- `quotes.json` - Alla sparade offerter

Dessa filer skapas automatiskt vid första körningen.

## Säkerhet och Backup

**Rekommendationer:**
- Ta regelbundna backuper av `customers.json` och `quotes.json`
- Skydda dessa filer då de innehåller känslig kunddata
- Överväg att flytta till en databas för produktionsmiljö

## Versionshistorik

- **V3.0** (2026-01-14): 
  - ✨ Komplett kundregister med JSON-lagring
  - ✨ Offertlagring med unika ID
  - ✨ Affärsavtal i PDF med anpassningsbara mallar
  - ✨ Tydliga varningar för saknade uppgifter
  - ✨ Förbättrat användargränssnitt
  - ✨ Integrerad Tretec-logotyp i PDF
  
- **V2.1**: Ellås-kategori tillagd

- **V2.0**: Smarta tjänsteberäkningar och extra rabatter

## Support

För frågor eller problem, kontakta utvecklingsteamet.

## Licens

Internt system för Tretec Larm AB.
