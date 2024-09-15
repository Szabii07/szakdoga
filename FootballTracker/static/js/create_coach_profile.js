document.addEventListener('DOMContentLoaded', function() {
    const addQualificationBtn = document.getElementById('add-qualification-btn');
    const qualificationInput = document.getElementById('qualification');
    const qualificationsList = document.getElementById('qualifications-list');
    const qualificationsInput = document.getElementById('qualifications-input');

    // Képesítések hozzáadása
    addQualificationBtn.addEventListener('click', function() {
        const qualification = qualificationInput.value.trim();
        if (qualification) {
            // Új képesítés hozzáadása a listához
            const listItem = document.createElement('li');
            listItem.className = 'qualification-item'; // Stílus osztály hozzáadása
            listItem.textContent = qualification;

            // Eltávolító gomb
            const removeBtn = document.createElement('button');
            removeBtn.textContent = "×";
            removeBtn.className = 'remove-btn'; // Stílus osztály hozzáadása
            removeBtn.onclick = function() {
                listItem.remove();
                updateQualificationsInput();
            };

            listItem.appendChild(removeBtn);
            qualificationsList.appendChild(listItem);

            // Töröljük a bemeneti mezőt
            qualificationInput.value = '';
            updateQualificationsInput();
        }
    });

    function updateQualificationsInput() {
        const qualifications = Array.from(qualificationsList.querySelectorAll('li'))
                                    .map(li => li.textContent.replace('×', '').trim());
        qualificationsInput.value = qualifications.join(',');
    }
});
