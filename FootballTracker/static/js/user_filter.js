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

    const followButtons = document.querySelectorAll('.follow-btn');

    followButtons.forEach(button => {
        button.addEventListener('click', function() {
            const isFollowing = button.dataset.followed === 'true';
            const userId = button.dataset.userId;

            fetch(`/follow_user/${userId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ follow: !isFollowing })
            })
            .then(response => {
                if (response.ok) {
                    button.textContent = isFollowing ? 'Követés' : 'Kikövetés';
                    button.dataset.followed = !isFollowing;
                    button.classList.toggle('follow-btn');
                    button.classList.toggle('unfollow-btn');
                } else {
                    alert('Hiba történt. Kérlek próbáld újra.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});
