document.addEventListener('DOMContentLoaded', function () {
    const maxExperiences = 10;
    let experienceCount = 0;
    const experienceList = document.getElementById('experience-list');
    const addExperienceButton = document.getElementById('add-experience');

    addExperienceButton.addEventListener('click', function () {
        if (experienceCount >= maxExperiences) {
            alert('Maximális tapasztalat számláló elérve!');
            return;
        }

        experienceCount++;
        const experienceEntry = document.createElement('div');
        experienceEntry.className = 'experience-entry';
        experienceEntry.innerHTML = `
            <div class="form-group">
                <label for="experience-title-${experienceCount}">Csapat</label>
                <input type="text" id="experience-title-${experienceCount}" name="experience_title_${experienceCount}" required>
            </div>
            <div class="form-group">
                <label for="experience-description-${experienceCount}">Elért eredmény</label>
                <textarea id="experience-description-${experienceCount}" name="experience_description_${experienceCount}" rows="4" required></textarea>
            </div>
        `;
        experienceList.appendChild(experienceEntry);
    });
});
