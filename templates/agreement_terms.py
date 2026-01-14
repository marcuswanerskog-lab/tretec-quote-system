#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mall för affärsavtalsvillkor
Baserat på standardavtal för säkerhets- och larmsystem
"""

# Avtalsvillkor - dessa kan anpassas efter behov
AGREEMENT_TERMS = {
    'title': 'AFFÄRSAVTAL - SÄKERHETS- OCH LARMSYSTEM',
    
    'introduction': """
Detta avtal reglerar leverans, installation och underhåll av säkerhets- och larmsystem
mellan Tretec Larm AB (nedan kallad "Leverantören") och kund (nedan kallad "Kunden").
""",
    
    'parties_section': """
PARTER

Leverantör:
{company_name}
Org.nr: {company_org_nr}
{company_address}
{company_postal}
Tel: {company_phone}
E-post: {company_email}

Kund:
{customer_name}
{customer_company}
{customer_email}
{customer_phone}
""",
    
    'scope_section': """
§1 AVTALETS OMFATTNING

Detta avtal omfattar leverans, installation, driftsättning och underhåll av säkerhets-
och larmutrustning enligt bifogad specifikation. Leveransen inkluderar:

• Säkerhets- och larmutrustning enligt specifikation
• Installation och driftsättning av utrustning
• Användarkurs och dokumentation
• Garantiservice enligt § 6
• Teknisk support enligt § 7
""",
    
    'delivery_section': """
§2 LEVERANS OCH INSTALLATION

2.1 Leveranstid
Leveransen påbörjas inom 14 arbetsdagar från avtalsundertecknande. 
Installation och driftsättning ska vara slutförd senast {installation_date}.

2.2 Installation
Leverantören ansvarar för professionell installation av all utrustning. 
Kunden ska tillhandahålla nödvändig tillgång till lokaler och erforderlig 
infrastruktur (t.ex. eluttag, nätverksanslutning).

2.3 Driftsättning och genomgång
Efter färdigställd installation genomförs testning och driftsättning tillsammans med 
kunden. Användarkurs och genomgång av systemet ingår.
""",
    
    'payment_section': """
§3 BETALNINGSVILLKOR

3.1 Totalt belopp
Total kostnad enligt detta avtal uppgår till {total_amount} kr exkl. moms.
Moms tillkommer enligt gällande lagstiftning (f.n. 25%).

3.2 Betalningsplan
{payment_plan}

3.3 Betalningsvillkor
Faktura ska betalas inom 30 dagar netto från fakturadatum. 
Vid försenad betalning utgår dröjsmålsränta enligt räntelagen.

3.4 Äganderätt
Levererad utrustning förblir leverantörens egendom till dess full betalning 
erlagts av kunden.
""",
    
    'contract_period_section': """
§4 AVTALSTID OCH UPPSÄGNING

4.1 Avtalstid
Detta avtal gäller från {contract_start_date} till {contract_end_date} ({contract_period}).

4.2 Förlängning
Avtalet förlängs automatiskt med 12 månader i taget om det inte sägs upp 
av någon part senast 3 månader före avtalstidens utgång.

4.3 Uppsägning
Uppsägning ska ske skriftligen till motparten. Vid uppsägning i förtid kan 
leverantören debitera administrativa kostnader samt eventuella 
avskrivningskostnader för installerad utrustning.
""",
    
    'warranty_section': """
§5 GARANTI OCH ANSVAR

5.1 Garanti
Leverantören garanterar att levererad utrustning är fri från material- och 
fabrikationsfel under en period av {warranty_period} från leveransdatum. 
Under garantitiden åtgärdas fel och brister utan kostnad för kunden.

5.2 Garantins omfattning
Garantin omfattar inte:
• Skador orsakade av felaktig hantering eller vårdslöshet
• Skador från yttre påverkan (blixtnedslag, översvämning, brand m.m.)
• Obehöriga ändringar eller reparationer
• Normalt slitage och förbrukningsartiklar

5.3 Ansvarsbegränsning
Leverantörens ansvar är begränsat till direkta skador på utrustningen. 
Leverantören ansvarar inte för följdskador eller indirekta förluster.
""",
    
    'support_section': """
§6 SUPPORT OCH UNDERHÅLL

6.1 Teknisk support
Leverantören tillhandahåller teknisk support via telefon och e-post under 
kontorstid (vardagar 08:00-17:00). Kontaktuppgifter:
Tel: {company_phone}
E-post: {company_email}

6.2 Underhåll och service
Årlig service och funktionskontroll rekommenderas och kan beställas separat.
Akut service utanför ordinarie arbetstid debiteras enligt gällande prislista.

6.3 Reservdelar
Reservdelar tillhandahålls enligt tillverkarens anvisningar och 
produktlivscykel. Vid utgångna produkter tillhandahålls motsvarande 
ersättningsprodukter.
""",
    
    'changes_section': """
§7 ÄNDRINGAR OCH TILLÄGG

7.1 Ändringar av avtalet
Ändringar och tillägg till detta avtal ska göras skriftligen och undertecknas 
av båda parter för att vara giltiga.

7.2 Utökning av system
Om kunden önskar utöka systemet med ytterligare komponenter upprättas 
tilläggsavtal med specifikation och priser.
""",
    
    'force_majeure_section': """
§8 FORCE MAJEURE

Ingen av parterna är ansvarig för dröjsmål eller utebliven leverans till följd 
av omständigheter som parten inte kunnat råda över, såsom krig, naturkatastrof, 
brand, strejk, lockout, myndighetsbeslut, eller annan liknande omständighet.
""",
    
    'confidentiality_section': """
§9 SEKRETESS

Båda parter förbinder sig att behandla all information som utbyts i samband 
med detta avtal konfidentiellt. Sekretessen gäller även efter avtalets upphörande.
""",
    
    'disputes_section': """
§10 TVISTER

Tvist i anledning av detta avtal ska i första hand lösas genom förhandling 
mellan parterna. Om överenskommelse inte kan nås ska tvisten avgöras enligt 
svensk lag vid svensk domstol.
""",
    
    'special_terms_section': """
§11 SÄRSKILDA VILLKOR

{special_terms}
""",
    
    'signatures_section': """
UNDERSKRIFTER

Detta avtal har upprättats i två exemplar varav parterna tagit var sitt.


Datum: {contract_date}


_____________________________          _____________________________
För Tretec Larm AB                     För {customer_company}
{company_representative}               {customer_name}


_____________________________          _____________________________
Namnförtydligande                      Namnförtydligande


_____________________________          _____________________________
Ort och datum                          Ort och datum
"""
}

# Standardvärden för betalningsplan
PAYMENT_PLAN_TEMPLATES = {
    'full_payment': '100% vid leverans',
    
    'split_50_50': """50% förskottsbetalning vid avtalsundertecknande
50% vid färdigställd installation och driftsättning""",
    
    'split_30_70': """30% förskottsbetalning vid avtalsundertecknande
70% vid färdigställd installation och driftsättning""",
    
    'installments_3': """40% förskottsbetalning vid avtalsundertecknande
30% vid påbörjad installation
30% vid färdigställd installation och driftsättning""",
    
    'installments_4': """30% förskottsbetalning vid avtalsundertecknande
25% vid leverans av material
25% vid påbörjad installation
20% vid färdigställd installation och driftsättning""",
    
    'monthly': """Månadsvis betalning enligt särskild betalningsplan
Första betalning förfaller {first_payment_date}
Därefter månatligen under {contract_period}"""
}

# Garantiperioder
WARRANTY_PERIODS = {
    'standard': '24 månader',
    'extended': '36 månader',
    'premium': '60 månader'
}

# Servicenivåer
SERVICE_LEVELS = {
    'basic': {
        'name': 'Bas',
        'description': 'Teknisk support under kontorstid',
        'response_time': '2 arbetsdagar',
        'support_hours': 'Vardagar 08:00-17:00'
    },
    'standard': {
        'name': 'Standard',
        'description': 'Utökad support och årlig service',
        'response_time': '1 arbetsdag',
        'support_hours': 'Vardagar 07:00-19:00'
    },
    'premium': {
        'name': 'Premium',
        'description': '24/7 support och prioriterad service',
        'response_time': '4 timmar',
        'support_hours': '24/7 alla dagar'
    }
}
