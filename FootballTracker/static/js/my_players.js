$(document).ready(function() {
    // Handle note form submission
    $('.noteForm').on('submit', function(e) {
        e.preventDefault();
        
        const $form = $(this);
        
        $.ajax({
            type: 'POST',
            url: $form.attr('action'),
            data: $form.serialize(),
            success: function(response) {
                const noteHTML = `
                    <div class="note-item" id="note-${response.note_id}">
                        <p>${response.note}</p>
                        <button class="delete-note-btn" data-note-id="${response.note_id}">Törlés</button>
                    </div>
                `;
                $form.closest('li').find('.commentsSection').append(noteHTML);
                $form.find('.comment-input').val('');
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });

    // Handle note deletion
    $(document).on('click', '.delete-note-btn', function() {
        const noteId = $(this).data('note-id');
        
        $.ajax({
            type: 'POST',
            url: '/delete-note/' + noteId + '/',
            data: {
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                $('#note-' + noteId).remove(); // Remove note from UI
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
    // Modal functionality
    const modal = document.getElementById("add-player-modal");
    const addPlayerButton = document.getElementById("add-player-button");
    const closeButton = document.querySelector(".close-button");

    addPlayerButton.addEventListener("click", function() {
        modal.style.display = "block";
    });

    closeButton.addEventListener("click", function() {
        modal.style.display = "none";
    });

    window.addEventListener("click", function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    $(document).ready(function() {
        $('.toggle-comments-btn').on('click', function() {
            const commentsContainer = $(this).closest('h4').next('.comments-container');
            commentsContainer.toggle();
            $(this).text(commentsContainer.is(':visible') ? 'Megjegyzések elrejtése' : 'Megjegyzések megjelenítése');
        });
    });
});
