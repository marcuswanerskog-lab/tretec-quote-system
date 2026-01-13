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
from reportlab.platypus import Table, TableStyle
import requests
from bs4 import BeautifulSoup
import io
import logging
from datetime import datetime
import traceback

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
                    price = int(''.join(filter(str.isdigit, price_text)))
                    
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
        data = request.json
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
    """Generera PDF för affärsavtal med samma layout som offert"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Företagslogga och header (samma som offert)
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
    
    # Avtalstitel
    y_position -= 25
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40*mm, y_position, "AFFÄRSAVTAL")
    
    # Kundinformation (samma som offert)
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
    c.drawString(40*mm, y_position - 12, f"Avtalsnummer: {data.get('agreement_number', 'N/A')}")
    
    # Produkter och tjänster tabell (samma layout som offert)
    y_position -= 25
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40*mm, y_position, "Avtalsspecifikation:")
    
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
    
    # Rita tabell (samma stil som offert)
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
    
    # Totalt (samma som offert)
    y_position -= 25
    c.setFont("Helvetica-Bold", 12)
    c.drawString(145*mm, y_position, f"Totalt: {total:,.0f} kr")
    
    # Moms
    y_position -= 15
    c.setFont("Helvetica", 10)
    vat = total * 0.25
    c.drawString(145*mm, y_position, f"Varav moms (25%): {vat:,.0f} kr")
    
    # Avtalsvillkor (skillnad mot offert)
    y_position -= 25
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40*mm, y_position, "Avtalsvillkor:")
    c.setFont("Helvetica", 9)
    y_position -= 12
    c.drawString(40*mm, y_position, f"Avtalsperiod: {data.get('contract_period', '12 månader')}")
    y_position -= 10
    c.drawString(40*mm, y_position, "Betalningsvillkor: 30 dagar netto.")
    y_position -= 10
    c.drawString(40*mm, y_position, "Uppsägningstid: 3 månader.")
    
    # Signaturer
    y_position -= 30
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40*mm, y_position, "För Tretec Larm AB")
    c.drawString(120*mm, y_position, "För kund")
    
    y_position -= 25
    c.line(40*mm, y_position, 90*mm, y_position)
    c.line(120*mm, y_position, 170*mm, y_position)
    
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
