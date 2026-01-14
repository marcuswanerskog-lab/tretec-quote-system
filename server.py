#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tretec Quote System Server
Flask-based backend for quote management, customer registry, and PDF generation
"""

from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import json
import os
from datetime import datetime
import uuid
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO

app = Flask(__name__)
CORS(app)

# File paths for JSON storage
CUSTOMERS_FILE = 'customers.json'
QUOTES_FILE = 'quotes.json'
LOGO_PATH = 'Treteclogo.jpg'

# Initialize storage files if they don't exist
def init_storage():
    if not os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
    if not os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=2)

# Customer management
def load_customers():
    try:
        with open(CUSTOMERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_customers(customers):
    with open(CUSTOMERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(customers, f, ensure_ascii=False, indent=2)

# Quote management
def load_quotes():
    try:
        with open(QUOTES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_quotes(quotes):
    with open(QUOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)

# API Endpoints

@app.route('/')
def index():
    return send_file('offertsystem.html')

@app.route('/api/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'GET':
        return jsonify(load_customers())
    elif request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        customers = load_customers()
        customer_id = data.get('id', str(uuid.uuid4()))
        customers[customer_id] = {
            'id': customer_id,
            'name': data.get('name', ''),
            'address': data.get('address', ''),
            'contact': data.get('contact', ''),
            'invoice_email': data.get('invoice_email', ''),
            'invoice_address': data.get('invoice_address', ''),
            'created': data.get('created', datetime.now().isoformat()),
            'updated': datetime.now().isoformat()
        }
        save_customers(customers)
        return jsonify(customers[customer_id])

@app.route('/api/customers/<customer_id>', methods=['GET', 'PUT', 'DELETE'])
def customer(customer_id):
    customers = load_customers()
    
    if request.method == 'GET':
        if customer_id in customers:
            return jsonify(customers[customer_id])
        return jsonify({'error': 'Customer not found'}), 404
    
    elif request.method == 'PUT':
        if customer_id in customers:
            data = request.json
            if not data:
                return jsonify({'error': 'Invalid request data'}), 400
            
            customers[customer_id].update({
                'name': data.get('name', customers[customer_id]['name']),
                'address': data.get('address', customers[customer_id]['address']),
                'contact': data.get('contact', customers[customer_id]['contact']),
                'invoice_email': data.get('invoice_email', customers[customer_id]['invoice_email']),
                'invoice_address': data.get('invoice_address', customers[customer_id]['invoice_address']),
                'updated': datetime.now().isoformat()
            })
            save_customers(customers)
            return jsonify(customers[customer_id])
        return jsonify({'error': 'Customer not found'}), 404
    
    elif request.method == 'DELETE':
        if customer_id in customers:
            del customers[customer_id]
            save_customers(customers)
            return jsonify({'success': True})
        return jsonify({'error': 'Customer not found'}), 404

@app.route('/api/quotes', methods=['GET', 'POST'])
def quotes():
    if request.method == 'GET':
        return jsonify(load_quotes())
    elif request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        quotes = load_quotes()
        quote_id = data.get('id', str(uuid.uuid4()))
        quotes[quote_id] = {
            'id': quote_id,
            'customer_id': data.get('customer_id', ''),
            'items': data.get('items', []),
            'services': data.get('services', []),
            'discount': data.get('discount', 0),
            'notes': data.get('notes', ''),
            'created': data.get('created', datetime.now().isoformat()),
            'updated': datetime.now().isoformat()
        }
        save_quotes(quotes)
        return jsonify(quotes[quote_id])

@app.route('/api/quotes/<quote_id>', methods=['GET', 'PUT', 'DELETE'])
def quote(quote_id):
    quotes = load_quotes()
    
    if request.method == 'GET':
        if quote_id in quotes:
            return jsonify(quotes[quote_id])
        return jsonify({'error': 'Quote not found'}), 404
    
    elif request.method == 'PUT':
        if quote_id in quotes:
            data = request.json
            if not data:
                return jsonify({'error': 'Invalid request data'}), 400
            
            quotes[quote_id].update({
                'customer_id': data.get('customer_id', quotes[quote_id]['customer_id']),
                'items': data.get('items', quotes[quote_id]['items']),
                'services': data.get('services', quotes[quote_id]['services']),
                'discount': data.get('discount', quotes[quote_id]['discount']),
                'notes': data.get('notes', quotes[quote_id]['notes']),
                'updated': datetime.now().isoformat()
            })
            save_quotes(quotes)
            return jsonify(quotes[quote_id])
        return jsonify({'error': 'Quote not found'}), 404
    
    elif request.method == 'DELETE':
        if quote_id in quotes:
            del quotes[quote_id]
            save_quotes(quotes)
            return jsonify({'success': True})
        return jsonify({'error': 'Quote not found'}), 404

@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    # Create PDF in memory
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20*mm, leftMargin=20*mm,
                           topMargin=20*mm, bottomMargin=20*mm)
    
    # Container for PDF elements
    elements = []
    styles = getSampleStyleSheet()
    
    # Add logo if exists
    if os.path.exists(LOGO_PATH):
        try:
            logo = Image(LOGO_PATH, width=50*mm, height=50*mm, kind='proportional')
            elements.append(logo)
            elements.append(Spacer(1, 10*mm))
        except (IOError, OSError):
            # Skip logo if there's an error loading the image
            pass
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#003366'),
        alignment=TA_CENTER
    )
    elements.append(Paragraph('OFFERT', title_style))
    elements.append(Spacer(1, 10*mm))
    
    # Customer information with warnings
    customer_data = data.get('customer', {})
    customer_name = customer_data.get('name', '⚠️ KUNDNAMN SAKNAS')
    customer_address = customer_data.get('address', '⚠️ ADRESS SAKNAS')
    customer_contact = customer_data.get('contact', '⚠️ KONTAKT SAKNAS')
    invoice_email = customer_data.get('invoice_email', '⚠️ FAKTURAMEJL SAKNAS')
    invoice_address = customer_data.get('invoice_address', '⚠️ FAKTURAADRESS SAKNAS')
    
    customer_info = f"""
    <b>Kund:</b> {customer_name}<br/>
    <b>Adress:</b> {customer_address}<br/>
    <b>Kontakt:</b> {customer_contact}<br/>
    <b>Fakturamejl:</b> {invoice_email}<br/>
    <b>Fakturaadress:</b> {invoice_address}<br/>
    """
    elements.append(Paragraph(customer_info, styles['Normal']))
    elements.append(Spacer(1, 10*mm))
    
    # Quote date
    quote_date = datetime.now().strftime('%Y-%m-%d')
    elements.append(Paragraph(f'<b>Datum:</b> {quote_date}', styles['Normal']))
    elements.append(Spacer(1, 10*mm))
    
    # Items table
    items = data.get('items', [])
    if items:
        table_data = [['Produkt', 'Antal', 'Pris', 'Summa']]
        for item in items:
            table_data.append([
                item.get('name', ''),
                str(item.get('quantity', 0)),
                f"{item.get('price', 0):.2f} kr",
                f"{item.get('quantity', 0) * item.get('price', 0):.2f} kr"
            ])
        
        table = Table(table_data, colWidths=[80*mm, 30*mm, 30*mm, 30*mm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 10*mm))
    
    # Total
    total = sum(item.get('quantity', 0) * item.get('price', 0) for item in items)
    discount = data.get('discount', 0)
    final_total = total * (1 - discount / 100)
    
    elements.append(Paragraph(f'<b>Totalt:</b> {total:.2f} kr', styles['Normal']))
    if discount > 0:
        elements.append(Paragraph(f'<b>Rabatt:</b> {discount}%', styles['Normal']))
        elements.append(Paragraph(f'<b>Att betala:</b> {final_total:.2f} kr', styles['Heading2']))
    elements.append(Spacer(1, 10*mm))
    
    # Business agreement if included
    if data.get('include_agreement', False):
        elements.append(Spacer(1, 10*mm))
        elements.append(Paragraph('<b>AFFÄRSAVTAL</b>', styles['Heading2']))
        elements.append(Spacer(1, 5*mm))
        
        agreement_text = load_agreement_template(customer_data)
        for para in agreement_text:
            elements.append(Paragraph(para, styles['Normal']))
            elements.append(Spacer(1, 3*mm))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return send_file(buffer, mimetype='application/pdf', as_attachment=True,
                    download_name=f'offert_{quote_date}.pdf')

def load_agreement_template(customer_data):
    """Load and customize business agreement template"""
    # Check if agreement files exist
    agreement_file = 'kopavtal_avtal.md'
    appendix_file = 'avtal_bilagor.md'
    
    agreement_parts = []
    
    if os.path.exists(agreement_file):
        try:
            with open(agreement_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Replace placeholders with customer data
                content = content.replace('{KUNDNAMN}', customer_data.get('name', '⚠️ KUNDNAMN SAKNAS'))
                content = content.replace('{ADRESS}', customer_data.get('address', '⚠️ ADRESS SAKNAS'))
                content = content.replace('{DATUM}', datetime.now().strftime('%Y-%m-%d'))
                agreement_parts.append(content)
        except (IOError, OSError) as e:
            agreement_parts.append(f'⚠️ AFFÄRSAVTAL: Kunde inte läsa avtalsmall ({e})')
    else:
        agreement_parts.append('⚠️ AFFÄRSAVTAL: Avtalsmall saknas (kopavtal_avtal.md)')
    
    if os.path.exists(appendix_file):
        try:
            with open(appendix_file, 'r', encoding='utf-8') as f:
                content = f.read()
                agreement_parts.append(content)
        except (IOError, OSError) as e:
            agreement_parts.append(f'⚠️ BILAGOR: Kunde inte läsa bilagemall ({e})')
    else:
        agreement_parts.append('⚠️ BILAGOR: Bilagemall saknas (avtal_bilagor.md)')
    
    return agreement_parts

if __name__ == '__main__':
    init_storage()
    print("Starting Tretec Quote System Server...")
    print("Server running on http://localhost:5000")
    # Note: debug=True is for development only. For production, set debug=False
    # and consider using a production WSGI server like gunicorn
    app.run(debug=True, host='0.0.0.0', port=5000)
