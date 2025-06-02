document.addEventListener("DOMContentLoaded", function () {
    const addGoodsButtons = document.querySelectorAll(".add-goods");
    const container = document.getElementById('goods-forms');
    const tbody = container.querySelector('tbody.goods-form');
    const totalForms = container.querySelector('[name="gformset-TOTAL_FORMS"]');

    addGoodsButtons.forEach(addButton => {
        addButton.addEventListener('click', function () {
            const currentFormCount = parseInt(totalForms.value);
            const lastRow = tbody.querySelector('tr.goods-form:last-child');
            const newRow = lastRow.cloneNode(true);

            // Обновляем поля в новом ряду
            newRow.querySelectorAll('input, select, textarea').forEach(field => {
                if (field.name) {
                    field.name = field.name.replace(/\d+/, currentFormCount);
                }
                if (field.id) {
                    field.id = field.id.replace(/\d+/, currentFormCount);
                }
                if (field.type !== 'checkbox' && field.type !== 'radio') {
                    field.value = '';
                } else {
                    field.checked = false;
                }
            });

            tbody.appendChild(newRow);
            totalForms.value = currentFormCount + 1;
        });
    });

    // Удаление строки при клике по корзинке
    tbody.addEventListener('click', function (e) {
        if (e.target.classList.contains('delete-row')) {
            const rows = tbody.querySelectorAll('tr.goods-form');
            if (rows.length > 1) {
                const row = e.target.closest('tr.goods-form');
                row.remove();
                const updatedRows = tbody.querySelectorAll('tr.goods-form');
                updatedRows.forEach((row, index) => {
                    row.querySelectorAll('input, select, textarea').forEach(field => {
                        if (field.name) {
                            field.name = field.name.replace(/\d+/, index);
                        }
                        if (field.id) {
                            field.id = field.id.replace(/\d+/, index);
                        }
                    });
                });

                totalForms.value = updatedRows.length;
            }
        }
    });
});