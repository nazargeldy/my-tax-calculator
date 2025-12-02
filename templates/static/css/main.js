// static/js/main.js

// Set footer year
document.addEventListener("DOMContentLoaded", function () {
  const y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
});

function calculate(asset) {
  // Read inputs
  const costBasis       = parseFloat(document.getElementById(`costBasis-${asset}`).value) || 0;
  const amountHeld      = parseFloat(document.getElementById(`amountHeld-${asset}`).value) || 0;
  const salePrice       = parseFloat(document.getElementById(`salePrice-${asset}`).value) || 0;
  const includeCostBase = document.getElementById(`includeCostBasis-${asset}`).checked;

  if (!amountHeld || !salePrice) {
    alert("Please enter at least Amount Held and Sale Price.");
    return;
  }

  // ----- SIMPLE TAX LOGIC (replace with your own if you want) -----
  // Proceeds from the sale
  const proceeds = salePrice * amountHeld;

  // Cost basis: either 0, or the full number user entered
  const basis    = includeCostBase ? costBasis : 0;

  // Capital gain
  const gain     = proceeds - basis;

  // Example tax rates (you can adjust)
  const shortTermTaxRate = 37;   // %
  const longTermTaxRate  = 20;   // %

  // Short-term
  const shortNetGains    = gain;
  const shortTaxOwed     = shortNetGains * (shortTermTaxRate / 100);
  const shortNetProceeds = proceeds - shortTaxOwed;

  // Long-term
  const longNetGains     = gain;
  const longTaxOwed      = longNetGains * (longTermTaxRate / 100);
  const longNetProceeds  = proceeds - longTaxOwed;

  // Break-even sale price per unit
  const breakEven        = amountHeld ? basis / amountHeld : 0;
  // ----------------------------------------------------------------

  const data = {
    shortTerm: {
      taxRate: shortTermTaxRate,
      netGains: shortNetGains,
      taxOwed: shortTaxOwed,
      netProceeds: shortNetProceeds
    },
    longTerm: {
      taxRate: longTermTaxRate,
      netGains: longNetGains,
      taxOwed: longTaxOwed,
      netProceeds: longNetProceeds
    },
    breakEven: breakEven,
    includeCostBasis: includeCostBase
  };

  // Inject result HTML
  const el = document.getElementById(`result-${asset}`);
  el.innerHTML = `
    <h5 class="mb-2">Short-Term Gains</h5>
    <div class="row no-gutters mb-2">
      <div class="col-6">Tax Rate</div><div class="col-6 text-right"><strong>${data.shortTerm.taxRate}%</strong></div>
      <div class="col-6">Net Gains</div><div class="col-6 text-right">$${data.shortTerm.netGains.toFixed(2)}</div>
      <div class="col-6">Tax Owed</div><div class="col-6 text-right">$${data.shortTerm.taxOwed.toFixed(2)}</div>
      <div class="col-6">Net Proceeds</div><div class="col-6 text-right">$${data.shortTerm.netProceeds.toFixed(2)}</div>
    </div>
    <hr class="my-2">
    <h5 class="mb-2">Long-Term Gains</h5>
    <div class="row no-gutters mb-2">
      <div class="col-6">Tax Rate</div><div class="col-6 text-right"><strong>${data.longTerm.taxRate}%</strong></div>
      <div class="col-6">Net Gains</div><div class="col-6 text-right">$${data.longTerm.netGains.toFixed(2)}</div>
      <div class="col-6">Tax Owed</div><div class="col-6 text-right">$${data.longTerm.taxOwed.toFixed(2)}</div>
      <div class="col-6">Net Proceeds</div><div class="col-6 text-right">$${data.longTerm.netProceeds.toFixed(2)}</div>
    </div>
    <hr class="my-2">
    <h5 class="mb-2">Break-Even Price</h5>
    <p class="lead mb-1">$${data.breakEven.toFixed(2)}</p>
    <p class="mb-0"><small>Included Original Cost Basis: ${data.includeCostBasis}</small></p>
  `;
}
