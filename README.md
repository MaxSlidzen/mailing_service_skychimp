# Skychimp

Сервис управления рассылками

### Для корректной работы необходимо:

- Установить виртуальное окружение и зайти в него;
- Установить зависимости из requirements.txt `pip3 install -r requirements.txt` или pyproject.toml `poetry install`;
- Создать в корне проекта файл `.env` и внести свои настройки проекта (согласно шаблону `.env.sample`);
- Создать базу данных с именем, которое указали в файле `.env`;
- Применить все миграции командой `python3 manage.py migrate`;
- Создать суперпользователя командой `python3 manage.py csu` (опционно);
- Добавить объект работы с cron `python3 manage.py crontab add`.

### Описание функционала групп в рамках интерфейса приложений:

1. Обычные пользователи (без привязки к группе) могут:

   - радактировать/удалять свой профиль;
   - создавать/редактировать/удалять/просматривать своих клиентов;
   - создавать/редактировать/удалять/просматривать свои рассылки, а также изменять статус(активность) рассылки;
   - просматривать статистику(логи) своих рассылок;
   - просматривать статьи блога.

2. Группа менеджеров рассылок (права на просмотр пользователей и просмотр рассылок) может:

   - радактировать/удалять свой профиль;
   - просматривать все рассылки и изменять их статус(активность);
   - просматривать список пользователей и блокировать (только обычных пользователей).
   - просматривать статьи блога.

3. Группа контент-менеджеров (права CRUD для статей) может:

   - радактировать/удалять свой профиль; 
   - создавать/редактировать/удалять/просматривать статьи блога.

4. Администратор(суперпользователь) может удалять аккаунты пользователей, а также всё вышеперечисленное за исключением:

      - редактирования/удаления чужих клиентов, просмотра карточки отдельного клиента;
      - редактирования/удаления чужих рассылок.

### Примечания:

- База данных и проект по умолчанию работает по московскому времени. Подробный список часовых
  поясов https://en.wikipedia.org/wiki/List_of_tz_database_time_zones;
- При регистрации пользователя, на почту отправляется одноразовая ссылка для подтверждения регистрации;
- Для отправки всех активных(незавершенных) рассылок независимо от их расписаний введите команду `python3 manage.py send_mailing`;
- При удалении клиента (единственного оставшегося в рассылке) сама рассылка не удаляется и может оказаться пустой.
