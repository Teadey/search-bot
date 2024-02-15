-none= Отсутствует
-query = Можете отправить свой запрос

register-password-request = Отправьте пароль для получения доступа к боту
register-password-invalid = Отправленный пароль неверен!
register-password-success = 
    Вы получили доступ к боту!
    { -query }

user-start-text = 
    Добро пожаловать!
    { -query }

user-search-not-available = Похоже, что этой записи уже нет
user-search-not-found = К сожалению ничего не нашлось по вашему запросу
user-search-result = 
    Вот что удалось найти по запросу "{ $query }"

    { -query }
user-search-detail = 
    Адрес: <i>{ $place }</i>
    Номер на стенде: <code>{ NUMBER($number, useGrouping: 0) }</code>
    Тип: <i>{ $tip }</i>
    Бирка: <i>{ $birka ->
        [0] { -none }
        *[other] { $birka }
    }</i>
    Комментарий: <i>{ $comment ->
        [0] { -none }
        *[other] { $comment }
    }</i>
    GPS: <i>{ $gps ->
        [0] { -none }
        *[other] { $gps }
    }</i>
    Номер коробки с дубликатом ключей: <i>{ $copy_box_number ->
        [0] { -none }
        *[other] { $copy_box_number }
    }</i>
user-search-comments = Комментарии к адресу <i>{ $place }</i>:
user-button-show-comments = Комментарии
user-button-add-comment = Добавить комментарий
user-button-refresh = Обновить 🔄
user-comment-request = Можете отправить свой комментарий
