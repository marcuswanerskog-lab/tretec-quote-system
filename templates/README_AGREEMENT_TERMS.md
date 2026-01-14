# Avtalsvillkor - Anpassningsguide

Detta dokument förklarar hur du anpassar affärsavtalsvillkoren i Tretec Quote System.

## Översikt

Affärsavtalsmallen finns i `templates/agreement_terms.py` och innehåller:
- **AGREEMENT_TERMS**: Fullständiga avtalsvillkor med 11 paragrafer
- **PAYMENT_PLAN_TEMPLATES**: Fördefinierade betalningsplaner
- **WARRANTY_PERIODS**: Garantiperioder (Standard, Utökad, Premium)
- **SERVICE_LEVELS**: Supportnivåer (Bas, Standard, Premium)

## Anpassa Avtalsvillkor

### 1. Grundläggande Information

Redigera texten i `AGREEMENT_TERMS` för att matcha ditt företags policy:

```python
AGREEMENT_TERMS = {
    'title': 'AFFÄRSAVTAL - SÄKERHETS- OCH LARMSYSTEM',
    'introduction': """Din egen introduktionstext...""",
    # ... etc
}
```

### 2. Avtalsklausuler

Avtalet innehåller följande paragrafer:

- **§1 AVTALETS OMFATTNING** - Vad avtalet inkluderar
- **§2 LEVERANS OCH INSTALLATION** - Leveransvillkor och installationsprocess
- **§3 BETALNINGSVILLKOR** - Priser, betalningsplan, faktureringsvillkor
- **§4 AVTALSTID OCH UPPSÄGNING** - Avtalslängd, förlängning, uppsägningsregler
- **§5 GARANTI OCH ANSVAR** - Garantivillkor och ansvarsbegränsningar
- **§6 SUPPORT OCH UNDERHÅLL** - Teknisk support och servicenivåer
- **§7 ÄNDRINGAR OCH TILLÄGG** - Hur avtalet kan ändras
- **§8 FORCE MAJEURE** - Ansvarsfrihet vid extraordinära händelser
- **§9 SEKRETESS** - Konfidentialitetsklausuler
- **§10 TVISTER** - Tvistelösning och tillämplig lag
- **§11 SÄRSKILDA VILLKOR** - Valfria kundspecifika villkor

### 3. Betalningsplaner

Lägg till eller ändra betalningsplaner i `PAYMENT_PLAN_TEMPLATES`:

```python
PAYMENT_PLAN_TEMPLATES = {
    'my_custom_plan': """40% vid avtalstecknande
                         30% vid leverans
                         30% vid driftsättning""",
}
```

Uppdatera sedan `templates/index.html` för att visa den nya planen i dropdown-menyn:

```html
<option value="my_custom_plan">Min Egen Plan</option>
```

### 4. Garantiperioder

Ändra eller lägg till garantiperioder:

```python
WARRANTY_PERIODS = {
    'standard': '24 månader',
    'extended': '36 månader',
    'premium': '60 månader',
    'lifetime': 'Livstidsgaranti'  # Ny period
}
```

### 5. Supportnivåer

Anpassa supportnivåer efter ditt företags serviceerbjudande:

```python
SERVICE_LEVELS = {
    'basic': {
        'name': 'Bas',
        'description': 'Teknisk support under kontorstid',
        'response_time': '2 arbetsdagar',
        'support_hours': 'Vardagar 08:00-17:00'
    },
    # Lägg till fler nivåer...
}
```

## Dynamiska Fält

Vissa fält fylls automatiskt i från formulärdata eller systemet:

### Kundinformation
- `{customer_name}` - Kundens namn
- `{customer_company}` - Företagsnamn
- `{customer_email}` - E-postadress
- `{customer_phone}` - Telefonnummer

### Företagsinformation
- `{company_name}` - Från COMPANY_INFO i server.py
- `{company_org_nr}` - Organisationsnummer
- `{company_address}` - Adress
- `{company_postal}` - Postnummer och ort
- `{company_phone}` - Telefon
- `{company_email}` - E-post

### Avtalsdetaljer
- `{contract_start_date}` - Automatiskt genererat (dagens datum)
- `{contract_end_date}` - Beräknat från avtalsperiod
- `{contract_period}` - Från formulär (12/24/36 månader)
- `{installation_date}` - Från formulär
- `{total_amount}` - Beräknat från produkter/tjänster
- `{warranty_period}` - Från vald garantiperiod
- `{special_terms}` - Fritext från formulär

## Exempel: Skapa Branschspecifikt Avtal

Om du vill anpassa avtalet för en annan bransch (t.ex. IT-tjänster):

1. Kopiera `agreement_terms.py` till `agreement_terms_it.py`
2. Ändra titeln och introduktionen
3. Anpassa paragraferna för IT-specifika villkor
4. Uppdatera import i `server.py`:

```python
from agreement_terms_it import AGREEMENT_TERMS, ...
```

## Juridisk Ansvarsfriskrivning

**VIKTIGT**: Dessa avtalsvillkor är exempel och inte juridiskt granskade. 
Konsultera alltid en jurist innan du använder avtalsmallar i produktion.

Avtalsmallen är baserad på svenska standardavtal för säkerhets- och larmsystem,
men måste anpassas för:
- Ditt specifika företag och verksamhet
- Gällande svensk lag och EU-direktiv
- Branschspecifika krav och standarder
- Försäkringsvillkor och ansvarsförsäkring

## Support

För frågor om anpassning av avtalsvillkor:
- Se `PROJEKTINFO.md` för teknisk dokumentation
- Konsultera juridisk rådgivare för avtalsrättsliga frågor
- GitHub Issues för tekniska problem

---
Senast uppdaterad: 2026-01-14
