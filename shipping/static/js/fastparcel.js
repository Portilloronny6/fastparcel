function messageAlert(message, type) {
    Swal.fire({
        title: message,
        icon: type,
        confirmButtonText: 'Ok'
    });
}