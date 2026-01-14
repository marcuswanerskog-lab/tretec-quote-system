#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tretec Quote System Server
Ett offertsystem för Tretec Larm AB med PDF-generering
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import requests
from bs4 import BeautifulSoup
import io
import logging
from datetime import datetime, timedelta
import traceback
import sys
import os

# Add templates directory to path for importing agreement terms
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'templates'))
from agreement_terms import (
    AGREEMENT_TERMS, 
    PAYMENT_PLAN_TEMPLATES, 
    WARRANTY_PERIODS, 
    SERVICE_LEVELS
)

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
CORS(app)

# Konfigurera loggning
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Produktdatabas
PRODUCTS = {
    'larm': [
        {'id': 1, 'name': 'Grundpaket Larm', 'price': 12500, 'category': 'larm'},
        {'id': 2, 'name': 'Utökningspaket Larm', 'price': 8500, 'category': 'larm'},
        {'id': 3, 'name': 'Rörelsedetektor', 'price': 950, 'category': 'larm'},
        {'id': 4, 'name': 'Dörr/Fönsterkontakt', 'price': 650, 'category': 'larm'},
    ],
    'kamera': [
        {'id': 5, 'name': 'IP-kamera Inomhus', 'price': 3200, 'category': 'kamera'},
        {'id': 6, 'name': 'IP-kamera Utomhus', 'price': 4500, 'category': 'kamera'},
        {'id': 7, 'name': 'NVR 8-kanaler', 'price': 6500, 'category': 'kamera'},
    ],
    'ellas': [],  # Fylls genom skrapning
}

# Tjänster
SERVICES = [
    {'id': 1, 'name': 'Installation larm', 'hourly_rate': 850, 'estimated_hours': 4},
    {'id': 2, 'name': 'Installation kamera', 'hourly_rate': 850, 'estimated_hours': 6},
    {'id': 3, 'name': 'Service och underhåll', 'hourly_rate': 950, 'estimated_hours': 2},
    {'id': 4, 'name': 'Konsultation', 'hourly_rate': 1200, 'estimated_hours': 1},
]

# Företagsinformation
COMPANY_INFO = {
    'name': 'Tretec Larm AB',
    'address': 'Exempelgatan 123',
    'postal': '123 45 Stockholm',
    'phone': '08-123 45 67',
    'email': 'info@treteclarm.se',
    'org_nr': '556123-4567',
}


def scrape_ellas_products():
    """Skrapa ellås-produkter från Låsgiganten"""
    try:
        logger.info("Försöker skrapa ellås-produkter från Låsgiganten...")
        url = "https://www.lasgiganten.se/ellas"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        products = []
        
        # Försök hitta produkter (detta är en generisk sökare som kan behöva anpassas)
        product_items = soup.find_all(['div', 'article'], class_=lambda x: x and ('product' in x.lower() if x else False))
        
        for idx, item in enumerate(product_items[:10], start=100):  # Max 10 produkter
            try:
                name_elem = item.find(['h2', 'h3', 'a'], class_=lambda x: x and ('title' in x.lower() or 'name' in x.lower() if x else False))
                price_elem = item.find(['span', 'div'], class_=lambda x: x and 'price' in x.lower() if x else False)
                
                if name_elem and price_elem:
                    name = name_elem.get_text(strip=True)
                    price_text = price_elem.get_text(strip=True)
                    # Extrahera nummer från pris
                    price_digits = ''.join(filter(str.isdigit, price_text))
                    if not price_digits:
                        continue
                    price = int(price_digits)
                    
                    if name and price > 0:
                        products.append({
                            'id': idx,
                            'name': name,
                            'price': price,
                            'category': 'ellas'
                        })
            except Exception as e:
                logger.debug(f"Kunde inte parsa produkt: {e}")
                continue
        
        if products:
            PRODUCTS['ellas'] = products
            logger.info(f"Hittade {len(products)} ellås-produkter")
        else:
            logger.warning("Inga ellås-produkter kunde skrapas")
            
    except Exception as e:
        logger.error(f"Fel vid skrapning av ellås-produkter: {e}")
        logger.debug(traceback.format_exc())


@app.route('/')
def index():
    """Startsida med offertformulär"""
    try:
        return render_template('index.html', 
                             products=PRODUCTS, 
                             services=SERVICES,
                             company=COMPANY_INFO)
    except Exception as e:
        logger.error(f"Fel vid rendering av startsida: {e}")
        logger.debug(traceback.format_exc())
        return f"Ett fel uppstod: {str(e)}", 500


@app.route('/api/products')
def get_products():
    """Hämta alla produkter"""
    try:
        category = request.args.get('category')
        search = request.args.get('search', '').lower()
        
        if category and category in PRODUCTS:
            products = PRODUCTS[category]
        else:
            products = []
            for cat_products in PRODUCTS.values():
                products.extend(cat_products)
        
        if search:
            products = [p for p in products if search in p['name'].lower()]
        
        return jsonify(products)
    except Exception as e:
        logger.error(f"Fel vid hämtning av produkter: {e}")
        logger.debug(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


@app.route('/api/services')
def get_services():
    """Hämta alla tjänster"""
    try:
        return jsonify(SERVICES)
    except Exception as e:
        logger.error(f"Fel vid hämtning av tjänster: {e}")
        logger.debug(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    """Generera PDF-offert"""
    try:
        # Validera Content-Type
        if not request.is_json:
            return jsonify({'error': 'Content-Type måste vara application/json'}), 400
        
        data = request.json
        if not data:
            return jsonify({'error': 'Ingen data skickades'}), 400
        
        doc_type = data.get('type', 'quote')  # 'quote' eller 'agreement'
        
        if doc_type == 'agreement':
            pdf_buffer = generate_agreement_pdf(data)
        else:
            pdf_buffer = generate_quote_pdf(data)
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'tretec_{doc_type}_{datetime.now().strftime("%Y%m%d")}.pdf'
        )
    except Exception as e:
        logger.error(f"Fel vid generering av PDF: {e}")
        logger.debug(traceback.format_exc())
        return jsonify({'error': f'Kunde inte generera PDF: {str(e)}'}), 500


def generate_quote_pdf(data):
    """Generera PDF för offert"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Företagslogga och header
    y_position = height - 40*mm
    c.setFont("Helvetica-Bold", 20)
    c.drawString(40*mm, y_position, COMPANY_INFO['name'])
    
    c.setFont("Helvetica", 10)
    y_position -= 15
    c.drawString(40*mm, y_position, COMPANY_INFO['address'])
    y_position -= 12
    c.drawString(40*mm, y_position, COMPANY_INFO['postal'])
    y_position -= 12
    c.drawString(40*mm, y_position, f"Tel: {COMPANY_INFO['phone']}")
    y_position -= 12
    c.drawString(40*mm, y_position, f"Email: {COMPANY_INFO['email']}")
    
    # Offerttitel
    y_position -= 25
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40*mm, y_position, "OFFERT")
    
    # Kundinformation
    y_position -= 20
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40*mm, y_position, "Kund:")
    c.setFont("Helvetica", 10)
    
    customer = data.get('customer', {})
    y_position -= 15
    c.drawString(40*mm, y_position, customer.get('name', 'N/A'))
    if customer.get('company'):
        y_position -= 12
        c.drawString(40*mm, y_position, customer.get('company'))
    
    # Datum
    y_position -= 20
    c.setFont("Helvetica", 10)
    c.drawString(40*mm, y_position, f"Datum: {datetime.now().strftime('%Y-%m-%d')}")
    
    # Produkter och tjänster tabell
    y_position -= 25
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40*mm, y_position, "Specifikation:")
    
    y_position -= 15
    table_data = [['Beskrivning', 'Antal', 'Pris/st', 'Rabatt', 'Summa']]
    
    items = data.get('items', [])
    total = 0
    
    for item in items:
        qty = item.get('quantity', 1)
        price = item.get('price', 0)
        discount = item.get('discount', 0)
        
        item_total = qty * price * (1 - discount/100)
        total += item_total
        
        table_data.append([
            item.get('name', ''),
            str(qty),
            f"{price:,.0f} kr",
            f"{discount}%",
            f"{item_total:,.0f} kr"
        ])
    
    # Rita tabell
    t = Table(table_data, colWidths=[80*mm, 20*mm, 25*mm, 20*mm, 25*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    table_height = len(table_data) * 20
    y_position -= table_height
    t.wrapOn(c, width, height)
    t.drawOn(c, 40*mm, y_position)
    
    # Totalt
    y_position -= 25
    c.setFont("Helvetica-Bold", 12)
    c.drawString(145*mm, y_position, f"Totalt: {total:,.0f} kr")
    
    # Moms
    y_position -= 15
    c.setFont("Helvetica", 10)
    vat = total * 0.25
    c.drawString(145*mm, y_position, f"Varav moms (25%): {vat:,.0f} kr")
    
    # Villkor
    y_position -= 25
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40*mm, y_position, "Villkor:")
    c.setFont("Helvetica", 9)
    y_position -= 12
    c.drawString(40*mm, y_position, "Offerten gäller i 30 dagar från datum ovan.")
    y_position -= 10
    c.drawString(40*mm, y_position, "Betalningsvillkor: 30 dagar netto.")
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer


def generate_agreement_pdf(data):
    """Generera omfattande PDF för affärsavtal med fullständiga avtalsvillkor"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Extrahera data
    customer = data.get('customer', {})
    items = data.get('items', [])
    contract_period = data.get('contract_period', '12 månader')
    agreement_number = data.get('agreement_number', f'AVT-{datetime.now().strftime("%Y%m%d-%H%M%S")}')
    payment_plan = data.get('payment_plan', 'split_50_50')
    warranty_period = data.get('warranty_period', 'standard')
    service_level = data.get('service_level', 'standard')
    installation_date = data.get('installation_date', (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'))
    special_terms = data.get('special_terms', 'Inga särskilda villkor.')
    
    # Beräkna totaler
    total = 0
    for item in items:
        qty = item.get('quantity', 1)
        price = item.get('price', 0)
        discount = item.get('discount', 0)
        item_total = qty * price * (1 - discount/100)
        total += item_total
    
    vat = total * 0.25
    total_with_vat = total + vat
    
    # Beräkna avtalsdatum
    contract_start = datetime.now()
    if '12' in contract_period:
        contract_end = contract_start + timedelta(days=365)
    elif '24' in contract_period:
        contract_end = contract_start + timedelta(days=730)
    elif '36' in contract_period:
        contract_end = contract_start + timedelta(days=1095)
    else:
        contract_end = contract_start + timedelta(days=365)
    
    # ===== SIDA 1: FÖRSÄTTSSIDA OCH PARTER =====
    y_pos = height - 40*mm
    
    # Header med företagsinfo
    c.setFont("Helvetica-Bold", 20)
    c.drawString(40*mm, y_pos, COMPANY_INFO['name'])
    
    c.setFont("Helvetica", 9)
    y_pos -= 12
    c.drawString(40*mm, y_pos, COMPANY_INFO['address'])
    y_pos -= 10
    c.drawString(40*mm, y_pos, COMPANY_INFO['postal'])
    y_pos -= 10
    c.drawString(40*mm, y_pos, f"Tel: {COMPANY_INFO['phone']} | E-post: {COMPANY_INFO['email']}")
    y_pos -= 10
    c.drawString(40*mm, y_pos, f"Org.nr: {COMPANY_INFO['org_nr']}")
    
    # Avtalstitel
    y_pos -= 30
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, y_pos, AGREEMENT_TERMS['title'])
    
    # Avtalsnummer och datum
    y_pos -= 20
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, y_pos, f"Avtalsnummer: {agreement_number}")
    y_pos -= 12
    c.drawCentredString(width/2, y_pos, f"Datum: {contract_start.strftime('%Y-%m-%d')}")
    
    # Inledning
    y_pos -= 25
    c.setFont("Helvetica", 10)
    intro_lines = AGREEMENT_TERMS['introduction'].strip().split('\n')
    for line in intro_lines:
        if line.strip():
            c.drawString(40*mm, y_pos, line.strip())
            y_pos -= 12
    
    # Parter
    y_pos -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40*mm, y_pos, "PARTER")
    
    y_pos -= 18
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40*mm, y_pos, "Leverantör:")
    c.setFont("Helvetica", 9)
    y_pos -= 12
    c.drawString(40*mm, y_pos, COMPANY_INFO['name'])
    y_pos -= 10
    c.drawString(40*mm, y_pos, f"Org.nr: {COMPANY_INFO['org_nr']}")
    y_pos -= 10
    c.drawString(40*mm, y_pos, COMPANY_INFO['address'])
    y_pos -= 10
    c.drawString(40*mm, y_pos, COMPANY_INFO['postal'])
    y_pos -= 10
    c.drawString(40*mm, y_pos, f"Tel: {COMPANY_INFO['phone']}")
    y_pos -= 10
    c.drawString(40*mm, y_pos, f"E-post: {COMPANY_INFO['email']}")
    
    y_pos -= 18
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40*mm, y_pos, "Kund:")
    c.setFont("Helvetica", 9)
    y_pos -= 12
    c.drawString(40*mm, y_pos, customer.get('name', 'N/A'))
    if customer.get('company'):
        y_pos -= 10
        c.drawString(40*mm, y_pos, customer.get('company', ''))
    if customer.get('email'):
        y_pos -= 10
        c.drawString(40*mm, y_pos, f"E-post: {customer.get('email', '')}")
    if customer.get('phone'):
        y_pos -= 10
        c.drawString(40*mm, y_pos, f"Tel: {customer.get('phone', '')}")
    
    # Avtalsomfattning
    y_pos -= 25
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40*mm, y_pos, "§1 AVTALETS OMFATTNING")
    
    y_pos -= 15
    c.setFont("Helvetica", 9)
    scope_lines = AGREEMENT_TERMS['scope_section'].strip().split('\n')
    for line in scope_lines:
        if line.strip() and not line.strip().startswith('§1'):
            if y_pos < 50*mm:
                c.showPage()
                y_pos = height - 40*mm
                c.setFont("Helvetica", 9)
            c.drawString(40*mm, y_pos, line.strip())
            y_pos -= 10
    
    # Ny sida för specifikation
    c.showPage()
    y_pos = height - 40*mm
    
    # ===== SIDA 2: SPECIFIKATION OCH PRISER =====
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40*mm, y_pos, "SPECIFIKATION OCH PRISER")
    
    y_pos -= 20
    # Produkter och tjänster tabell
    table_data = [['Beskrivning', 'Antal', 'Pris/st', 'Rabatt', 'Summa']]
    
    for item in items:
        qty = item.get('quantity', 1)
        price = item.get('price', 0)
        discount = item.get('discount', 0)
        item_total = qty * price * (1 - discount/100)
        
        table_data.append([
            item.get('name', ''),
            str(qty),
            f"{price:,.0f} kr",
            f"{discount}%",
            f"{item_total:,.0f} kr"
        ])
    
    t = Table(table_data, colWidths=[80*mm, 20*mm, 25*mm, 20*mm, 25*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    table_height = len(table_data) * 20
    y_pos -= table_height
    t.wrapOn(c, width, height)
    t.drawOn(c, 40*mm, y_pos)
    
    # Totaler
    y_pos -= 25
    c.setFont("Helvetica", 10)
    c.drawString(145*mm, y_pos, f"Summa exkl. moms: {total:,.0f} kr")
    y_pos -= 12
    c.drawString(145*mm, y_pos, f"Moms (25%): {vat:,.0f} kr")
    y_pos -= 12
    c.setFont("Helvetica-Bold", 11)
    c.drawString(145*mm, y_pos, f"TOTALT inkl. moms: {total_with_vat:,.0f} kr")
    
    # Leverans och installation
    y_pos -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40*mm, y_pos, "§2 LEVERANS OCH INSTALLATION")
    
    y_pos -= 15
    c.setFont("Helvetica", 9)
    delivery_text = AGREEMENT_TERMS['delivery_section'].format(
        installation_date=installation_date
    )
    for line in delivery_text.strip().split('\n'):
        if line.strip() and not line.strip().startswith('§2'):
            if y_pos < 50*mm:
                c.showPage()
                y_pos = height - 40*mm
                c.setFont("Helvetica", 9)
            c.drawString(40*mm, y_pos, line.strip())
            y_pos -= 10
    
    # Betalningsvillkor
    y_pos -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40*mm, y_pos, "§3 BETALNINGSVILLKOR")
    
    y_pos -= 15
    c.setFont("Helvetica", 9)
    # Hämta betalningsplan
    payment_plan_text = PAYMENT_PLAN_TEMPLATES.get(payment_plan, PAYMENT_PLAN_TEMPLATES['split_50_50'])
    if 'monthly' in payment_plan.lower():
        payment_plan_text = payment_plan_text.format(
            first_payment_date=(datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
            contract_period=contract_period
        )
    
    payment_text = AGREEMENT_TERMS['payment_section'].format(
        total_amount=f"{total:,.0f}",
        payment_plan=payment_plan_text
    )
    
    for line in payment_text.strip().split('\n'):
        if line.strip() and not line.strip().startswith('§3'):
            if y_pos < 50*mm:
                c.showPage()
                y_pos = height - 40*mm
                c.setFont("Helvetica", 9)
            c.drawString(40*mm, y_pos, line.strip())
            y_pos -= 10
    
    # Ny sida för avtalsvillkor
    c.showPage()
    y_pos = height - 40*mm
    
    # ===== SIDA 3: AVTALSVILLKOR =====
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40*mm, y_pos, "§4 AVTALSTID OCH UPPSÄGNING")
    
    y_pos -= 15
    c.setFont("Helvetica", 9)
    period_text = AGREEMENT_TERMS['contract_period_section'].format(
        contract_start_date=contract_start.strftime('%Y-%m-%d'),
        contract_end_date=contract_end.strftime('%Y-%m-%d'),
        contract_period=contract_period
    )
    
    for line in period_text.strip().split('\n'):
        if line.strip() and not line.strip().startswith('§4'):
            if y_pos < 50*mm:
                c.showPage()
                y_pos = height - 40*mm
                c.setFont("Helvetica", 9)
            c.drawString(40*mm, y_pos, line.strip())
            y_pos -= 10
    
    # Garanti
    y_pos -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40*mm, y_pos, "§5 GARANTI OCH ANSVAR")
    
    y_pos -= 15
    c.setFont("Helvetica", 9)
    warranty_text = AGREEMENT_TERMS['warranty_section'].format(
        warranty_period=WARRANTY_PERIODS.get(warranty_period, WARRANTY_PERIODS['standard'])
    )
    
    for line in warranty_text.strip().split('\n'):
        if line.strip() and not line.strip().startswith('§5'):
            if y_pos < 50*mm:
                c.showPage()
                y_pos = height - 40*mm
                c.setFont("Helvetica", 9)
            c.drawString(40*mm, y_pos, line.strip())
            y_pos -= 10
    
    # Support och underhåll
    y_pos -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40*mm, y_pos, "§6 SUPPORT OCH UNDERHÅLL")
    
    y_pos -= 15
    c.setFont("Helvetica", 9)
    support_text = AGREEMENT_TERMS['support_section'].format(
        company_phone=COMPANY_INFO['phone'],
        company_email=COMPANY_INFO['email']
    )
    
    for line in support_text.strip().split('\n'):
        if line.strip() and not line.strip().startswith('§6'):
            if y_pos < 50*mm:
                c.showPage()
                y_pos = height - 40*mm
                c.setFont("Helvetica", 9)
            c.drawString(40*mm, y_pos, line.strip())
            y_pos -= 10
    
    # Ny sida för övriga villkor
    if y_pos < 150*mm:
        c.showPage()
        y_pos = height - 40*mm
    
    # ===== SIDA 4: ÖVRIGA VILLKOR OCH SIGNATURER =====
    
    # Ändringar och tillägg
    y_pos -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40*mm, y_pos, "§7 ÄNDRINGAR OCH TILLÄGG")
    
    y_pos -= 15
    c.setFont("Helvetica", 9)
    for line in AGREEMENT_TERMS['changes_section'].strip().split('\n'):
        if line.strip() and not line.strip().startswith('§7'):
            c.drawString(40*mm, y_pos, line.strip())
            y_pos -= 10
    
    # Force majeure
    y_pos -= 15
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40*mm, y_pos, "§8 FORCE MAJEURE")
    
    y_pos -= 15
    c.setFont("Helvetica", 9)
    for line in AGREEMENT_TERMS['force_majeure_section'].strip().split('\n'):
        if line.strip() and not line.strip().startswith('§8'):
            c.drawString(40*mm, y_pos, line.strip())
            y_pos -= 10
    
    # Sekretess
    y_pos -= 15
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40*mm, y_pos, "§9 SEKRETESS")
    
    y_pos -= 15
    c.setFont("Helvetica", 9)
    for line in AGREEMENT_TERMS['confidentiality_section'].strip().split('\n'):
        if line.strip() and not line.strip().startswith('§9'):
            c.drawString(40*mm, y_pos, line.strip())
            y_pos -= 10
    
    # Tvister
    y_pos -= 15
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40*mm, y_pos, "§10 TVISTER")
    
    y_pos -= 15
    c.setFont("Helvetica", 9)
    for line in AGREEMENT_TERMS['disputes_section'].strip().split('\n'):
        if line.strip() and not line.strip().startswith('§10'):
            c.drawString(40*mm, y_pos, line.strip())
            y_pos -= 10
    
    # Särskilda villkor
    if special_terms and special_terms != 'Inga särskilda villkor.':
        y_pos -= 15
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40*mm, y_pos, "§11 SÄRSKILDA VILLKOR")
        
        y_pos -= 15
        c.setFont("Helvetica", 9)
        c.drawString(40*mm, y_pos, special_terms)
        y_pos -= 10
    
    # Signaturer - ny sida om inte tillräckligt med plats
    if y_pos < 100*mm:
        c.showPage()
        y_pos = height - 40*mm
    
    y_pos -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40*mm, y_pos, "UNDERSKRIFTER")
    
    y_pos -= 15
    c.setFont("Helvetica", 9)
    c.drawString(40*mm, y_pos, "Detta avtal har upprättats i två exemplar varav parterna tagit var sitt.")
    
    y_pos -= 30
    c.setFont("Helvetica", 9)
    c.drawString(40*mm, y_pos, f"Datum: {contract_start.strftime('%Y-%m-%d')}")
    
    # Signaturområden
    y_pos -= 40
    c.setFont("Helvetica-Bold", 9)
    c.drawString(40*mm, y_pos, f"För {COMPANY_INFO['name']}")
    c.drawString(120*mm, y_pos, f"För {customer.get('company', customer.get('name', 'Kund'))}")
    
    y_pos -= 30
    c.line(40*mm, y_pos, 95*mm, y_pos)
    c.line(120*mm, y_pos, 175*mm, y_pos)
    
    y_pos -= 15
    c.setFont("Helvetica", 8)
    c.drawString(40*mm, y_pos, "Namnförtydligande")
    c.drawString(120*mm, y_pos, customer.get('name', ''))
    
    y_pos -= 20
    c.line(40*mm, y_pos, 95*mm, y_pos)
    c.line(120*mm, y_pos, 175*mm, y_pos)
    
    y_pos -= 15
    c.setFont("Helvetica", 8)
    c.drawString(40*mm, y_pos, "Ort och datum")
    c.drawString(120*mm, y_pos, "Ort och datum")
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer


@app.errorhandler(404)
def not_found(e):
    """Felhantering för 404"""
    logger.warning(f"404 fel: {request.url}")
    return jsonify({'error': 'Resursen kunde inte hittas'}), 404


@app.errorhandler(500)
def internal_error(e):
    """Felhantering för 500"""
    logger.error(f"500 fel: {str(e)}")
    logger.debug(traceback.format_exc())
    return jsonify({'error': 'Ett internt serverfel uppstod'}), 500


@app.errorhandler(Exception)
def handle_exception(e):
    """Generell felhantering"""
    logger.error(f"Ohanterat fel: {str(e)}")
    logger.debug(traceback.format_exc())
    return jsonify({'error': 'Ett oväntat fel uppstod'}), 500


if __name__ == '__main__':
    logger.info("Startar Tretec Quote System Server...")
    
    # Försök skrapa ellås-produkter vid start
    try:
        scrape_ellas_products()
    except Exception as e:
        logger.warning(f"Kunde inte skrapa ellås-produkter vid start: {e}")
    
    # Använd debug=False i produktion för säkerhet
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info("Server redo på http://localhost:5000")
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
