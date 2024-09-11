document.addEventListener('DOMContentLoaded', function() {
    var positionsModal = document.getElementById('positions-modal');
    var experienceModal = document.getElementById('experience-modal');
    
    document.getElementById('select-positions-btn').addEventListener('click', function() {
        positionsModal.style.display = 'block';
    });
    
    document.querySelectorAll('#positions-modal .close').forEach(function(element) {
        element.addEventListener('click', function() {
            positionsModal.style.display = 'none';
        });
    });
    
    document.getElementById('positions-form').addEventListener('submit', function(event) {
        event.preventDefault();
        
        var selectedPositions = [];
        document.querySelectorAll('#positions-form input[type="checkbox"]:checked').forEach(function(checkbox) {
            selectedPositions.push(checkbox.value);
        });
        
        document.getElementById('position-input').value = selectedPositions.join(',');
        document.getElementById('positions-list').innerText = selectedPositions.length > 0 ? selectedPositions.join(', ') : 'Nincs kiválasztva';
        
        positionsModal.style.display = 'none';
    });
    
    document.getElementById('add-experience-btn').addEventListener('click', function() {
        experienceModal.style.display = 'block';
    });
    
    document.querySelectorAll('#experience-modal .close').forEach(function(element) {
        element.addEventListener('click', function() {
            experienceModal.style.display = 'none';
        });
    });
    
    document.getElementById('experience-form').addEventListener('submit', function(event) {
        event.preventDefault();
        
        var title = document.getElementById('experience-title').value;
        var description = document.getElementById('experience-description').value;
        
        if (title && description) {
            var experienceList = document.getElementById('experience-list');
            
            var li = document.createElement('li');
            li.innerText = `${title}: ${description}`;
            
            var titlesInput = document.getElementById('experience-titles');
            var descriptionsInput = document.getElementById('experience-descriptions');
            
            titlesInput.value += title + ',';
            descriptionsInput.value += description + ',';
            
            experienceList.appendChild(li);
            
            experienceModal.style.display = 'none';
        } else {
            alert('Kérlek töltsd ki mindkét mezőt!');
        }
    });
});
