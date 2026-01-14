// Tretec Quote System - Frontend JavaScript

// Global state
let currentQuoteId = null;
let currentCustomerId = null;
let customers = [];
let products = [];
let quotes = [];
let quoteItems = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializePage();
});

function initializePage() {
    // Set default date to today
    document.getElementById('quote-date').valueAsDate = new Date();
    
    // Set default valid until to 30 days from now
    const validUntil = new Date();
    validUntil.setDate(validUntil.getDate() + 30);
    document.getElementById('valid-until').valueAsDate = validUntil;
    
    // Load data
    loadCustomers();
    loadProducts();
    loadQuotesList();
}

// Tab management
function showTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    // Show selected tab
    document.getElementById(tabName + '-tab').classList.add('active');
    
    // Set active button
    event.target.classList.add('active');
    
    // Refresh data when switching to certain tabs
    if (tabName === 'quotes') {
        loadQuotesList();
    } else if (tabName === 'customers') {
        loadCustomersList();
    } else if (tabName === 'products') {
        loadProductsList();
    }
}

// Customer management
async function loadCustomers() {
    try {
        const response = await fetch('/api/customers');
        customers = await response.json();
        
        // Populate customer select
        const select = document.getElementById('customer-select');
        select.innerHTML = '<option value="">-- Välj kund eller skapa ny --</option>';
        
        customers.forEach(customer => {
            const option = document.createElement('option');
            option.value = customer.id;
            option.textContent = customer.name || 'Namnlös kund';
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading customers:', error);
    }
}

function selectCustomer() {
    const select = document.getElementById('customer-select');
    const customerId = select.value;
    
    if (!customerId) {
        document.getElementById('customer-details').style.display = 'none';
        document.getElementById('customer-warnings').innerHTML = '';
        currentCustomerId = null;
        return;
    }
    
    const customer = customers.find(c => c.id === customerId);
    if (!customer) return;
    
    currentCustomerId = customerId;
    
    // Show customer details form
    document.getElementById('customer-details').style.display = 'block';
    
    // Populate form
    document.getElementById('customer-name').value = customer.name || '';
    document.getElementById('customer-org').value = customer.org_number || '';
    document.getElementById('customer-phone').value = customer.phone || '';
    document.getElementById('customer-email').value = customer.email || '';
    document.getElementById('customer-invoice-email').value = customer.invoice_email || '';
    document.getElementById('customer-invoice-address').value = customer.invoice_address || '';
    
    // Check for missing information
    checkCustomerInfo(customer);
}

function checkCustomerInfo(customer) {
    const warnings = [];
    
    if (!customer.name) warnings.push('Namn saknas');
    if (!customer.phone) warnings.push('Telefonnummer saknas');
    if (!customer.invoice_email) warnings.push('Fakturamejl saknas');
    if (!customer.invoice_address) warnings.push('Fakturaadress saknas');
    
    const warningsDiv = document.getElementById('customer-warnings');
    
    if (warnings.length > 0) {
        warningsDiv.innerHTML = `
            <div class="warnings">
                <strong>⚠️ Följande kunduppgifter saknas:</strong>
                ${warnings.map(w => `<div class="warning-item">• ${w}</div>`).join('')}
                <div style="margin-top: 10px;">
                    <small>Dessa kommer att visas som "SAKNAS" i PDF:en. Fyll i uppgifterna nedan och spara.</small>
                </div>
            </div>
        `;
    } else {
        warningsDiv.innerHTML = '<div class="badge badge-success">✓ Alla kunduppgifter är kompletta</div>';
    }
}

function showNewCustomerForm() {
    document.getElementById('customer-select').value = '';
    document.getElementById('customer-details').style.display = 'block';
    document.getElementById('customer-warnings').innerHTML = '';
    currentCustomerId = null;
    
    // Clear form
    document.getElementById('customer-name').value = '';
    document.getElementById('customer-org').value = '';
    document.getElementById('customer-phone').value = '';
    document.getElementById('customer-email').value = '';
    document.getElementById('customer-invoice-email').value = '';
    document.getElementById('customer-invoice-address').value = '';
}

async function saveCurrentCustomer() {
    const customerData = {
        name: document.getElementById('customer-name').value,
        org_number: document.getElementById('customer-org').value,
        phone: document.getElementById('customer-phone').value,
        email: document.getElementById('customer-email').value,
        invoice_email: document.getElementById('customer-invoice-email').value,
        invoice_address: document.getElementById('customer-invoice-address').value
    };
    
    if (!customerData.name) {
        alert('Namn är obligatoriskt');
        return;
    }
    
    try {
        let response;
        if (currentCustomerId) {
            // Update existing customer
            response = await fetch(`/api/customers/${currentCustomerId}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(customerData)
            });
        } else {
            // Create new customer
            response = await fetch('/api/customers', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(customerData)
            });
        }
        
        const customer = await response.json();
        currentCustomerId = customer.id;
        
        alert('Kund sparad!');
        await loadCustomers();
        
        // Select the saved customer
        document.getElementById('customer-select').value = currentCustomerId;
        checkCustomerInfo(customer);
    } catch (error) {
        console.error('Error saving customer:', error);
        alert('Ett fel uppstod när kunden skulle sparas');
    }
}

async function loadCustomersList() {
    await loadCustomers();
    
    const listDiv = document.getElementById('customers-list');
    
    if (customers.length === 0) {
        listDiv.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">👥</div>
                <p>Inga kunder ännu. Lägg till din första kund!</p>
            </div>
        `;
        return;
    }
    
    listDiv.innerHTML = customers.map(customer => {
        const missingFields = [];
        if (!customer.invoice_email) missingFields.push('fakturamejl');
        if (!customer.invoice_address) missingFields.push('fakturaadress');
        if (!customer.phone) missingFields.push('telefon');
        
        const badge = missingFields.length > 0 
            ? `<span class="badge badge-warning">Saknar: ${missingFields.join(', ')}</span>`
            : `<span class="badge badge-success">Komplett</span>`;
        
        return `
            <div class="list-item">
                <div class="list-item-content">
                    <div class="list-item-title">${customer.name || 'Namnlös'}</div>
                    <div class="list-item-details">
                        ${customer.org_number ? `Org.nr: ${customer.org_number} | ` : ''}
                        ${customer.phone || 'Inget telefonnummer'}
                        <br/>
                        ${customer.email || 'Ingen e-post'} | ${badge}
                    </div>
                </div>
                <div class="list-item-actions">
                    <button onclick="editCustomer('${customer.id}')" class="btn btn-secondary">Redigera</button>
                    <button onclick="deleteCustomer('${customer.id}')" class="btn btn-danger">Ta bort</button>
                </div>
            </div>
        `;
    }).join('');
}

function editCustomer(customerId) {
    // Switch to quote tab and select customer
    showTab('quote');
    document.querySelector('.tab-button').click(); // Click first tab to activate it properly
    
    setTimeout(() => {
        document.getElementById('customer-select').value = customerId;
        selectCustomer();
    }, 100);
}

async function deleteCustomer(customerId) {
    if (!confirm('Är du säker på att du vill ta bort denna kund?')) {
        return;
    }
    
    try {
        await fetch(`/api/customers/${customerId}`, { method: 'DELETE' });
        alert('Kund borttagen');
        loadCustomersList();
    } catch (error) {
        console.error('Error deleting customer:', error);
        alert('Ett fel uppstod när kunden skulle tas bort');
    }
}

// Product management
async function loadProducts() {
    try {
        const response = await fetch('/api/products');
        products = await response.json();
        updateProductSelect();
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

function updateProductSelect() {
    const select = document.getElementById('product-select');
    select.innerHTML = '';
    
    products.forEach(product => {
        const option = document.createElement('option');
        option.value = product.id;
        option.textContent = `${product.name} - ${product.price} kr/${product.unit}`;
        option.dataset.product = JSON.stringify(product);
        select.appendChild(option);
    });
}

function searchProducts() {
    const searchTerm = document.getElementById('product-search').value.toLowerCase();
    const select = document.getElementById('product-select');
    
    select.innerHTML = '';
    
    const filtered = products.filter(p => 
        p.name.toLowerCase().includes(searchTerm) ||
        (p.category && p.category.toLowerCase().includes(searchTerm))
    );
    
    filtered.forEach(product => {
        const option = document.createElement('option');
        option.value = product.id;
        option.textContent = `${product.name} - ${product.price} kr/${product.unit}`;
        option.dataset.product = JSON.stringify(product);
        select.appendChild(option);
    });
}

function addProductToQuote() {
    const select = document.getElementById('product-select');
    const selectedOption = select.options[select.selectedIndex];
    
    if (!selectedOption) {
        alert('Välj en produkt först');
        return;
    }
    
    const product = JSON.parse(selectedOption.dataset.product);
    
    quoteItems.push({
        id: product.id,
        name: product.name,
        quantity: 1,
        price: product.price,
        discount: 0
    });
    
    updateQuoteItemsTable();
}

function updateQuoteItemsTable() {
    const tbody = document.getElementById('quote-items');
    
    tbody.innerHTML = quoteItems.map((item, index) => `
        <tr>
            <td>${item.name}</td>
            <td>
                <input type="number" class="quote-item-input" value="${item.quantity}" 
                       min="0" step="0.1" onchange="updateItemQuantity(${index}, this.value)">
            </td>
            <td>${item.price.toLocaleString('sv-SE')} kr</td>
            <td>
                <input type="number" class="quote-item-input" value="${item.discount}" 
                       min="0" max="100" onchange="updateItemDiscount(${index}, this.value)">
            </td>
            <td>${calculateItemTotal(item).toLocaleString('sv-SE')} kr</td>
            <td>
                <button onclick="removeItem(${index})" class="btn btn-danger">×</button>
            </td>
        </tr>
    `).join('');
    
    updateTotals();
}

function updateItemQuantity(index, value) {
    quoteItems[index].quantity = parseFloat(value) || 0;
    updateQuoteItemsTable();
}

function updateItemDiscount(index, value) {
    quoteItems[index].discount = parseFloat(value) || 0;
    updateQuoteItemsTable();
}

function removeItem(index) {
    quoteItems.splice(index, 1);
    updateQuoteItemsTable();
}

function calculateItemTotal(item) {
    return item.quantity * item.price * (1 - item.discount / 100);
}

function updateTotals() {
    const subtotal = quoteItems.reduce((sum, item) => sum + calculateItemTotal(item), 0);
    const vat = subtotal * 0.25;
    const total = subtotal + vat;
    
    document.getElementById('subtotal').textContent = subtotal.toLocaleString('sv-SE') + ' kr';
    document.getElementById('vat').textContent = vat.toLocaleString('sv-SE') + ' kr';
    document.getElementById('total').innerHTML = '<strong>' + total.toLocaleString('sv-SE') + ' kr</strong>';
}

// Quote management
async function saveQuote() {
    if (!currentCustomerId) {
        alert('Välj eller skapa en kund först');
        return;
    }
    
    if (quoteItems.length === 0) {
        alert('Lägg till minst en produkt eller tjänst');
        return;
    }
    
    const customer = customers.find(c => c.id === currentCustomerId);
    
    const quoteData = {
        quote_number: document.getElementById('quote-number').value,
        date: document.getElementById('quote-date').value,
        valid_until: document.getElementById('valid-until').value,
        customer_id: currentCustomerId,
        customer: {
            name: customer.name,
            org_number: customer.org_number,
            phone: customer.phone,
            email: customer.email,
            invoice_email: customer.invoice_email,
            invoice_address: customer.invoice_address
        },
        items: quoteItems,
        notes: document.getElementById('quote-notes').value,
        agreement_text: document.getElementById('agreement-text').value
    };
    
    try {
        let response;
        if (currentQuoteId) {
            // Update existing quote
            response = await fetch(`/api/quotes/${currentQuoteId}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(quoteData)
            });
        } else {
            // Create new quote
            response = await fetch('/api/quotes', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(quoteData)
            });
        }
        
        const quote = await response.json();
        currentQuoteId = quote.id;
        
        alert('Offert sparad!');
        await loadQuotesList();
    } catch (error) {
        console.error('Error saving quote:', error);
        alert('Ett fel uppstod när offerten skulle sparas');
    }
}

async function loadQuotesList() {
    try {
        const response = await fetch('/api/quotes');
        quotes = await response.json();
        
        // Update load quote select
        const select = document.getElementById('load-quote-select');
        select.innerHTML = '<option value="">-- Välj offert --</option>';
        
        quotes.forEach(quote => {
            const option = document.createElement('option');
            option.value = quote.id;
            option.textContent = `${quote.quote_number || quote.id} - ${quote.customer?.name || 'Okänd kund'}`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading quotes:', error);
    }
    
    // Update quotes list tab
    updateQuotesListTab();
}

function updateQuotesListTab() {
    const listDiv = document.getElementById('quotes-list');
    
    if (quotes.length === 0) {
        listDiv.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📄</div>
                <p>Inga sparade offerter ännu. Skapa din första offert!</p>
            </div>
        `;
        return;
    }
    
    listDiv.innerHTML = quotes.map(quote => {
        const total = quote.items.reduce((sum, item) => 
            sum + (item.quantity * item.price * (1 - (item.discount || 0) / 100)), 0) * 1.25;
        
        return `
            <div class="list-item">
                <div class="list-item-content">
                    <div class="list-item-title">Offert ${quote.quote_number || quote.id}</div>
                    <div class="list-item-details">
                        Kund: ${quote.customer?.name || 'Okänd'} | 
                        Datum: ${quote.date || 'N/A'} | 
                        Totalt: ${total.toLocaleString('sv-SE')} kr
                    </div>
                </div>
                <div class="list-item-actions">
                    <button onclick="loadQuote('${quote.id}')" class="btn btn-secondary">Ladda</button>
                    <button onclick="generatePDFForQuote('${quote.id}')" class="btn btn-success">PDF</button>
                    <button onclick="deleteQuote('${quote.id}')" class="btn btn-danger">Ta bort</button>
                </div>
            </div>
        `;
    }).join('');
}

function loadSelectedQuote() {
    const select = document.getElementById('load-quote-select');
    const quoteId = select.value;
    
    if (!quoteId) {
        alert('Välj en offert först');
        return;
    }
    
    loadQuote(quoteId);
}

async function loadQuote(quoteId) {
    try {
        const response = await fetch(`/api/quotes/${quoteId}`);
        const quote = await response.json();
        
        // Set quote ID
        currentQuoteId = quoteId;
        
        // Populate form
        document.getElementById('quote-number').value = quote.quote_number || '';
        document.getElementById('quote-date').value = quote.date || '';
        document.getElementById('valid-until').value = quote.valid_until || '';
        document.getElementById('quote-notes').value = quote.notes || '';
        document.getElementById('agreement-text').value = quote.agreement_text || '';
        
        // Load customer
        if (quote.customer_id) {
            currentCustomerId = quote.customer_id;
            document.getElementById('customer-select').value = quote.customer_id;
            selectCustomer();
        }
        
        // Load items
        quoteItems = quote.items || [];
        updateQuoteItemsTable();
        
        // Switch to quote tab
        const quoteTab = document.querySelector('.tab-button');
        quoteTab.click();
        
        alert('Offert laddad!');
    } catch (error) {
        console.error('Error loading quote:', error);
        alert('Ett fel uppstod när offerten skulle laddas');
    }
}

async function deleteQuote(quoteId) {
    if (!confirm('Är du säker på att du vill ta bort denna offert?')) {
        return;
    }
    
    try {
        await fetch(`/api/quotes/${quoteId}`, { method: 'DELETE' });
        alert('Offert borttagen');
        await loadQuotesList();
        
        if (currentQuoteId === quoteId) {
            clearQuote();
        }
    } catch (error) {
        console.error('Error deleting quote:', error);
        alert('Ett fel uppstod när offerten skulle tas bort');
    }
}

function clearQuote() {
    currentQuoteId = null;
    currentCustomerId = null;
    quoteItems = [];
    
    document.getElementById('quote-number').value = '';
    document.getElementById('quote-notes').value = '';
    document.getElementById('agreement-text').value = '';
    document.getElementById('customer-select').value = '';
    document.getElementById('customer-details').style.display = 'none';
    document.getElementById('customer-warnings').innerHTML = '';
    
    // Reset dates
    document.getElementById('quote-date').valueAsDate = new Date();
    const validUntil = new Date();
    validUntil.setDate(validUntil.getDate() + 30);
    document.getElementById('valid-until').valueAsDate = validUntil;
    
    updateQuoteItemsTable();
}

// PDF generation
async function generatePDF() {
    if (!currentCustomerId) {
        alert('Välj eller skapa en kund först');
        return;
    }
    
    if (quoteItems.length === 0) {
        alert('Lägg till minst en produkt eller tjänst');
        return;
    }
    
    const customer = customers.find(c => c.id === currentCustomerId);
    
    const pdfData = {
        quote_number: document.getElementById('quote-number').value || 'DRAFT',
        date: document.getElementById('quote-date').value,
        valid_until: document.getElementById('valid-until').value,
        customer: {
            name: customer.name,
            org_number: customer.org_number,
            phone: customer.phone,
            email: customer.email,
            invoice_email: customer.invoice_email,
            invoice_address: customer.invoice_address
        },
        items: quoteItems,
        notes: document.getElementById('quote-notes').value,
        agreement_text: document.getElementById('agreement-text').value
    };
    
    try {
        const response = await fetch('/api/generate-pdf', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(pdfData)
        });
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `offert_${pdfData.quote_number}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        alert('PDF genererad och nedladdad!');
    } catch (error) {
        console.error('Error generating PDF:', error);
        alert('Ett fel uppstod när PDF:en skulle genereras');
    }
}

async function generatePDFForQuote(quoteId) {
    try {
        const response = await fetch(`/api/quotes/${quoteId}`);
        const quote = await response.json();
        
        const pdfData = {
            quote_number: quote.quote_number || quote.id,
            date: quote.date,
            valid_until: quote.valid_until,
            customer: quote.customer,
            items: quote.items,
            notes: quote.notes,
            agreement_text: quote.agreement_text
        };
        
        const pdfResponse = await fetch('/api/generate-pdf', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(pdfData)
        });
        
        const blob = await pdfResponse.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `offert_${pdfData.quote_number}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        console.error('Error generating PDF:', error);
        alert('Ett fel uppstod när PDF:en skulle genereras');
    }
}

// Products list
async function loadProductsList() {
    const category = document.getElementById('product-category-filter').value;
    
    try {
        let url = '/api/products';
        if (category) {
            url += `?category=${category}`;
        }
        
        const response = await fetch(url);
        const filteredProducts = await response.json();
        
        const listDiv = document.getElementById('products-list');
        
        if (filteredProducts.length === 0) {
            listDiv.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📦</div>
                    <p>Inga produkter hittades.</p>
                </div>
            `;
            return;
        }
        
        listDiv.innerHTML = filteredProducts.map(product => `
            <div class="list-item">
                <div class="list-item-content">
                    <div class="list-item-title">${product.name}</div>
                    <div class="list-item-details">
                        Kategori: ${product.category || 'N/A'} | 
                        Pris: ${product.price.toLocaleString('sv-SE')} kr/${product.unit}
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

// Modal management
function showNewCustomerModal() {
    document.getElementById('customer-modal').classList.add('show');
}

function closeCustomerModal() {
    document.getElementById('customer-modal').classList.remove('show');
    
    // Clear modal form
    document.getElementById('modal-customer-name').value = '';
    document.getElementById('modal-customer-org').value = '';
    document.getElementById('modal-customer-phone').value = '';
    document.getElementById('modal-customer-email').value = '';
    document.getElementById('modal-customer-invoice-email').value = '';
    document.getElementById('modal-customer-invoice-address').value = '';
}

async function createCustomerFromModal() {
    const customerData = {
        name: document.getElementById('modal-customer-name').value,
        org_number: document.getElementById('modal-customer-org').value,
        phone: document.getElementById('modal-customer-phone').value,
        email: document.getElementById('modal-customer-email').value,
        invoice_email: document.getElementById('modal-customer-invoice-email').value,
        invoice_address: document.getElementById('modal-customer-invoice-address').value
    };
    
    if (!customerData.name) {
        alert('Namn är obligatoriskt');
        return;
    }
    
    try {
        const response = await fetch('/api/customers', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(customerData)
        });
        
        const customer = await response.json();
        
        alert('Kund skapad!');
        closeCustomerModal();
        await loadCustomers();
        await loadCustomersList();
    } catch (error) {
        console.error('Error creating customer:', error);
        alert('Ett fel uppstod när kunden skulle skapas');
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('customer-modal');
    if (event.target == modal) {
        closeCustomerModal();
    }
}
