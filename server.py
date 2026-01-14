#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tretec Quote System Server
Flask-based backend for quote management, customer database, and PDF generation
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
import os
from datetime import datetime
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

app = Flask(__name__)
CORS(app)

# File paths for data storage
CUSTOMERS_FILE = 'customers.json'
QUOTES_FILE = 'quotes.json'
PRODUCTS_FILE = 'products.json'

# Initialize data files if they don't exist
def init_data_files():
    if not os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    
    if not os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    
    if not os.path.exists(PRODUCTS_FILE):
        # Initialize with some default products
        default_products = [
            {
                "id": "prod_001",
                "name": "Larmsystem Basic",
                "category": "Larm",
                "price": 5000,
                "unit": "st"
            },
            {
                "id": "prod_002",
                "name": "Larmsystem Premium",
                "category": "Larm",
                "price": 12000,
                "unit": "st"
            },
            {
                "id": "prod_003",
                "name": "Överfallslarm",
                "category": "Larm",
                "price": 3500,
                "unit": "st"
            },
            {
                "id": "prod_004",
                "name": "Installation",
                "category": "Tjänst",
                "price": 850,
                "unit": "timme"
            },
            {
                "id": "prod_005",
                "name": "Service",
                "category": "Tjänst",
                "price": 750,
                "unit": "timme"
            }
        ]
        with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_products, f, ensure_ascii=False, indent=2)

# Helper functions for data management
def load_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Customer endpoints
@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = load_json(CUSTOMERS_FILE)
    return jsonify(customers)

@app.route('/api/customers', methods=['POST'])
def create_customer():
    customer = request.json
    customers = load_json(CUSTOMERS_FILE)
    
    # Generate ID if not provided
    if 'id' not in customer:
        customer['id'] = f"cust_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    customer['created_at'] = datetime.now().isoformat()
    customer['updated_at'] = datetime.now().isoformat()
    
    customers.append(customer)
    save_json(CUSTOMERS_FILE, customers)
    
    return jsonify(customer), 201

@app.route('/api/customers/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    customers = load_json(CUSTOMERS_FILE)
    customer = next((c for c in customers if c['id'] == customer_id), None)
    
    if customer:
        return jsonify(customer)
    return jsonify({'error': 'Customer not found'}), 404

@app.route('/api/customers/<customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customers = load_json(CUSTOMERS_FILE)
    customer_index = next((i for i, c in enumerate(customers) if c['id'] == customer_id), None)
    
    if customer_index is not None:
        updated_customer = request.json
        updated_customer['id'] = customer_id
        updated_customer['updated_at'] = datetime.now().isoformat()
        
        # Preserve created_at if it exists
        if 'created_at' in customers[customer_index]:
            updated_customer['created_at'] = customers[customer_index]['created_at']
        
        customers[customer_index] = updated_customer
        save_json(CUSTOMERS_FILE, customers)
        
        return jsonify(updated_customer)
    return jsonify({'error': 'Customer not found'}), 404

@app.route('/api/customers/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customers = load_json(CUSTOMERS_FILE)
    customers = [c for c in customers if c['id'] != customer_id]
    save_json(CUSTOMERS_FILE, customers)
    
    return jsonify({'message': 'Customer deleted'}), 200

# Quote endpoints
@app.route('/api/quotes', methods=['GET'])
def get_quotes():
    quotes = load_json(QUOTES_FILE)
    return jsonify(quotes)

@app.route('/api/quotes', methods=['POST'])
def create_quote():
    quote = request.json
    quotes = load_json(QUOTES_FILE)
    
    # Generate ID if not provided
    if 'id' not in quote:
        quote['id'] = f"quote_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    quote['created_at'] = datetime.now().isoformat()
    quote['updated_at'] = datetime.now().isoformat()
    
    quotes.append(quote)
    save_json(QUOTES_FILE, quotes)
    
    return jsonify(quote), 201

@app.route('/api/quotes/<quote_id>', methods=['GET'])
def get_quote(quote_id):
    quotes = load_json(QUOTES_FILE)
    quote = next((q for q in quotes if q['id'] == quote_id), None)
    
    if quote:
        return jsonify(quote)
    return jsonify({'error': 'Quote not found'}), 404

@app.route('/api/quotes/<quote_id>', methods=['PUT'])
def update_quote(quote_id):
    quotes = load_json(QUOTES_FILE)
    quote_index = next((i for i, q in enumerate(quotes) if q['id'] == quote_id), None)
    
    if quote_index is not None:
        updated_quote = request.json
        updated_quote['id'] = quote_id
        updated_quote['updated_at'] = datetime.now().isoformat()
        
        # Preserve created_at if it exists
        if 'created_at' in quotes[quote_index]:
            updated_quote['created_at'] = quotes[quote_index]['created_at']
        
        quotes[quote_index] = updated_quote
        save_json(QUOTES_FILE, quotes)
        
        return jsonify(updated_quote)
    return jsonify({'error': 'Quote not found'}), 404

@app.route('/api/quotes/<quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    quotes = load_json(QUOTES_FILE)
    quotes = [q for q in quotes if q['id'] != quote_id]
    save_json(QUOTES_FILE, quotes)
    
    return jsonify({'message': 'Quote deleted'}), 200

# Product endpoints
@app.route('/api/products', methods=['GET'])
def get_products():
    products = load_json(PRODUCTS_FILE)
    
    # Filter by category if provided
    category = request.args.get('category')
    if category:
        products = [p for p in products if p.get('category') == category]
    
    # Search by name if provided
    search = request.args.get('search')
    if search:
        search_lower = search.lower()
        products = [p for p in products if search_lower in p.get('name', '').lower()]
    
    return jsonify(products)

@app.route('/api/products', methods=['POST'])
def create_product():
    product = request.json
    products = load_json(PRODUCTS_FILE)
    
    # Generate ID if not provided
    if 'id' not in product:
        product['id'] = f"prod_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    products.append(product)
    save_json(PRODUCTS_FILE, products)
    
    return jsonify(product), 201

# PDF Generation endpoint
@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    
    # Create PDF in memory
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                          rightMargin=20*mm, leftMargin=20*mm,
                          topMargin=20*mm, bottomMargin=20*mm)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    normal_style = styles['Normal']
    
    # Add logo if exists
    logo_path = 'Treteclogo.jpg'
    if os.path.exists(logo_path):
        try:
            img = Image(logo_path, width=60*mm, height=30*mm)
            img.hAlign = 'CENTER'
            elements.append(img)
            elements.append(Spacer(1, 12))
        except:
            pass
    
    # Add company header
    elements.append(Paragraph("OFFERT", title_style))
    elements.append(Spacer(1, 12))
    
    # Company info
    company_info = """
    <b>Tretec Larm AB</b><br/>
    Organisationsnummer: XXX-XXXXXX<br/>
    Telefon: XXX-XXXXXXX<br/>
    E-post: info@treteclarm.se
    """
    elements.append(Paragraph(company_info, normal_style))
    elements.append(Spacer(1, 12))
    
    # Quote metadata
    quote_date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    quote_number = data.get('quote_number', 'N/A')
    valid_until = data.get('valid_until', '')
    
    metadata_text = f"""
    <b>Offert nummer:</b> {quote_number}<br/>
    <b>Datum:</b> {quote_date}<br/>
    <b>Giltig till:</b> {valid_until}
    """
    elements.append(Paragraph(metadata_text, normal_style))
    elements.append(Spacer(1, 20))
    
    # Customer information
    customer = data.get('customer', {})
    elements.append(Paragraph("Kunduppgifter", heading_style))
    
    # Check for missing customer information
    missing_info = []
    if not customer.get('name'):
        missing_info.append('Namn')
    if not customer.get('invoice_email'):
        missing_info.append('Fakturamejl')
    if not customer.get('invoice_address'):
        missing_info.append('Fakturaadress')
    if not customer.get('phone'):
        missing_info.append('Telefonnummer')
    
    customer_text = f"""
    <b>Namn:</b> {customer.get('name', '<font color="red">SAKNAS</font>')}<br/>
    <b>Organisationsnummer:</b> {customer.get('org_number', 'N/A')}<br/>
    <b>Telefon:</b> {customer.get('phone', '<font color="red">SAKNAS</font>')}<br/>
    <b>E-post:</b> {customer.get('email', 'N/A')}<br/>
    <b>Fakturamejl:</b> {customer.get('invoice_email', '<font color="red">SAKNAS</font>')}<br/>
    <b>Fakturaadress:</b> {customer.get('invoice_address', '<font color="red">SAKNAS</font>')}
    """
    
    if missing_info:
        customer_text += f'<br/><br/><b><font color="red">OBS! Följande uppgifter saknas: {", ".join(missing_info)}</font></b>'
    
    elements.append(Paragraph(customer_text, normal_style))
    elements.append(Spacer(1, 20))
    
    # Products/Services table
    elements.append(Paragraph("Produkter och tjänster", heading_style))
    
    items = data.get('items', [])
    if items:
        # Table header
        table_data = [['Produkt/Tjänst', 'Antal', 'Á-pris', 'Rabatt', 'Summa']]
        
        subtotal = 0
        for item in items:
            name = item.get('name', '')
            quantity = item.get('quantity', 0)
            price = item.get('price', 0)
            discount = item.get('discount', 0)
            
            item_total = quantity * price * (1 - discount / 100)
            subtotal += item_total
            
            table_data.append([
                name,
                str(quantity),
                f"{price:,.0f} kr",
                f"{discount}%" if discount > 0 else "-",
                f"{item_total:,.0f} kr"
            ])
        
        # Add totals
        vat_amount = subtotal * 0.25
        total = subtotal + vat_amount
        
        table_data.append(['', '', '', 'Summa exkl. moms:', f"{subtotal:,.0f} kr"])
        table_data.append(['', '', '', 'Moms (25%):', f"{vat_amount:,.0f} kr"])
        table_data.append(['', '', '', 'Totalt inkl. moms:', f"{total:,.0f} kr"])
        
        # Create table
        table = Table(table_data, colWidths=[80*mm, 20*mm, 25*mm, 25*mm, 30*mm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -4), colors.beige),
            ('GRID', (0, 0), (-1, -4), 1, colors.black),
            ('LINEBELOW', (0, -3), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
    
    # Notes/Comments
    notes = data.get('notes', '')
    if notes:
        elements.append(Paragraph("Anteckningar", heading_style))
        elements.append(Paragraph(notes, normal_style))
        elements.append(Spacer(1, 20))
    
    # Business agreement section
    elements.append(Paragraph("Affärsavtal", heading_style))
    
    # Use custom agreement text if provided, otherwise use default
    agreement_text = data.get('agreement_text', '')
    if not agreement_text:
        agreement_text = """
        Denna offert är giltig i 30 dagar från offertdatum. Priser är angivna i svenska kronor exklusive moms där annat inte anges.
        <br/><br/>
        <b>Betalningsvillkor:</b> 30 dagar netto<br/>
        <b>Leveransvillkor:</b> Enligt överenskommelse<br/>
        <b>Garanti:</b> 12 månader från leverans
        <br/><br/>
        Installation och service utförs av behöriga tekniker. Alla produkter uppfyller gällande säkerhetsstandarder.
        <br/><br/>
        Vid accept av denna offert vänligen signera och returnera en kopia.
        """
    
    elements.append(Paragraph(agreement_text, normal_style))
    elements.append(Spacer(1, 30))
    
    # Signature section
    signature_text = """
    <br/><br/>
    _________________________<br/>
    Underskrift<br/><br/>
    _________________________<br/>
    Namnförtydligande<br/><br/>
    _________________________<br/>
    Datum
    """
    elements.append(Paragraph(signature_text, normal_style))
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Return PDF
    return send_file(
        io.BytesIO(pdf),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'offert_{quote_number}.pdf'
    )

# Main route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_data_files()
    print("Tretec Quote System Server")
    print("Starting server on http://localhost:5000")
    print("NOTE: For production use, set debug=False and use a production WSGI server like Gunicorn")
    app.run(debug=False, host='0.0.0.0', port=5000)
