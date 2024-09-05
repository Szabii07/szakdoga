document.getElementById('select-positions-btn').addEventListener('click', function() {
    document.getElementById('positions-modal').style.display = 'block';
});

document.querySelector('.close').addEventListener('click', function() {
    document.getElementById('positions-modal').style.display = 'none';
});

document.getElementById('positions-form').addEventListener('submit', function(e) {
    e.preventDefault();

    var selectedPositions = [];
    var checkboxes = document.querySelectorAll('#positions-form input[type="checkbox"]:checked');
    checkboxes.forEach(function(checkbox) {
        selectedPositions.push(checkbox.value);
    });

    document.getElementById('position-input').value = selectedPositions.join(',');
    document.getElementById('positions-list').textContent = selectedPositions.join(', ');

    document.getElementById('positions-modal').style.display = 'none';
});
