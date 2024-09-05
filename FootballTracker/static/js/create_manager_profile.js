document.addEventListener('DOMContentLoaded', function() {
    var selectPlayersBtn = document.getElementById("select-players-btn");
    var playersModal = document.getElementById("players-modal");
    var closeModal = document.querySelector(".modal .close");
    var playersList = document.getElementById("players-list");
    var savePlayersBtn = document.getElementById("save-players-btn");
    var selectedPlayersInput = document.getElementById("selected-players");

    // Modal megjelenítése
    selectPlayersBtn.onclick = function() {
        playersModal.style.display = "block";
        loadPlayers();
    }

    // Modal bezárása
    closeModal.onclick = function() {
        playersModal.style.display = "none";
    }

    // Modal bezárása kattintásra kívül
    window.onclick = function(event) {
        if (event.target == playersModal) {
            playersModal.style.display = "none";
        }
    }

    // Játékosok betöltése a backendből
    function loadPlayers() {
        fetch('/players/') // Ez az URL az API végpont, ahol a játékosok adatokat kapjuk
            .then(response => response.json())
            .then(data => {
                playersList.innerHTML = ''; // Ürítse ki az előző listát
                data.forEach(player => {
                    var div = document.createElement('div');
                    var checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.value = player.id;
                    checkbox.id = 'player-' + player.id;

                    var label = document.createElement('label');
                    label.htmlFor = 'player-' + player.id;
                    label.textContent = player.username;

                    div.appendChild(checkbox);
                    div.appendChild(label);
                    playersList.appendChild(div);
                });
            });
    }

    // Kiválasztott játékosok mentése
    savePlayersBtn.onclick = function() {
        var selectedPlayers = Array.from(document.querySelectorAll('#players-list input[type="checkbox"]:checked'))
            .map(checkbox => checkbox.value);
        selectedPlayersInput.value = selectedPlayers.join(',');
        playersModal.style.display = "none";
    }
});
