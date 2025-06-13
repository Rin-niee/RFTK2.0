document.addEventListener('DOMContentLoaded', function () {
    const nameSelect = document.getElementById('organizations-names');

    // Загружаем все организации при загрузке страницы
    fetch(`get_organizations/`)
        .then(response => response.json())
        .then(data => {
            nameSelect.innerHTML = '<option value="">-- Выбрать организацию --</option>';
            data.forEach(org => {
                const option = document.createElement('option');
                option.value = org.id;
                option.text = org.name;
                nameSelect.appendChild(option);
            });
        })
        .catch(() => {
            nameSelect.innerHTML = '<option value="">Ошибка загрузки</option>';
        });

    // Подстановка данных по выбранной организации
    nameSelect.addEventListener('change', function () {
        const selectedId = this.value;
        if (!selectedId) return;

        fetch(`get_organizations_details/?id=${selectedId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }

                document.getElementById('id_org_name').value = data.org_name;
                document.getElementById('id_INN_number').value = data.INN;
                document.getElementById('id_KPP').value = data.KPP;
                document.getElementById('id_OGRN').value = data.OGRN;

                document.getElementById('id_phone').value = data.phone;
                document.getElementById('id_fax').value = data.fax;

                document.getElementById('id_position_boss').value = data.position_boss;
                document.getElementById('id_name_boss').value = data.name_boss;
                document.getElementById('id_name_buh').value = data.name_buh;
                document.getElementById('id_RS').value = data.bank_rs;
                document.getElementById('id_bank_name').value = data.bank_name;
                document.getElementById('id_bank_adress').value = data.bank_adress;
                document.getElementById('id_KS').value = data.bank_ks;
            })
            .catch(err => {
                console.error('Ошибка при получении деталей:', err);
                alert('Не удалось загрузить данные');
            });
    });
});