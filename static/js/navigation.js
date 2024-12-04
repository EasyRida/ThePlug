document.addEventListener('DOMContentLoaded', function() {
    // Handle Learn Skills dropdown
    const learnSkillsBtn = document.querySelector('[data-dropdown="learn-skills"]');
    const learnSkillsMenu = document.querySelector('[data-menu="learn-skills"]');
    
    if (learnSkillsBtn) {
        learnSkillsBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const isVisible = learnSkillsMenu.classList.contains('visible');
            hideAllDropdowns();
            if (!isVisible) {
                learnSkillsMenu.classList.add('visible', 'opacity-100');
                learnSkillsMenu.classList.remove('invisible', 'opacity-0');
            }
        });
    }

    // Handle Find Services dropdown
    const findServicesBtn = document.querySelector('[data-dropdown="find-services"]');
    const findServicesMenu = document.querySelector('[data-menu="find-services"]');
    
    if (findServicesBtn) {
        findServicesBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const isVisible = findServicesMenu.classList.contains('visible');
            hideAllDropdowns();
            if (!isVisible) {
                findServicesMenu.classList.add('visible', 'opacity-100');
                findServicesMenu.classList.remove('invisible', 'opacity-0');
            }
        });
    }

    // Hide dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('[data-dropdown]')) {
            hideAllDropdowns();
        }
    });

    function hideAllDropdowns() {
        const dropdowns = document.querySelectorAll('[data-menu]');
        dropdowns.forEach(dropdown => {
            dropdown.classList.remove('visible', 'opacity-100');
            dropdown.classList.add('invisible', 'opacity-0');
        });
    }
});