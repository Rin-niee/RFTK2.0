document.addEventListener('DOMContentLoaded', function () {
    const ipFactCheckbox = document.getElementById('id_IP_fact');
    const kppField = document.getElementById('kpp-field');

    function toggleKPP() {
        if (ipFactCheckbox.checked) {
            kppField.style.display = 'none';
        } else {
            kppField.style.display = '';
        }
    }

    // При загрузке
    toggleKPP();

    // При изменении
    ipFactCheckbox.addEventListener('change', toggleKPP);
});