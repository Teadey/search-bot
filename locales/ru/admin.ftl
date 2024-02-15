admin-start-text = Добро пожаловать в панель администратора!
admin-button-back = Назад
admin-button-yes = Да
admin-button-no = Нет
admin-button-cancel = Отмена
admin-button-close = Закрыть

# User list
admin-users-list = Список пользователей:
admin-button-list-users = Пользователи
admin-error-users-notfound = Ни одного пользователя не было найдено
admin-users-export = Экспортировать 📦

# Admin list
admin-admins-list = Список администраторов:
admin-error-admins-notfound = Ни одного администратора еще не было добавлено
admin-button-list-admins = Администраторы
admin-button-add-admin = Добавить 🆕
admin-button-del-admin = Удалить 🗑
admin-show-admin = 
    Айди администратора: <a href='tg://user?id={ $admin_id }'><b>{ $admin_id }</b></a>

    Назначен: <code>{ $created_on }</code>
    Последнее обновление: <code>{ $updated_on }</code>
admin-show-sudo = Права суперпользователя: { $sudo ->
        [0] ❌
        [1] ✅
        *[other] ❓
    }
admin-delete-text = 
    Вы уверены что хотите удалить пользователя <a href='tg://user?id={ $admin_id }'><b>{ $admin_id }</b></a> из списка администраторов?

    Права суперпользователя: { $sudo ->
        [0] ❌
        [1] ✅
        *[other] ❓
    }
    Назначен: <code>{ $created_on }</code>
    Последнее обновление: <code>{ $updated_on }</code>
admin-add-admin-request = Отправьте айди или выберите из списка пользователя, которого хотите назначить администратором
admin-error-user-id-is-invalid =
    Айди пользователя неверен!
    Отправьте айди или выберите из списка пользователя, которого хотите назначить администратором. 
    Айди можно узнать, например у бота @my_id_bot
admin-error-is-not-user-id =
    Пересланное сообщение было отправлено не пользователем!
    Отправьте айди или выберите из списка пользователя, которого хотите назначить администратором. 
    Айди можно узнать, например у бота @my_id_bot
admin-error-already-admin = Пользователь уже администратор
admin-add-admin-sudo-request = Назначить пользователя <a href='tg://user?id={ $admin_id }'><b>{ $admin_id }</b></a> суперпользователем?
admin-add-admin-confirm = Вы уверены что хотите добавить пользователя <a href='tg://user?id={ $admin_id }'><b>{ $admin_id }</b></a> в администраторы?
