    document.getElementById('add-bank').addEventListener('click', function () {
        const container = document.getElementById('bank-forms');
        const totalForms = container.querySelector('[name="banks-TOTAL_FORMS"]');
        let currentFormCount = parseInt(totalForms.value);
        const lastBankForm = container.querySelector('.bank-form:last-child');
        const newBankForm = lastBankForm.cloneNode(true);
        newBankForm.querySelectorAll('input, select, textarea').forEach(field => {
            if (field.name) {
                field.name = field.name.replace(/\d+/, currentFormCount);
                field.id = field.id.replace(/\d+/, currentFormCount);
                field.value = '';
            }
        });
        container.appendChild(newBankForm);
        totalForms.value = currentFormCount + 1;
    });