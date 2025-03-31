from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    asset = data.get('asset')
    cost_basis = float(data.get('costBasis', 0))
    amount_held = float(data.get('amountHeld', 0))
    sale_price = float(data.get('salePrice', 0))
    
    # Toggle to include original cost basis (true/false)
    include_cost_basis = data.get('includeCostBasis', False)

    # Basic calculations from your spreadsheet logic:
    # Real cost basis for all shares
    real_cost_basis = cost_basis * amount_held
    # Gross proceeds from sale
    gross_proceeds = sale_price * amount_held
    # Net gains (this simple example: gains = proceeds - cost basis)
    net_gains = gross_proceeds - real_cost_basis

    # Example tax rates (update these as needed)
    short_term_tax_rate = 25 if asset in ['btc', 'tsla', 'sol'] else 0
    long_term_tax_rate = 15 if asset in ['btc', 'tsla', 'sol'] else 0

    # Calculate tax owed and net proceeds for short-term (for demonstration)
    short_term_tax_owed = net_gains * (short_term_tax_rate / 100)
    short_term_net_proceeds = gross_proceeds - short_term_tax_owed

    # Similarly for long-term (if needed)
    long_term_tax_owed = net_gains * (long_term_tax_rate / 100)
    long_term_net_proceeds = gross_proceeds - long_term_tax_owed

    # Calculate break-even price using short-term net proceeds as an example
    if amount_held > 0:
        if include_cost_basis:
            break_even = (short_term_net_proceeds + real_cost_basis) / amount_held
        else:
            break_even = short_term_net_proceeds / amount_held
    else:
        break_even = 0

    results = {
        'shortTerm': {
            'taxRate': short_term_tax_rate,
            'netGains': net_gains,
            'taxOwed': short_term_tax_owed,
            'netProceeds': short_term_net_proceeds
        },
        'longTerm': {
            'taxRate': long_term_tax_rate,
            'netGains': net_gains,
            'taxOwed': long_term_tax_owed,
            'netProceeds': long_term_net_proceeds
        },
        'breakEven': break_even,
        'includeCostBasis': include_cost_basis
    }
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
