

echo "Створення міграцій..."
if ! python manage.py makemigrations; then
    echo "Помилка при створенні міграцій."
    exit 1
fi






echo "Збирання статичних файлів..."
if ! python manage.py collectstatic --noinput; then
    echo "Помилка при збиранні статичних файлів."
    exit 1
fi


echo "Виконання міграцій..."
if ! python manage.py migrate; then
    echo "Помилка при виконанні міграцій."
    exit 1
fi


echo "Ініціалізація даних..."
if ! python manage.py shell < initialize.py; then
    echo "Помилка при ініціалізації додаткових даних."
    exit 1
fi




exec gunicorn erpsys.wsgi:application --bind 0.0.0.0:8000
