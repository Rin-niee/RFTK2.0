document.addEventListener('DOMContentLoaded', function () {
    const ipDiscCheckbox = document.getElementById('id_discount_fact');
    const dSize = document.getElementById('id_discount_size');

    function toggledSize() {
        if (ipDiscCheckbox.checked) {
            dSize.style.display = '';
        } else {
            dSize.style.display = 'none';
        }
    }

    // При загрузке
    toggledSize();

    // При изменении
    ipDiscCheckbox.addEventListener('change', toggledSize);
});