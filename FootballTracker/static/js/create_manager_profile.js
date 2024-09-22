document.addEventListener('DOMContentLoaded', function() {
    var playersModal = document.getElementById('players-modal');
    var selectedPlayers = []; // Csak a kiválasztott játékosok ID-jait tárolja
    var selectedPlayersInput = document.getElementById('selected-players');
    var selectedPlayersList = document.getElementById('selected-players-list');
    var playersList = document.getElementById('players-list');
    var searchBox = document.getElementById('search-box');

    // Játékosok kiválasztásának kezelése
    document.getElementById('select-players-btn').addEventListener('click', function() {
        playersModal.style.display = 'block';
        loadPlayers('');  // Üres keresés, hogy minden játékos megjelenjen a modálban
    });

    document.getElementById('save-players-btn').addEventListener('click', function() {
        selectedPlayersInput.value = selectedPlayers.join(',');
        playersModal.style.display = 'none';

        // Frissítés a kiválasztott játékosok listáján
        selectedPlayersList.innerHTML = '';
        selectedPlayers.forEach(function(playerId) {
            const playerItem = document.createElement('div');
            // Játékos nevének lekérdezése az ID alapján
            fetch(`/get_player_name/?id=` + playerId) // Feltételezve, hogy van egy endpoint a név lekérdezésére
                .then(response => response.json())
                .then(data => {
                    playerItem.textContent = 'Játékos: ' + data.name; // A játékos neve itt jelenik meg
                    selectedPlayersList.appendChild(playerItem);
                });
        });
    });

    // Keresés mező figyelése
    searchBox.addEventListener('input', function() {
        var query = searchBox.value;
        loadPlayers(query);
    });

    // Játékosok betöltése AJAX-szal
    function loadPlayers(query) {
        fetch(`/search_players/?q=` + encodeURIComponent(query))
            .then(response => response.json())
            .then(data => {
                playersList.innerHTML = ''; // Játékos lista törlése
                data.players.forEach(function(player) {
                    var playerItem = document.createElement('div');
                    playerItem.classList.add('player-item');
                    playerItem.textContent = player.first_name + ' ' + player.last_name; // Játékos neve
                    playerItem.dataset.playerId = player.id;

                    // Kiválasztott játékos stílus megváltoztatása
                    playerItem.addEventListener('click', function() {
                        var playerId = this.dataset.playerId;
                        if (selectedPlayers.includes(playerId)) {
                            // Ha már kiválasztottuk, akkor eltávolítjuk a kiválasztást
                            selectedPlayers = selectedPlayers.filter(id => id !== playerId);
                            playerItem.classList.remove('selected'); // Eltávolítjuk a kiemelést
                        } else {
                            // Ha még nincs kiválasztva, hozzáadjuk
                            selectedPlayers.push(playerId); // Csak az ID-t tároljuk
                            playerItem.classList.add('selected'); // Kiemeljük a kiválasztott játékost
                        }
                    });

                    playersList.appendChild(playerItem);
                });
            });
    }

    document.addEventListener('DOMContentLoaded', function () {
        const addPlayerButton = document.getElementById('add-player-button');
        const modal = document.getElementById('add-player-modal');
        const closeButton = document.querySelector('.close-button');
    
        addPlayerButton.addEventListener('click', function () {
            modal.style.display = 'block';
        });
    
        closeButton.addEventListener('click', function () {
            modal.style.display = 'none';
        });
    
        window.addEventListener('click', function (event) {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    });
    
});
