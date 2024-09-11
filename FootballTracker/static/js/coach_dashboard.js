document.addEventListener("DOMContentLoaded", function() {
    // Handle like button click
    document.querySelectorAll('.post-actions .like-button').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const postId = this.dataset.postId;
            fetch(`/like_post/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ action: 'like' })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateLikeDislikeCounts(postId, data.like_count, data.dislike_count);
                }
            });
        });
    });

    // Handle dislike button click
    document.querySelectorAll('.post-actions .dislike-button').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const postId = this.dataset.postId;
            fetch(`/dislike_post/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ action: 'dislike' })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateLikeDislikeCounts(postId, data.like_count, data.dislike_count);
                }
            });
        });
    });

    // Handle comment form submission
    document.querySelectorAll('.comment-form').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const postId = this.dataset.postId;
            const formData = new FormData(this);

            fetch(`/add_comment/${postId}/`, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    addCommentToPost(postId, data.comment);
                }
            });
        });
    });

    function updateLikeDislikeCounts(postId, likeCount, dislikeCount) {
        document.querySelector(`#like-count-${postId}`).textContent = likeCount;
        document.querySelector(`#dislike-count-${postId}`).textContent = dislikeCount;
    }

    function addCommentToPost(postId, comment) {
        const commentList = document.querySelector(`#comments-${postId}`);
        const commentElement = document.createElement('div');
        commentElement.classList.add('comment');
        commentElement.innerHTML = `<strong>${comment.user}:</strong> ${comment.content} <em>(${comment.created_at})</em>`;
        commentList.appendChild(commentElement);
    }

    // Utility function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
