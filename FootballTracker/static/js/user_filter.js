document.addEventListener('DOMContentLoaded', function() {
    const userTypeSelect = document.getElementById('user_type');
    const playerFilters = document.getElementById('player-filters');

    userTypeSelect.addEventListener('change', function() {
        if (userTypeSelect.value === 'player') {
            playerFilters.style.display = 'block';
        } else {
            playerFilters.style.display = 'none';
        }
    });
});
