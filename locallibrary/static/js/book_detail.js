function confirmBelovedChange(event) {
    const userConfirmed = confirm("Вы уверены, что хотите сделать эту книгу любимой?");
    if (!userConfirmed) {
        event.preventDefault();
            return false;
    }
    return true;
}