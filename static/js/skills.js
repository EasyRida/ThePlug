document.addEventListener('DOMContentLoaded', function() {
    // Filter form handling
    const filterForm = document.getElementById('filter-form');
    const searchInput = document.getElementById('search-input');
    const categoryFilters = document.querySelectorAll('[data-filter="category"]');
    const priceRange = document.getElementById('price-range');
    const priceDisplay = document.getElementById('price-display');
    
    // Update price display
    if (priceRange && priceDisplay) {
        priceRange.addEventListener('input', (e) => {
            priceDisplay.textContent = `R${e.target.value}`;
        });
    }

    // Handle category filter clicks
    categoryFilters.forEach(filter => {
        filter.addEventListener('click', () => {
            filter.classList.toggle('active');
            applyFilters();
        });
    });

    // Debounced search
    let searchTimeout;
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                applyFilters();
            }, 300);
        });
    }

    // Apply filters
    function applyFilters() {
        if (filterForm) {
            filterForm.submit();
        }
    }

    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(tooltip => {
        tippy(tooltip, {
            content: tooltip.getAttribute('data-tooltip'),
            placement: 'top',
            animation: 'scale',
        });
    });
});