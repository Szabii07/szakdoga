document.addEventListener('DOMContentLoaded', function() {
    const followForms = document.querySelectorAll('.follow-form');

    followForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const button = form.querySelector('button');
            const isFollowing = button.dataset.followStatus === 'true';
            const url = form.action;

            fetch(url, {
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
                    button.dataset.followStatus = !isFollowing;
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
