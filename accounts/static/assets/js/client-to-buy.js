

$('.scp').on('click', function(event) {
   var textToCopy = $(event.target).attr('data-social');
   if (textToCopy) {
       navigator.clipboard.writeText(textToCopy);
   }
 });



 $('.dia').on('click', function(event) {

  const isProcessClient = event.target.classList.contains('process-client');
  const isArhivClient = event.target.classList.contains('arhiv-client');
  
  if (isProcessClient || isArhivClient) {
    const slug = event.target.getAttribute('data-slug');
    const message = isProcessClient
      ? '<span class="badge shade-green">Обробленний</span>'
      : '<span class="badge shade-light text-dark">В архиві</span>';
    
    // Оновлюємо DOM перед викликом fetch
    $(event.target).closest('tr').find('td').eq(-2).html(message);
    const url = isProcessClient
      ? 'processClient'
      : 'processClientToArhiv';
    setTimeout(() => fetch_to_base(event, slug, message, url), 0);
  }
});
const clients = new Set();
// Ручне перенесення клієнтів або внесення в архив

$(".select-single").select2({

});

document.querySelectorAll('.get-client-id-for-change').forEach(checkbox => {
  checkbox.addEventListener('change', function(){
    const clientId = checkbox.getAttribute('data-client-id');
    if (checkbox.checked) {
      clients.add(clientId); 
    } else {
      clients.delete(clientId); 
    }
    document.getElementById('helperbox').style.display = clients.size > 0 ? 'block' : 'none';
  });
});

document.getElementById('update-clients').addEventListener('click', function(e){
    e.preventDefault();
    const userId = document.getElementById('select-users').value; 
    if (!userId) {
      alert('Оберіть користувача для переносу клієнтів');
      return;
    }
    const url = `${changeUsersClientsURL}?clients=${Array.from(clients).join(',')}&user_id=${userId}`;
    
    $(this).attr('href', url);

    window.location.href = url;
});

document.getElementById('copy-cilents').addEventListener('click', function(e){
  e.preventDefault();
  const url = `${textToCopyUsersClientsURL}?clients=${Array.from(clients).join(',')}`;
  
  $(this).attr('href', url);

  window.location.href = url;
});


document.querySelectorAll('.get-client-info').forEach(button => {
   button.addEventListener('click', function() {
       const clientId = this.getAttribute('data-client-id');
       fetch(`/get-client-info/${clientId}/`) // Виклик URL з ID клієнта
           .then(response => response.json())
           .then(data => {
               // Заповнюємо модальне вікно інформацією про клієнта
               document.getElementById('client-info-content').innerHTML = `
                 <div class="col-lg-6 col-sm-6 col-6">
                     <div class="customer-card">
                       <h6>Client ID:</h6>
                       <h5>#${data.id}</h5>
                     </div>
                   </div>    
                   <div class="col-lg-6 col-sm-6 col-6">
                     <div class="customer-card">
                       <h6>Дата створення:</h6>
                       <h5>${data.data}</h5>
                     </div>
                   </div>
                   <div class="col-lg-6 col-sm-6 col-6">
                     <div class="customer-card">
                       <h6>Дата першої покупки:</h6>
                       <h5>${data.data_the_first_buys}</h5>
                     </div>
                   </div>
                    <div class="col-lg-6 col-sm-6 col-6">
                     <div class="customer-card">
                       <h6>Дата останньої покупки:</h6>
                       <h5>${data.data_the_last_buys}</h5>
                     </div>
                   </div>
                   <div class="col-lg-6 col-sm-6 col-6">
                     <div class="customer-card" >
                       <h6>Кількість продажів:</h6>
                       <h5>${data.client_cost}</h5>
                     </div>
                   </div>
                   <div class="col-lg-6 col-sm-6 col-6">
                     <div class="customer-card">
                       <h6>Локація:</h6>
                       <h5>${data.city}</h5>
                     </div>
                   </div>
                  <div class="col-lg-12 col-sm-6 col-6">
                     <div class="customer-card">
                       <h6>Username:</h6>
                       <h5>${data.social_media}</h5>
                     </div>
                   </div>
                   <div class="col-lg-12 col-sm-6 col-6">
                     <div class="customer-card">
                       <h6>Посилання:</h6>
                       <h5><a href="${data.link}" class="btn btn-outline-info" target=_blank">${data.link}</a></h5>
                     </div>
                     
                   </div>
                    </div>
                    <div class="col-lg-12 col-sm-6 col-6">
                     <div class="customer-card">
                       <h6>Повідомлення:</h6>
                       <h5>${data.messages}</h5>
                     </div>
                   </div>
                    <div class="col-lg-12 col-sm-6 col-6">
                     <div class="customer-card">
                       <h6>Посилання на канал:</h6>
                       <h5><a href="${data.channels_link}" class="btn btn-outline-info" target=_blank">${data.channels_tg}</a></h5>
                     </div>
                     
                   </div>
         </div>
         <div class="modal-footer">
           <button type="button" class="btn btn-warning to-upd bi bi-pencil-square m-0" data-client-slug="${data.slug}" id="process-client-button"  data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="Змінити дані клієнта"></button>
           <button type="button" class="btn btn-success to-procces" data-client-slug="${data.slug}" id="process-client-button">Клієнт в роботі</button>
           <button type="button" class="btn btn-dark" data-bs-dismiss="modal">Закрити</button>
         </div>
               `;
           })
           .catch(error => console.error('Error:', error));
   });
});
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('to-upd')) { 
        const slug = event.target.getAttribute('data-client-slug');
        window.location.href = `/update-clients/${slug}`;  // Перенаправлення на потрібний URL
    }
});
document.addEventListener('click', function(event) {
if (event.target.classList.contains('to-procces')) {
   const slug = event.target.getAttribute('data-client-slug');

  var cock = getCookie('csrftoken');
   
   fetch(`/to-process-client/${slug}/`, {
       method: 'POST',
       headers: {
           'X-CSRFToken': cock,  // Додаємо CSRF токен
           'Content-Type': 'application/json'
       },
   })
   .then(response => response.json())
   .then(data => {
       if (data.status === 'success') {
           alert(data.message);
       } else {
           alert('Помилка: ' + data.message);
       }
   })
   .catch(error => console.error('Error:', error));
}
});



async function fetch_to_base(event, slug, message, url){
  var cock = getCookie('csrftoken');
    await fetch(`/${url}/${slug}`, {
         method: 'POST',
         headers: {
             'X-CSRFToken': cock,  // Додаємо CSRF токен
             'Content-Type': 'application/json'
         },
     })
     .then(response => response.json())
     .then(data => {
         if (data.status === 'success') {
         } else {
             alert('Помилка: ' + data.message);
         }
     })
     .catch(error => console.error('Error:', error));
  }

// Функція для отримання CSRF токена
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
     const cookies = document.cookie.split(';');
     for (let i = 0; i < cookies.length; i++) {
         const cookie = cookies[i].trim();
         if (cookie.substring(0, name.length + 1) === (name + '=')) {
             cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
             break;
         }
     }
  }
  return cookieValue;
  }
