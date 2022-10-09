function messageAlert(message, type, kwargs) {
    Swal.fire({
        title: message,
        icon: type,
        ...kwargs,
    });
}

export {messageAlert};