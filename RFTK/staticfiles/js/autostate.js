document.addEventListener('DOMContentLoaded', function () {
    const typeSelect = document.getElementById('counterparty-type');
    const nameSelect = document.getElementById('counterparty-names');

    typeSelect.addEventListener('change', function () {
        const type = this.value;
        nameSelect.innerHTML = '<option value="">-- Загрузка... --</option>';

        //Список контрагентов по типу
        fetch(`get_counterparties/?type=${type}`)
            .then(response => response.json())
            .then(data => {
                nameSelect.innerHTML = '<option value="">-- Выбрать --</option>';
                data.forEach(counterparty => {
                    const option = document.createElement('option');
                    option.value = counterparty.id;
                    option.text = counterparty.name;
                    nameSelect.appendChild(option);
                });
            })
            .catch(() => {
                nameSelect.innerHTML = '<option value="">Ошибка загрузки</option>';
            });
    });

    nameSelect.addEventListener('change', function () {
        const selectedId = this.value;
        if (!selectedId) return;

        fetch(`get_counterparty_details/?id=${selectedId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }

                if (data.type === 'org') { //подставляем данные для организации
                    document.getElementById('id_IP_fact').checked = data.IP_fact;
                    document.getElementById('id_org_name').value = data.name;
                    document.getElementById('id_all_name').value = data.full_name;
                    document.getElementById('id_INN_number').value = data.INN;
                    document.getElementById('id_OKPO_code').value = data.OKPO_code;
                    document.getElementById('id_OKVED').value = data.OKVED;
                    document.getElementById('id_org_adress').value = data.org_adress;
                    document.getElementById('id_OGRN').value = data.OGRN;
                    document.getElementById('id_KPP').value = data.KPP;

                    document.getElementById('id_RS').value = data.bank_rs;
                    document.getElementById('id_bank_name').value = data.bank_name;
                    document.getElementById('id_bank_adress').value = data.bank_adress;
                    document.getElementById('id_KS').value = data.bank_ks;

                    document.getElementById('id_phone').value = data.phone;
                    document.getElementById('id_fax').value = data.fax;
                    document.getElementById('id_email').value = data.email;
                    document.getElementById('id_vebsite').value = data.vebsite;

                    document.getElementById('id_position_boss').value = data.position_boss;
                    document.getElementById('id_name_boss').value = data.name_boss;
                    document.getElementById('id_name_buh').value = data.name_buh;
                    document.getElementById('id_name_kass').value = data.name_kass;
                    document.getElementById('id_USL_name').value = data.usl_name;
                } if (data.type === 'ind') {//подставляем данные для частной организации
                    
                    document.getElementById('id_priv_name').value = data.full_name;
                    document.getElementById('id_priv_adress').value = data.address;
                    document.getElementById('id_passport').value = data.passport;
                    document.getElementById('id_Who_gave').value = data.Who_gave;
                    document.getElementById('id_DATE_gave').value = data.DATE_gave;

                    document.getElementById('id_bank_name').value = data.bank_name;
                    document.getElementById('id_bank_adress').value = data.bank_adress;
                    document.getElementById('id_KS').value = data.bank_ks;
                    document.getElementById('id_RS').value = data.bank_rs;

                    document.getElementById('id_phone').value = data.phone;
                    document.getElementById('id_fax').value = data.fax;
                    document.getElementById('id_email').value = data.email;
                    document.getElementById('id_vebsite').value = data.vebsite;

                    document.getElementById('id_position_boss').value = data.position_boss;
                    document.getElementById('id_name_boss').value = data.name_boss;
                    document.getElementById('id_name_buh').value = data.name_buh;
                    document.getElementById('id_name_kass').value = data.name_kass;
                    document.getElementById('id_USL_name').value = data.usl_name;
                }
            })
            .catch(err => {
                console.error('Ошибка при получении деталей:', err);
                alert('Не удалось загрузить данные');
            });
    });
});