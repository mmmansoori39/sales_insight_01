document.addEventListener('DOMContentLoaded', function() {
  // Load saved settings (if any)
  const savedDateRange = localStorage.getItem('dateRange');
  const savedCurrency = localStorage.getItem('currency');
  const savedTooltips = localStorage.getItem('tooltips');

  if (savedDateRange) {
    document.getElementById('dateRange').value = savedDateRange;
  }

  if (savedCurrency) {
    document.getElementById('currency').value = savedCurrency;
  }

  if (savedTooltips === 'enabled') {
    document.getElementById('tooltips').checked = true;
  }

  // Event listener for save button
  document.getElementById('saveSettings').addEventListener('click', function() {
    const selectedDateRange = document.getElementById('dateRange').value;
    const selectedCurrency = document.getElementById('currency').value;
    const tooltipsEnabled = document.getElementById('tooltips').checked;

    // Save settings to localStorage
    localStorage.setItem('dateRange', selectedDateRange);
    localStorage.setItem('currency', selectedCurrency);
    localStorage.setItem('tooltips', tooltipsEnabled ? 'enabled' : 'disabled');

    alert('Settings saved!');
  });
});
