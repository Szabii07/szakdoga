document.addEventListener('DOMContentLoaded', function() {
    // Modal és gombok elemek
    var qualificationModal = document.getElementById("qualification-modal");
    var addQualificationBtn = document.getElementById("add-qualification-btn");
    var qualificationClose = document.querySelector(".close[data-modal='qualification-modal']");
    var qualificationForm = document.getElementById("qualification-form");
    var qualificationsDisplay = document.getElementById("qualifications-display");

    // Modal megnyitása
    addQualificationBtn.onclick = function() {
        qualificationModal.style.display = "block";
    }

    // Modal bezárása
    qualificationClose.onclick = function() {
        qualificationModal.style.display = "none";
    }

    // Modal bezárása kattintásra az ablakon kívül
    window.onclick = function(event) {
        if (event.target == qualificationModal) {
            qualificationModal.style.display = "none";
        }
    }

    // Képesítés űrlap beküldése
    qualificationForm.onsubmit = function(event) {
        event.preventDefault();
        var qualification = document.getElementById("qualification").value.trim();
        
        if (qualification) {
            var qualificationItems = qualificationsDisplay.getElementsByClassName("qualification-item");
            if (qualificationItems.length >= 10) {
                alert("Maximum 10 képesítés adható hozzá.");
                return;
            }

            var newQualification = document.createElement("div");
            newQualification.classList.add("qualification-item");
            newQualification.textContent = `Képesítés: ${qualification}`;
            qualificationsDisplay.appendChild(newQualification);

            // űrlap törlése és modal bezárása
            qualificationForm.reset();
            qualificationModal.style.display = "none";
        } else {
            alert("Kérlek töltsd ki a képesítés mezőt.");
        }
    }
});
