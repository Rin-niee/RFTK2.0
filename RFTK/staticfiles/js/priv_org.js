document.addEventListener('DOMContentLoaded', function () {
    const radios = document.querySelectorAll('input[name="type"]');
    const orgFields = document.getElementById('org-fields');  // блок для организации
    const indFields = document.getElementById('ind-fields');  // блок для частника

    function setFieldsDisabled(container, disabled) {
        const elements = container.querySelectorAll('input, select, textarea');
        elements.forEach(el => el.disabled = disabled);
    }

    function toggleFields() {
        const checkedRadio = document.querySelector('input[name="type"]:checked');
        if (!checkedRadio) return;

        if (checkedRadio.value === 'org') {
            orgFields.style.display = '';
            indFields.style.display = 'none';

            setFieldsDisabled(orgFields, false);
            setFieldsDisabled(indFields, true);
        } else if (checkedRadio.value === 'ind') {
            orgFields.style.display = 'none';
            indFields.style.display = '';

            setFieldsDisabled(orgFields, true);
            setFieldsDisabled(indFields, false);
        }
    }

    // Изначально выставляем правильный вид
    toggleFields();

    // Обработчик изменения
    radios.forEach(radio => {
        radio.addEventListener('change', toggleFields);
    });
});

