from post.models import CategoriyChanels, ClientsCategoriy, ClientsTypes
from sales.models import ClientStatus
from django.contrib.auth import get_user_model; 


if not CategoriyChanels.objects.filter(name='Основні').exists():
    CategoriyChanels.objects.create(name='Основні', slug='base-channels')
    CategoriyChanels.objects.create(name='Регіональні', slug='regional-channels')
    ClientsCategoriy.objects.create(name='Категорія відсутня', slug='cat-nema')
    CategoriyChanels.objects.create(name='Боти', slug='bots')
    CategoriyChanels.objects.create(name='Спеціалізовані', slug='specialized-channels')

if not ClientsTypes.objects.filter(name='Відсутня').exists():
    ClientsTypes.objects.create(name='Відсутня', slug='types-nema')

if not ClientStatus.objects.filter(name='Новий').exists():
    ClientStatus.objects.create(name='Новий', slug='new')
    ClientStatus.objects.create(name='В процесі', slug='in-process')
    ClientStatus.objects.create(name='Архів', slug='arhiv')

User = get_user_model()

if not User.objects.filter(username='dev').exists():
    user_dev = User.objects.create_superuser('dev', 'root@example.com', 'sakamoto39')
    user_dev.save()
