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
    
    # Example calculation logic (adjust these formulas to your spreadsheet logic)
    real_cost_basis = cost_basis * amount_held
    gross_proceeds = sale_price * amount_held
    net_gains = gross_proceeds - real_cost_basis

    # Example tax rates for demonstration
    short_term_tax_rate = 25 if asset in ['btc', 'tsla', 'sol'] else 0
    long_term_tax_rate = 15 if asset in ['btc', 'tsla', 'sol'] else 0

    short_term_tax_owed = net_gains * (short_term_tax_rate / 100)
    short_term_net_proceeds = gross_proceeds - short_term_tax_owed

    long_term_tax_owed = net_gains * (long_term_tax_rate / 100)
    long_term_net_proceeds = gross_proceeds - long_term_tax_owed

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
        }
    }
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
