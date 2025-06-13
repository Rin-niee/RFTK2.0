document.addEventListener('DOMContentLoaded', function () {
    const radios = document.querySelectorAll('input[name="consignee_status"]');
    const consigneeInfoBlock = document.getElementById('consignee-info-block');

    function setFieldsDisabled(container, disabled) {
        const elements = container.querySelectorAll('input, select, textarea');
        elements.forEach(el => el.disabled = disabled);
    }

    function toggleConsigneeFields() {
        const selected = document.querySelector('input[name="consignee_status"]:checked');
        if (!selected || !consigneeInfoBlock) return;

        if (selected.value === '0') {
            consigneeInfoBlock.style.display = 'none';
            setFieldsDisabled(consigneeInfoBlock, true);
        } else {
            consigneeInfoBlock.style.display = '';
            setFieldsDisabled(consigneeInfoBlock, false);
        }
    }

    toggleConsigneeFields(); // При загрузке
    radios.forEach(radio => {
        radio.addEventListener('change', toggleConsigneeFields);
    });
});