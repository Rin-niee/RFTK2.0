document.addEventListener('DOMContentLoaded', () => {
    const nameSelect = document.getElementById('organizations-names-buy');

    async function loadOrganizations() {
        try {
            const response = await fetch(`get_all_organizations/`);

            if (!response.ok) {
                throw new Error(`Ошибка загрузки организаций: ${response.status}`);
            }

            const data = await response.json();

            nameSelect.innerHTML = '<option value="">-- Выбрать организацию --</option>';
            data.forEach(org => {
                const option = document.createElement('option');
                option.value = org.id;
                option.textContent = org.name;
                nameSelect.appendChild(option);
            });
        } catch (error) {
            console.error(error);
            nameSelect.innerHTML = '<option value="">Ошибка загрузки</option>';
        }
    }

    async function loadOrganizationDetails(orgId) {
        try {
            const response = await fetch(`get_counterparty_details_for_counter/?id=${orgId}`);

            if (!response.ok) {
                throw new Error(`Ошибка получения данных организации: ${response.status}`);
            }

            const data = await response.json();

            if (data.error) {
                alert(data.error);
                return;
            }

            document.getElementById('id_buy-org_name').value = data.org_name ?? '';
            document.getElementById('id_buy-INN_number').value = data.INN ?? '';
            document.getElementById('id_buy-KPP').value = data.KPP ?? '';
            document.getElementById('id_buy-OGRN').value = data.OGRN ?? '';

            document.getElementById('id_buy-phone').value = data.phone ?? '';
            document.getElementById('id_buy-fax').value = data.fax ?? '';

            document.getElementById('id_buy-RS').value = data.bank_rs ?? '';
            document.getElementById('id_buy-bank_name').value = data.bank_name ?? '';
            document.getElementById('id_buy-bank_adress').value = data.bank_adress ?? '';
            document.getElementById('id_buy-KS').value = data.bank_ks ?? '';
        } catch (error) {
            console.error('Ошибка при получении деталей:', error);
            alert('Не удалось загрузить данные');
        }
    }

    nameSelect.addEventListener('change', function () {
        const selectedId = this.value;
        if (selectedId) {
            loadOrganizationDetails(selectedId);
        }
    });

    loadOrganizations();
});
