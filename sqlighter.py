import sqlite3


class SQLighter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_users(self, is_on=True):
        """Получение всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `users` WHERE `is_on` = ?", (is_on,)).fetchall()

    def user_exists(self, user_id):
        """Проверка наличия юзера в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, mailing=True):
        """Добавление нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`, `filter_id` `mailing`) VALUES(?,?,?)",
                                       (user_id, mailing))

    def update_subscription(self, user_id, is_on):
        """Обновление статуса подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `is_on` = ? WHERE `user_id` = ?", (is_on, user_id))

    def get_active_filter(self, user_id, is_active=True):
        """Получение id активного фильтра"""
        with self.connection:
            filters = self.cursor.execute("SELECT * FROM `filters` WHERE `user_id` = ? AND `is_active` = ?",
                                          (user_id, is_active)).fetchall()
            filter_id = filters[0][0]
            return filter_id

    def get_filter(self, filter_id):
        """Получение фильра по его id"""
        with self.connection:
            selected_filter = self.cursor.execute("SELECT * FROM `filters` WHERE `filter_id` = ?",
                                                  (filter_id,)).fetchall()
            selected_filter = selected_filter[0]
            keys = self.cursor.execute('SELECT * FROM `filters`').description
            keys = [key[0] for key in keys]
            result = dict(zip(keys, selected_filter))
            return result

    def get_filters_ids(self, user_id):
        """Получение id всех фильтров пользователя"""
        with self.connection:
            filters = self.cursor.execute("SELECT * FROM `filters` WHERE `user_id` = ?", (user_id,)).fetchall()
            filters_id = []
            for elem in filters:
                filters_id.append(elem[0])
            return filters_id

    def change_active_filter(self, user_id, new_filter_id):
        """Изменение активного фильтра пользователя"""
        with self.connection:
            active_filter_id = self.get_active_filter(user_id)
            is_active = False
            self.cursor.execute("UPDATE `filters` SET `is_active` = ? WHERE `filter_id` = ?",
                                (is_active, active_filter_id,))
            new_is_active = True
            return self.cursor.execute("UPDATE `filters` SET `is_active` = ? WHERE `filter_id` = ?",
                                       (new_is_active, new_filter_id,))

    def insert_filter(self, user_id, filters):
        """Добавление нового фильтра"""
        with self.connection:
            filters['is_active'] = False
            self.cursor.execute("INSERT INTO `filters` (`user_id`, "
                                "`is_active`, "
                                "`lastkey`, "
                                "`filter_name`, "
                                "`ctl00$cphBody$ucRegion$ddlBoundList`, "
                                "`ctl00$cphBody$ucTradeType$ddlBoundList`, "
                                "`ctl00$cphBody$ucTradeStatus$ddlBoundList`, "
                                "`ctl00$cphBody$tbTradeObject`, "
                                "`ctl00$cphBody$txtTradeCode`)"
                                " VALUES(?,?,?,?,?,?,?,?)",
                                (user_id,
                                 filters['is_active'],
                                 filters['lastkey'],
                                 filters['filter_name'],
                                 filters['ctl00$cphBody$ucRegion$ddlBoundList'],
                                 filters['ctl00$cphBody$ucTradeType$ddlBoundList'],
                                 filters['ctl00$cphBody$ucTradeStatus$ddlBoundList'],
                                 filters['ctl00$cphBody$tbTradeObject'],
                                 filters['ctl00$cphBody$txtTradeCode'],
                                 ))
            new_filter_id = self.cursor.lastrowid
        return new_filter_id

    def get_lastkey(self, user_id):
        """Получение значения lastkey"""
        with self.connection:
            filter_id = self.get_active_filter(user_id)
            row = self.cursor.execute("SELECT * FROM `filters` WHERE `filter_id` = ?", (filter_id,)).fetchall()
            lastkey = row[0][3]
            return lastkey

    def update_lastkey(self, user_id, lastkey):
        """Обновление значения lastkey"""
        with self.connection:
            filter_id = self.get_active_filter(user_id)
            return self.cursor.execute("UPDATE `filters` SET `lastkey` = ? WHERE `filter_id` = ?", (lastkey, filter_id))

    def stop_mailing(self, user_id, mailing=False):
        """Остановка рассылки"""
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `mailing` = ? WHERE `user_id` = ?", (mailing, user_id))

    def start_mailing(self, user_id, mailing=True):
        """Включение рассылки"""
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `mailing` = ? WHERE `user_id` = ?", (mailing, user_id))

    def is_mailing(self, user_id):
        """Проверка статуса рассылки"""
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            result = result[0][1]
            return bool(result)

    def close(self):
        self.connection.close()
