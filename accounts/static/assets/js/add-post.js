$(document).ready(function() {

    $('.select-multiple').select2({
        placeholder: "Оберіть Канал",
        allowClear: true
    });

    var cleave = new Cleave('#hm-0', {
        time: true,
        timePattern: ['h', 'm']
    });

    $('#datepicker-0').on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('DD/MM/YYYY'));
        validateFields();
    });

    $(document).on('change', 'input[name$="date_payment"]', function() {
        const datePaymentInput = $(this); 
        validateFutureDate(datePaymentInput);
    });

    $(document).on('change', 'input[name$="scrin"]', function(event) {
        const file = event.target.files[0];
        const preview = document.getElementById('preview');

        if (file) {
            const reader = new FileReader();

            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            };

            reader.readAsDataURL(file);
        }
    });

    const previewImage = document.getElementById("preview");
    const modalImage = document.getElementById("modalImage");

    previewImage.addEventListener("click", function() {
        // Копіюємо URL зображення у модальне вікно
        modalImage.src = previewImage.src;
    });



    // Отримуємо загальну кількість форм для formset
    var totalForms = document.getElementById('id_postchannel_set-TOTAL_FORMS');
    
    function addFormsetRow(channelId) {
        totalForms = document.getElementById('id_postchannel_set-TOTAL_FORMS');
        var formIndex = parseInt(totalForms.value);
        var initialFormTemplate = document.querySelectorAll('.formset-row').item(formIndex - 1);
        // Використовуємо шаблон для створення нового рядка
        var newForm = initialFormTemplate.cloneNode(true);


        // Оновлюємо індекси полів у новій формі на основі поточного значення totalForms
        newForm.innerHTML = newForm.innerHTML.replace(/-\d+-/g, `-${formIndex}-`);

        // Отримуємо значення часу, дати та тарифу з першої форми
        var lastDateValue = document.querySelector('input[name$="date_post"]').value;
        var lastTarifValue = document.querySelector('input[name$="tarif"]').value;
        var lastTimeValue = document.querySelector('input[name$="time_post"]').value;
        var lastPostValue = document.querySelector('input[name$="post"]').value;

     // Встановлюємо значення у новій формі
        newForm.querySelector('input[name$="date_post"]').value = lastDateValue;   
        newForm.querySelector('input[name$="tarif"]').value = lastTarifValue;
        newForm.querySelector('input[name$="post"]').value = lastPostValue;
        newForm.querySelector('select[name$="channel"]').value = channelId || 1;
        $(newForm).find('input[name$="time_post"]').val(lastTimeValue);


        // Вставляємо нову форму після останньої форми у formset
        //initialFormTemplate.parentNode.appendChild(newForm);
        initialFormTemplate.parentNode.insertBefore(newForm, initialFormTemplate.nextSibling);


        
        initializeDatepickers();
        newForm.querySelectorAll('[name$="time_post"]').forEach(function(field) {
            var newId = 'hm' + formIndex;
            field.id = newId;
            var cleave = new Cleave('#' + newId, {
                time: true,
                timePattern: ['h', 'm']
            });
        });
        // Оновлюємо кількість форм
        totalForms.value = parseInt(totalForms.value) + 1;
        updateFormIndexes();
        redistributeTotalSum();
        
        // Виводимо загальну суму без знижки
        const totalSum = parseFloat($('input[name="total-sum"]').val());
        $('#val-sum-not-discount').text(!isNaN(totalSum) ? totalSum.toFixed(2) + ' грн' : '0.00 грн');
        


    }
    function initializeDatepickers() {
        $('[name$="date_post"]').each(function(index, field) {
            var newId = 'dp' + index;
            field.id = newId;
            
            $('#' + newId).daterangepicker({
                singleDatePicker: true,
                autoUpdateInput: false,
                startDate: moment().startOf('day'), // Початкова дата для відображення календаря
                locale: {
                    format: 'DD/MM/YYYY'
                }
            });
    
            // Встановлюємо значення лише після вибору дати
            $('#' + newId).on('apply.daterangepicker', function(ev, picker) {
                $(this).val(picker.startDate.format('DD/MM/YYYY'));
                validateFields();
            });
    
            // Очищуємо поле, якщо вибір скасовано
            $('#' + newId).on('cancel.daterangepicker', function(ev, picker) {
                $(this).val('');
            });
        });
    }

    function removeFormsetRow(channelId) {
        $('.formset-row').each(function() {
            const channelSelect = $(this).find('select[name$="channel"]');
            if (channelSelect.val() == channelId) {
                if (totalForms.value == 1){
                    showAlert(text="Має залишитись хоча б одна форма");
                } else{
                    $(this).remove();
                    totalForms.value = parseInt(totalForms.value) - 1;
                    updateFormIndexes();
        
                }
            }
        });
    }

    // Обробник вибору "Вибрати всі" для додавання каналів
    $('#select-chaneger').on('select2:select', function(e) {
        const selectedValue = e.params.data.id;

        if (selectedValue.startsWith('select_all_')) {
            const category = e.params.data.element.dataset.category;
            $(`#select-chaneger optgroup[label="${category}"] option`).each(function() {
                if (!$(this).hasClass('select-all-option') && !$(this).prop('selected')) {
                    $(this).prop('selected', true);
                    addFormsetRow($(this).val());
                    validateFields();

                }
            });
            $('#select-chaneger').trigger('change');
        } else {
            addFormsetRow(selectedValue);
            validateFields();


        }
        calculateTotal();
    });

    // Обробник зняття вибору "Вибрати всі" для видалення каналів
    $('#select-chaneger').on('select2:unselect', function(e) {
        const unselectedValue = e.params.data.id;

        if (unselectedValue.startsWith('select_all_')) {
            const category = e.params.data.element.dataset.category;
            $(`#select-chaneger optgroup[label="${category}"] option`).each(function() {
                $(this).prop('selected', false);
                removeFormsetRow($(this).val());
            });
            $('#select-chaneger').trigger('change');
        } else {
            removeFormsetRow(unselectedValue);
        }
        redistributeTotalSum();
    });

    // Видалення окремого рядка через кнопку
    $(document).on('click', '.remove-row-btn', function() {
        if (totalForms.value == 1){
            showAlert(text="Має залишитись хоча б одна форма");
        } else{
            $(this).closest('.formset-row').remove();
            totalForms.value = parseInt(totalForms.value) - 1;
            updateFormIndexes();

            redistributeTotalSum();

        }

    });
    function redistributeTotalSum() {
        const totalSum = parseFloat($('#inp-total').val()); // Отримуємо загальну суму
        const tarifInputs = $('input[name$="tarif"]'); // Всі поля тарифів
        const formsetCount = tarifInputs.length; // Кількість формсетів
    
        if (!isNaN(totalSum) && formsetCount > 0) {
            const dividedSum = truncateToFixed(totalSum / formsetCount, 2); // Сума на кожен рядок
            let remainingSum = totalSum;
    
            tarifInputs.each(function(index) {
                if (index === formsetCount - 1) {
                    $(this).val(truncateToFixed(remainingSum, 2)); // Останній рядок отримує залишок
                } else {
                    $(this).val(dividedSum);
                    remainingSum -= parseFloat(dividedSum); // Оновлюємо залишок
                }
            });
        } else {
            // Якщо сума або кількість рядків некоректна, очищаємо поля
            tarifInputs.val('');
        }
    }


        // Додавання окремого рядка через кнопку
    $(document).on('click', '#add-new-row', function() {
        const channelSelect = $(this).find('select[name$="channel"]');
        addFormsetRow(channelSelect.val());
        calculateTotal();
        if (channelSelect.val()) {
            removeValidationError(channelSelect);
            validateFields();
        }
    });

    // --------- Рахування скидки та суми ------------------

    // Функція для обчислення суми значень у полях "тариф"
    function calculateTotal() {
            let total = 0;
            
            // Перебираємо всі поля тарифу та додаємо їх значення
            $('input[name$="tarif"]').each(function() {
                const value = parseFloat($(this).val());
                if (!isNaN(value)) {
                    total += value;
                }
            });
    
            // Виводимо загальну суму в елемент з id="val-sum"
            $('#val-sum').text(total.toFixed(2) + ' грн');

            return total;
        }
            function truncateToFixed(num, decimals) {
                const factor = Math.pow(10, decimals);
                return (Math.trunc(num * factor) / factor).toFixed(decimals);
            }
        
            function redistributeTotalSum() {
                const totalSumInput = $('#inp-total'); // Поле "Загальна сума"
                const discountInput = $('#inp-discount'); // Поле "Знижка"
                const totalSumOutput = $('#val-sum'); // Поле для виведення "Загальна сума після знижки"
                const discountAmountOutput = $('#val-sum-discount'); // Поле для виведення суми знижки
                const tarifInputs = $('input[name$="tarif"]'); // Отримуємо всі поля "tarif"
                const formsetCount = tarifInputs.length; // Кількість формсетів
        
                const totalSum = parseFloat(totalSumInput.val()); // Загальна сума
                const discountPercentage = parseFloat(discountInput.val()) || 0; // Знижка у відсотках (0, якщо не введено)
        
                if (!isNaN(totalSum) && formsetCount > 0) {
                    // Розрахунок знижки, якщо вона є
                    const discountAmount = truncateToFixed((totalSum * discountPercentage) / 100, 2);
                    const discountedSum = totalSum - discountAmount;
        
                    // Оновлюємо відображення суми знижки та загальної суми
                    discountAmountOutput.text(discountAmount + ' грн'); // Сума знижки
                    totalSumOutput.text(discountedSum.toFixed(2) + ' грн'); // Сума після знижки
        
                    // Розподіляємо загальну суму (після знижки) між полями "tarif"
                    const dividedSum = truncateToFixed(discountedSum / formsetCount, 2); // Розраховуємо частку без округлення
                    let remainingSum = discountedSum; // Для обліку можливих неточностей
                    
                    tarifInputs.each(function (index) {
                        if (index === formsetCount - 1) {
                            // Для останнього поля додаємо залишок
                            $(this).val(truncateToFixed(remainingSum, 2));
                        } else {
                            $(this).val(dividedSum);
                            remainingSum -= parseFloat(dividedSum); // Зменшуємо залишок на поточне значення
                        }
                    });
                } else {
                    // Якщо введені дані некоректні, очищаємо поля
                    discountAmountOutput.text('0.00 грн');
                    totalSumOutput.text('0.00 грн');
                    tarifInputs.val('');
                }
            }
        
            // Виклик розподілення при зміні "Загальної суми"
            $('#inp-total').on('input', function () {
                redistributeTotalSum();
            });
        
            // Виклик перерахунку при зміні знижки
            $('#inp-discount').on('input', function () {
                redistributeTotalSum();
            });
        

    //-------- Валідація



    
    async function validateFields() {
        let isValid = true;
        const promises = [];
    
        // Перевірка вибору каналу
        $('select[name$="channel"]').each(function() {
            const channel = $(this).val();
            const formRow = $(this).closest('.formset-row');
    
            if (channel === "") {
                showValidationError($(this), "Потрібно обрати канал.");
                isValid = false;
            } else {
                removeValidationError($(this));
                
                // Перевірка дати
                const dateInput = formRow.find('input[name$="date_post"]');
                if (!validateDateField(dateInput)) {
                    isValid = false;
                } else {
                    // Перевірка часу
                    const timeInput = formRow.find('input[name$="time_post"]');
                    if (!validateTimeField(timeInput)) {
                        isValid = false;
                    } else {
                        if (document.querySelector('.is_update')){
                            return;
                        } else {
                        // Додаємо проміс перевірки часу до масиву
                        promises.push(checkTimeAvailability(formRow).then((available) => {
                            if (!available) {
                                isValid = false;
                            }
                        }));}
                    }
                }
            }
        });
    
        // Чекаємо на завершення всіх асинхронних перевірок
        await Promise.all(promises);
    
        const btnSuccess = document.querySelector('.btn-success');
        if (!isValid) {
            btnSuccess.classList.add('disabled');
        } else {
            btnSuccess.classList.remove('disabled');
        }
        return isValid;
    }
    
        // Виклик функції при зміні загальної суми
        $('#inp-total').on('input', function() {
            redistributeTotalSum();
            
            document.querySelector('#val-sum-not-discount').textContent = `${$(this).val()}.00 грн`;
        });



        function validateFutureDate(dateInput) {
            const dateValue = dateInput.val();
            const [day, month, year] = dateValue.split('/'); // Припускаємо формат DD/MM/YYYY
            const selectedDate = new Date(`${year}-${month}-${day}`);
            const today = new Date();
            
            // Скидаємо час для порівняння тільки дати
            today.setHours(0, 0, 0, 0);
            selectedDate.setHours(0, 0, 0, 0);
        
            if (selectedDate < today) {
                showValidationError(dateInput, "Дата не може бути раніше сьогоднішньої.");
                return false;
            } else {
                removeValidationError(dateInput);
                return true;
            }
        }
    
        function validateDateField(dateInput) {
            const dateValue = dateInput.val();
            if (!/^\d{2}\/\d{2}\/\d{4}$/.test(dateValue)) {
                showValidationError(dateInput, "DD/MM/YYYY.");
                return false;
            }
            removeValidationError(dateInput);
            return true;
        }
    
        function validateTimeField(timeInput) {
            const timeValue = timeInput.val();
            if (!/^\d{2}:\d{2}$/.test(timeValue)) {
                showValidationError(timeInput, "HH:MM.");
                return false;
            }
            removeValidationError(timeInput);
            return true;
        }
    
        function checkTimeAvailability(formRow) {
            return new Promise((resolve) => {
                const timeInput = formRow.find('input[name$="time_post"]');
                const dateInput = formRow.find('input[name$="date_post"]');
                const channelId = formRow.find('select[name$="channel"]').val();
            
                const timeValue = timeInput.val();
                const dateValue = formatDateToYMD(dateInput.val());
            
                // Перевірка, чи заповнені значення часу та дати перед викликом AJAX
                if (!timeValue || !dateValue || !channelId) {
                    // Якщо значення часу, дати або каналу не заповнені, очищуємо повідомлення
                    removeValidationError(timeInput);
                    timeInput.next('.valid-feedback').remove();
                    resolve(false);
                    return; // Завершуємо функцію тут, щоб не виконувати AJAX
                }
        
                // Виконуємо AJAX-запит лише якщо всі поля заповнені
                $.ajax({
                    url: '/check-time/',
                    method: 'GET',
                    data: {
                        channel_id: channelId,
                        date_post: dateValue,
                        time_post: timeValue
                    },
                    success: function(response) {
                        if (response.exists) {
                            showValidationError(timeInput, `Місце зайнято.`);
                            resolve(false);
                        } else {
                            showValidationSuccess(timeInput, "Місце вільне!");
                            resolve(true);
                        }
                    },
                    error: function() {
                        showValidationError(timeInput, "Не вдалося перевірити доступність.");
                        resolve(false);
                    }
                });
            });
        }
        
    
        function showValidationError(input, message) {
            input.removeClass('is-valid').addClass('is-invalid');
            input.next('.valid-feedback').remove();
            if (input.next('.invalid-feedback').length === 0) {
                input.after(`<div class="invalid-feedback">${message}</div>`);
            }
        }
    
        function removeValidationError(input) {
            input.removeClass('is-invalid');
            input.next('.invalid-feedback').remove();
        }
    
        function showValidationSuccess(input, message) {
            input.removeClass('is-invalid').addClass('is-valid');
            input.next('.invalid-feedback').remove();
            if (input.next('.valid-feedback').length === 0) {
                input.after(`<div class="valid-feedback">${message}</div>`);
            }
        }
    
        function formatDateToYMD(dateString) {
            const dateParts = dateString.split('/');
            if (dateParts.length === 3) {
                const day = dateParts[0];
                const month = dateParts[1];
                const year = dateParts[2];
                return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
            }
            return dateString;
        }
    
        $(document).on('input', 'input[name$="time_post"], select[name$="channel"]', 'input[name$="date_post"]', function() {
            validateFields();
            
            // Видаляємо повідомлення "Місце вільне", якщо поля було змінено
            // $(this).closest('.formset-row').find('.valid-feedback').remove();
        });

        $(document).on('change', 'input[name$="date_post"]', function() {
            validateFields();
            $(this).closest('.formset-row').find('.valid-feedback').remove();

        });
        $(document).on('input', 'input[name$="tarif"]', function() {
            validateFields();
            calculateTotal();
        });

    
    

    function updateFormIndexes() {
        var forms = document.querySelectorAll('.formset-row');
        var totalForms = document.getElementById('id_postchannel_set-TOTAL_FORMS');
        totalForms.value = forms.length;

        forms.forEach(function(form, index) {
            $(form).find(':input').each(function() {
                var name = $(this).attr('name');
                var id = $(this).attr('id');
                $(this).attr('value', $(this).val());

                // Оновлюємо індекси в name та id полях
                if (name) {
                    var newName = name.replace(/-\d+-/g, `-${index}-`);
                    $(this).attr('name', newName);
                }

                if (id) {
                    var newId = id.replace(/-\d+-/g, `-${index}-`);
                    $(this).attr('id', newId);
                }
            });
        });
    }

    function waitForFormser() {
        const dateFields = document.querySelectorAll('.date-field'); // Додайте клас `date-field` до полів дати
        const timeFields = document.querySelectorAll('.time-field'); // Додайте клас `time-field` до полів часу
        
        if (dateFields &&  timeFields) {
            // Коли контейнер знайдено, запускаємо основний код
            chaneger_date_time(dateFields,timeFields);
            
        } else {
            // Якщо контейнер ще не існує, перевіряємо знову через 100 мс
            setTimeout(waitForFormser, 100);
        }
    }
    
       // Знайти всі поля дати та часу
   function chaneger_date_time(dateFields,timeFields){

       // Форматування дат
       dateFields.forEach(field => {
           const dateValue = field.value;

           console.log(dateValue);
           if (dateValue) {
               const [year, month, day] = dateValue.split("-");
               field.value = `${day}/${month}/${year}`;  // Формат DD/MM/YYYY
           }
       });

       // Форматування часу
       timeFields.forEach(field => {
           const timeValue = field.value;
           if (timeValue) {
               const [hours, minutes] = timeValue.split(":");
               field.value = `${hours}:${minutes}`;  // Формат HH:MM
           }
       });
    } 
    const title =  document.querySelector('.card-title').textContent.trim();
    if (title.includes("Внести зміни в пост")) {
        waitForFormser();
    } else {
        return;
    }

    function showAlert(text) {
        // Створюємо елемент алерту
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show';
        alertDiv.role = 'alert';
        alertDiv.innerHTML = `
            <i class="bi bi-x-circle alert-icon"></i>
            ${text}
        `;
    
        // Стилі для фіксованої позиції
        alertDiv.style.position = 'fixed';
        alertDiv.style.top = '90px'; // Відстань від верху
        alertDiv.style.left = '50%';
        alertDiv.style.transform = 'translateX(-50%)';
        alertDiv.style.zIndex = '1050'; // Високий z-index для накладання поверх інших елементів
        alertDiv.style.width = '400px'; // Фіксована ширина
        alertDiv.style.textAlign = 'center';
    
        // Додаємо алерт в початок тіла документа
        document.body.appendChild(alertDiv);
    
        setTimeout(() => {
            alertDiv.classList.remove('show'); 
            alertDiv.addEventListener('transitionend', () => alertDiv.remove()); // Видаляє елемент після завершення анімації
        }, 4000);
    }
    



});


// TODO 
