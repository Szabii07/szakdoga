$(document).ready(function() {
    $('#noteForm').on('submit', function(e) {
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function(response) {
                // Hozzáadjuk az új megjegyzést a megjegyzések listához
                const noteHTML = `
                    <div class="note-item" id="note-${response.note_id}">
                        <p>${response.note}</p>
                        <button class="delete-note-btn" data-note-id="${response.note_id}">Törlés</button>
                    </div>
                `;
                $('#commentsSection').append(noteHTML);
                $('.comment-input').val(''); // Megjegyzés mező ürítése
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });

    // Megjegyzés törlése
    $(document).on('click', '.delete-note-btn', function() {
        const noteId = $(this).data('note-id');

        $.ajax({
            type: 'POST',
            url: '/delete-note/' + noteId + '/',
            data: {
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                $('#note-' + noteId).remove();
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
});
