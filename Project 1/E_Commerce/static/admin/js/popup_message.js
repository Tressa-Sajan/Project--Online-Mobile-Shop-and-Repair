function displayPopupMessage(message, messageType) {
    var alertType = 'info';
    if (messageType === 'error') {
        alertType = 'danger';
    } else if (messageType === 'success') {
        alertType = 'success';
    }

    var alertElement = '<div class="alert alert-' + alertType + ' alert-dismissible fade show" role="alert">' +
        message +
        '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
        '<span aria-hidden="true">&times;</span>' +
        '</button>' +
        '</div>';

    // Append the alert element to the messages container
    $('#messages-container').append(alertElement);
}
