// static/js/chat.js
$(document).ready(function() {
    $('#chat-send-button').click(function() {
        var user_question = $('#chat-input-field').val();
        if (user_question) {
            // Send the user_question to the server
            $.post('/chat', { message: user_question }, function(data) {
                // Add the answer to the chat window
                $('#chat-window').append('<p>' + data.answer + '</p>');
            });

            // Clear the input field
            $('#chat-input-field').val('');
        }
    });
});