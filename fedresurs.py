import re
import time
import random

from lxml import html
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/89.0.4389.90 Safari/537.36"
}

URL = 'https://bankrot.fedresurs.ru/TradeList.aspx?attempt=1'

FORM_DATA = {
    'ctl00$PrivateOffice1$ctl00': 'ctl00$PrivateOffice1$ctl00|ctl00$cphBody$btnTradeSearch',
    'ctl00$PrivateOffice1$tbLogin': '',
    'ctl00$PrivateOffice1$tbPassword': '',
    'ctl00$PrivateOffice1$cbRememberMe': 'on',
    'ctl00$PrivateOffice1$tbEmailForPassword': '',
    'ctl00_PrivateOffice1_RadToolTip1_ClientState': '',
    'ctl00$DebtorSearch1$inputDebtor': 'поиск',
    'ctl00$cphBody$ucRegion$ddlBoundList': '',
    'ctl00$cphBody$mdsTradePlace$tbSelectedText': '',
    'ctl00$cphBody$mdsTradePlace$hfSelectedValue': '',
    'ctl00$cphBody$mdsTradePlace$hfSelectedType': '',
    'ctl00$cphBody$ucTradeType$ddlBoundList': '',
    'ctl00$cphBody$mdsDebtor$tbSelectedText': '',
    'ctl00$cphBody$mdsDebtor$hfSelectedValue': '',
    'ctl00$cphBody$mdsDebtor$hfSelectedType': '',
    'ctl00$cphBody$ucTradeStatus$ddlBoundList': '',
    'ctl00$cphBody$mdsArmTO$tbSelectedText': '',
    'ctl00$cphBody$mdsArmTO$hfSelectedValue': '',
    'ctl00$cphBody$mdsArmTO$hfSelectedType': '',
    'ctl00$cphBody$ucPropertyCategoriesSelect$tbSelectedText': '',
    'ctl00$cphBody$ucPropertyCategoriesSelect$hfSelectedValue': '',
    'ctl00$cphBody$ucPropertyCategoriesSelect$hfSelectedType': '',
    'ctl00$cphBody$tbTradeObject': '',
    'ctl00$cphBody$txtTradeCode': '',
    'ctl00$cphBody$cldrBeginDate$tbSelectedDate': '',
    'ctl00$cphBody$cldrBeginDate$tbSelectedDateValue': '',
    'ctl00$cphBody$cldrEndDate$tbSelectedDate': '',
    'ctl00$cphBody$cldrEndDate$tbSelectedDateValue': '',
    '__ASYNCPOST': 'true',
}


# typecasting filters to form
def decode_filters_region(my_filters):
    region = "ctl00$cphBody$ucRegion$ddlBoundList"

    out_filter = my_filters
    out_filter[region] = my_filters.pop('Регион')
    if out_filter[region] == 'Алтайский край':
        reg_val = 1
    elif out_filter[region] == 'Амурская область':
        reg_val = 10
    elif out_filter[region] == 'Архангельская область':
        reg_val = 11
    elif out_filter[region] == 'Астраханская область':
        reg_val = 12
    elif out_filter[region] == 'Белгородская область':
        reg_val = 14
    elif out_filter[region] == 'Брянская область':
        reg_val = 15
    elif out_filter[region] == 'Владимирская область':
        reg_val = 17
    elif out_filter[region] == 'Волгоградская область':
        reg_val = 18
    elif out_filter[region] == 'Вологодская область':
        reg_val = 19
    elif out_filter[region] == 'Воронежская область':
        reg_val = 20
    elif out_filter[region] == 'г. Москва':
        reg_val = 45
    elif out_filter[region] == 'г. Санкт-Петербург':
        reg_val = 40
    elif out_filter[region] == 'г. Севастополь':
        reg_val = 201
    elif out_filter[region] == 'Еврейская автономная область':
        reg_val = 99
    elif out_filter[region] == 'Забайкальский край':
        reg_val = 101
    elif out_filter[region] == 'Ивановская область':
        reg_val = 24
    elif out_filter[region] == 'Иные территории, включая г.Байконур':
        reg_val = 203
    elif out_filter[region] == 'Иркутская область':
        reg_val = 25
    elif out_filter[region] == 'Кабардино-Балкарская Республика':
        reg_val = 83
    elif out_filter[region] == 'Калининградская область':
        reg_val = 27
    elif out_filter[region] == 'Калужская область':
        reg_val = 29
    elif out_filter[region] == 'Камчатский край':
        reg_val = 30
    elif out_filter[region] == 'Карачаево-Черкесская Республика':
        reg_val = 91
    elif out_filter[region] == 'Кемеровская область':
        reg_val = 32
    elif out_filter[region] == 'Кировская область':
        reg_val = 33
    elif out_filter[region] == 'Костромская область':
        reg_val = 34
    elif out_filter[region] == 'Краснодарский край':
        reg_val = 3
    elif out_filter[region] == 'Красноярский край':
        reg_val = 4
    elif out_filter[region] == 'Курганская область':
        reg_val = 37
    elif out_filter[region] == 'Курская область':
        reg_val = 38
    elif out_filter[region] == 'Ленинградская область':
        reg_val = 41
    elif out_filter[region] == 'Липецкая область':
        reg_val = 42
    elif out_filter[region] == 'Магаданская область':
        reg_val = 44
    elif out_filter[region] == 'Московская область':
        reg_val = 46
    elif out_filter[region] == 'Мурманская область':
        reg_val = 47
    elif out_filter[region] == 'Ненецкий автономный округ':
        reg_val = 200
    elif out_filter[region] == 'Нижегородская область':
        reg_val = 22
    elif out_filter[region] == 'Новгородская область':
        reg_val = 49
    elif out_filter[region] == 'Новосибирская область':
        reg_val = 50
    elif out_filter[region] == 'Омская область':
        reg_val = 52
    elif out_filter[region] == 'Оренбургская область':
        reg_val = 53
    elif out_filter[region] == 'Орловская область':
        reg_val = 54
    elif out_filter[region] == 'Пензенская область':
        reg_val = 56
    elif out_filter[region] == 'Пермский край':
        reg_val = 57
    elif out_filter[region] == 'Приморский край':
        reg_val = 5
    elif out_filter[region] == 'Псковская область':
        reg_val = 58
    elif out_filter[region] == 'Республика Адыгея':
        reg_val = 79
    elif out_filter[region] == 'Республика Алтай':
        reg_val = 84
    elif out_filter[region] == 'Республика Башкортостан':
        reg_val = 80
    elif out_filter[region] == 'Республика Бурятия':
        reg_val = 81
    elif out_filter[region] == 'Республика Дагестан':
        reg_val = 82
    elif out_filter[region] == 'Республика Ингушетия':
        reg_val = 26
    elif out_filter[region] == 'Республика Калмыкия':
        reg_val = 85
    elif out_filter[region] == 'Республика Карелия':
        reg_val = 86
    elif out_filter[region] == 'Республика Коми':
        reg_val = 87
    elif out_filter[region] == 'Республика Крым':
        reg_val = 202
    elif out_filter[region] == 'Республика Марий Эл':
        reg_val = 88
    elif out_filter[region] == 'Республика Мордовия':
        reg_val = 89
    elif out_filter[region] == 'Республика Саха (Якутия)':
        reg_val = 98
    elif out_filter[region] == 'Республика Северная Осетия - Алания':
        reg_val = 102
    elif out_filter[region] == 'Республика Татарстан':
        reg_val = 92
    elif out_filter[region] == 'Республика Тыва':
        reg_val = 93
    elif out_filter[region] == 'Республика Хакасия':
        reg_val = 95
    elif out_filter[region] == 'Ростовская область':
        reg_val = 60
    elif out_filter[region] == 'Рязанская область':
        reg_val = 61
    elif out_filter[region] == 'Самарская область':
        reg_val = 36
    elif out_filter[region] == 'Саратовская область':
        reg_val = 63
    elif out_filter[region] == 'Сахалинская область':
        reg_val = 64
    elif out_filter[region] == 'Свердловская область':
        reg_val = 65
    elif out_filter[region] == 'Смоленская область':
        reg_val = 66
    elif out_filter[region] == 'Ставропольский край':
        reg_val = 7
    elif out_filter[region] == 'Тамбовская область':
        reg_val = 68
    elif out_filter[region] == 'Тверская область':
        reg_val = 28
    elif out_filter[region] == 'Томская область':
        reg_val = 69
    elif out_filter[region] == 'Тульская область':
        reg_val = 70
    elif out_filter[region] == 'Тюменская область':
        reg_val = 71
    elif out_filter[region] == 'Удмуртская Республика':
        reg_val = 94
    elif out_filter[region] == 'Ульяновская область':
        reg_val = 73
    elif out_filter[region] == 'Хабаровский край':
        reg_val = 8
    elif out_filter[region] == 'Ханты-Мансийский автономный округ - Югра':
        reg_val = 103
    elif out_filter[region] == 'Челябинская область':
        reg_val = 75
    elif out_filter[region] == 'Чеченская Республика':
        reg_val = 96
    elif out_filter[region] == 'Читинская область':
        reg_val = 76
    elif out_filter[region] == 'Чувашская Республика - Чувашия':
        reg_val = 97
    elif out_filter[region] == 'Чукотский автономный округ':
        reg_val = 77
    elif out_filter[region] == 'Ямало-Ненецкий автономный округ':
        reg_val = 104
    elif out_filter[region] == 'Ярославская область':
        reg_val = 78
    else:
        reg_val = ''

    out_filter[region] = reg_val

    return out_filter


def decode_filters_tradetype(my_filters):
    tradetype = 'ctl00$cphBody$ucTradeType$ddlBoundList'
    out_filter = my_filters
    out_filter[tradetype] = my_filters.pop('Вид торгов')
    if out_filter[tradetype] == 'Открытый аукцион':
        type_val = 1
    elif out_filter[tradetype] == 'Открытый конкурс':
        type_val = 2
    elif out_filter[tradetype] == 'Публичное предложение':
        type_val = 3
    elif out_filter[tradetype] == 'Закрытый аукцион':
        type_val = 5
    elif out_filter[tradetype] == 'Закрытый конкурс':
        type_val = 6
    elif out_filter[tradetype] == 'Закрытое публичное предложение':
        type_val = 7
    else:
        type_val = ''

    out_filter[tradetype] = type_val
    return out_filter


def decode_filters_status(my_filters):
    status = 'ctl00$cphBody$ucTradeStatus$ddlBoundList'
    out_filter = my_filters
    out_filter[status] = my_filters.pop('Статус')
    if out_filter[status] == 'На рассмотрении':
        stat_val = 1
    elif out_filter[status] == 'Объявлены торги':
        stat_val = 2
    elif out_filter[status] == 'Открыт прием заявок':
        stat_val = 3
    elif out_filter[status] == 'Прием заявок завершен':
        stat_val = 4
    elif out_filter[status] == 'Идут торги':
        stat_val = 5
    elif out_filter[status] == 'Завершенные':
        stat_val = 6
    elif out_filter[status] == 'Аннулированные':
        stat_val = 9
    elif out_filter[status] == 'Торги отменены':
        stat_val = 10
    elif out_filter[status] == 'Торги не состоялись':
        stat_val = 11
    elif out_filter[status] == 'Торги приостановлены':
        stat_val = 13
    else:
        stat_val = ''

    out_filter[status] = stat_val
    return out_filter


def decode_filters_keywords(my_filters):
    keywords = 'ctl00$cphBody$tbTradeObject'
    out_filter = my_filters
    keywords_val = my_filters['Ключевые слова']
    out_filter[keywords] = my_filters.pop('Ключевые слова')

    out_filter[keywords] = keywords_val
    return out_filter


def decode_filters_tradecode(my_filters):
    tradecode = 'ctl00$cphBody$txtTradeCode'
    out_filter = my_filters
    tradecode_val = my_filters['Номер торгов']
    out_filter[tradecode] = my_filters.pop('Номер торгов')

    out_filter[tradecode] = tradecode_val
    return out_filter


def form_filters(my_filters):
    if my_filters['Регион']:
        my_filters.update(decode_filters_region(my_filters))
    if my_filters['Вид торгов']:
        my_filters.update(decode_filters_tradetype(my_filters))
    if my_filters['Номер торгов']:
        my_filters.update(decode_filters_tradecode(my_filters))
    if my_filters['Ключевые слова']:
        my_filters.update(decode_filters_keywords(my_filters))
    if my_filters['Статус']:
        my_filters.update(decode_filters_status(my_filters))


# posting request with filter data
def post_filters_form(my_filters):
    with requests.Session() as session:
        content = session.post(URL, headers=HEADERS, data=FORM_DATA).text
        soup = BeautifulSoup(content, 'html.parser')
        time.sleep(random.randrange(2, 4))

        my_filters['__VIEWSTATE'] = soup.find('input', attrs={'id': '__VIEWSTATE'})['value']
        my_filters['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'id': '__VIEWSTATEGENERATOR'})['value']
        my_filters['__PREVIOUSPAGE'] = soup.find('input', attrs={'id': '__PREVIOUSPAGE'})['value']
        my_filters['__EVENTVALIDATION'] = soup.find('input', attrs={'id': '__EVENTVALIDATION'})['value']
        my_filters['ctl00$cphBody$btnTradeSearch.x'] = random.randrange(1, 99)
        my_filters['ctl00$cphBody$btnTradeSearch.y'] = random.randrange(1, 99)

        print("Applying filters")
        time.sleep(random.randrange(3, 7))
        form_filters(my_filters)
        form = FORM_DATA
        form.update(my_filters)

        response = session.post(URL, headers=HEADERS, data=form)
        content = response.text
        return content


# parsing content
# parsing main table
def get_trade_list(src):
    soup = BeautifulSoup(src, 'html.parser')
    time.sleep(random.randrange(2, 4))

    rows = soup.find('table', attrs={'id': 'ctl00_cphBody_gvTradeList'}).find_all('tr')
    thead = soup.find('table', attrs={'id': 'ctl00_cphBody_gvTradeList'}).find_all('th')

    keys = []

    for elem in range(len(thead)):
        keys.append(thead[elem].text.strip().lower())

    content = []
    for row in rows:
        i = 0
        values = []
        for elem in row.find_all('td'):
            values.append(elem.text.strip())
            i += 1
            if i == 8:
                item = dict(zip(keys, values))
                content.append(item)
    return content


# decorate percentage data
def init_percentage_data(total, data):
    if data == '-':
        data = 'Не указано'
        data_num = 'Не указано'
    else:
        if re.search('руб', data):
            data = re.sub('руб', "", data)
            if data[-1] == ".":
                data = data[:-1].strip()
            data_num = data.replace(' ', '').replace(',', '.')
            data_num = float(data_num)
            data = "Не указано"
        else:
            data = re.sub(r"%", "", data).replace(' ', '').replace(',', '.')
            data = float(data)
            data_num = (total * data) / 100
    return data, data_num


# decorate receiver info
def init_receiver_info(data):
    receiver_info = '-'
    if len(data) == 1:
        receiver_info = data[0]
    elif len(data) == 0:
        receiver_info = 'Нет информации'
    else:
        for i in range(len(data) - 1):
            if data[i] != data[i + 1]:
                receiver_info = 'Уточняйте на сайте'
            else:
                receiver_info = data[0]
    return receiver_info


# parser
class Bankrot:
    host = "https://bankrot.fedresurs.ru"
    url = 'https://bankrot.fedresurs.ru/TradeList.aspx?attempt=1'
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) "
                      "Chrome/89.0.4389.90 Safari/537.36 "
    }

    lastkey = ""

    def __init__(self, lastkey):
        self.lastkey = lastkey

    def new_records(self, form=FORM_DATA):
        content = self.get_page_src(form)
        new = []
        items = get_trade_list(content)
        for i in range(len(items)):
            key = items[i]['номер торгов']
            if self.lastkey != key:
                new.append(content[i])

        return new

    def get_lastkey(self, form=FORM_DATA):
        content = self.get_page_src(form)
        content = get_trade_list(content)
        key = content[0]['номер торгов']
        return str(key)

    def update_lastkey(self, new_key):
        self.lastkey = new_key

        with open(self.lastkey_file, "r+") as f:
            f.seek(0)
            f.write(str(new_key))
            f.truncate()

        return new_key

    def get_page_src(self, form=FORM_DATA):
        if form == FORM_DATA:
            print('Setting cookies...')
            time.sleep(random.randrange(2, 5))

            response = requests.post(self.url, headers=self.headers, data=form)
            page_source = response.text
        else:
            page_source = post_filters_form(form)
        return page_source

    def get_record(self, rec_num, my_filters=FORM_DATA):

        content = self.get_page_src(my_filters)

        print(f"Getting data of record №{rec_num + 1}... Step 1/2.")
        time.sleep(random.randrange(1, 3))

        tree = html.fromstring(content)
        trade_cards = tree.xpath('//a[@title="Полная информация о торгах"]')
        time.sleep(random.randrange(2, 4))

        uri = trade_cards[rec_num].attrib["href"]

        data = my_filters
        soup = BeautifulSoup(content, 'html.parser')
        time.sleep(random.randrange(2, 4))

        data['__VIEWSTATE'] = soup.find('input', attrs={'id': '__VIEWSTATE'})['value']
        data['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'id': '__VIEWSTATEGENERATOR'})['value']
        data['__PREVIOUSPAGE'] = soup.find('input', attrs={'id': '__PREVIOUSPAGE'})['value']

        print(f"Getting data of record №{rec_num + 1}... Step 2/2.")

        time.sleep(random.randrange(2, 5))
        print("Forming response...")
        response = requests.post(self.host + uri, headers=self.headers, data=data)
        rec_source = response.text
        return rec_source

    def get_record_details(self, src, my_filters=FORM_DATA):
        soup = BeautifulSoup(src, 'html.parser')
        time.sleep(random.randrange(2, 4))

        uri = soup.find('table', attrs={'id': 'ctl00_cphBody_tableTradeInfo'}).find('a', attrs={
            'id': 'ctl00_cphBody_hlMessageLink'}).get_attribute_list('onclick')
        uri = uri[0].split(",")
        uri = re.search(r"/.*'", uri[0]).group()[:-1]
        time.sleep(random.randrange(2, 4))

        item_num = soup.find('div', attrs={'style': 'font-weight: bold; margin: 0px 10px 10px 10px;'}).get_text(
            strip=True)
        item_num = item_num.split()[-1]

        data = my_filters

        data['__VIEWSTATE'] = soup.find('input', attrs={'id': '__VIEWSTATE'})['value']
        data['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'id': '__VIEWSTATEGENERATOR'})['value']
        data['__PREVIOUSPAGE'] = soup.find('input', attrs={'id': '__PREVIOUSPAGE'})['value']

        response = requests.post(self.host + uri, headers=self.headers, data=data)
        details_source = response.text

        return details_source, item_num

    def form_record_info(self, src, item_num, rec_num, form=FORM_DATA):
        soup = BeautifulSoup(src, 'html.parser')
        time.sleep(random.randrange(2, 4))
        rows = soup.find('table', class_='lotInfo').find_all('tr', class_='odd')

        content = self.get_page_src(form)
        content = get_trade_list(content)

        debtor = soup.find_all('table', class_='headInfo')
        debtor = debtor[1].find('tr').find_all('td')
        debtor_type = debtor[0].get_text().split()[0]
        debtor = content[rec_num]['должник']

        platform = content[rec_num]['площадка']
        date = content[rec_num]['дата торгов']

        r = re.compile('^[а-яА-Я]+$')
        receiver_name = soup.find_all('table', class_='headInfo')[2].find('tr').find_all('td')
        if receiver_name[0].get_text(strip=True).split()[0] == 'Арбитражный':
            receiver_name = receiver_name[1].get_text(strip=True).split()
            receiver_name = [elem for elem in filter(r.match, receiver_name)]
            receiver_name = receiver_name[:3]
            receiver_name = ' '.join(receiver_name)
        else:
            receiver_name = receiver_name[1].get_text(strip=True)

        info_box = soup.find_all('div', class_='msg')
        if re.search('Текст', info_box[0].get_text()):
            info_box = info_box[0].text
        else:
            info_box = info_box[1].text
        email_pattern = re.compile("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+")
        emails = re.findall(email_pattern, info_box)

        for i in range(len(emails)):
            if emails[i][-1] == '.' or emails[i][-1] == ')':
                emails[i] = emails[i][:-1]

        receiver_email = init_receiver_info(emails)

        num_pattern = re.compile(r"\b\+?[7,8][- (]*\d{3}[- )]*\d{3}[- ]*\d{2}[- ]*\d{2}\b", re.S)
        nums = re.findall(num_pattern, info_box)

        receiver_num = init_receiver_info(nums)

        start_price = "Нет информации"
        description = "Нет информации"
        step_price = "Нет информации"
        step_price_num = "Нет информации"
        deposit = "Нет информации"
        deposit_num = "Нет информации"

        if debtor_type == "Наименование":
            debtor_type = "Юридическое лицо"
        elif debtor_type == "ФИО":
            debtor_type = "Физическое лицо"
        else:
            debtor_type = "Не определено"

        for row in rows:
            cells = row.find_all('td')
            if cells[0].get_text() == item_num:
                start_price = float(cells[2].get_text().replace(' ', '').replace(',', '.'))
                step_price, step_price_num = init_percentage_data(start_price, cells[3].get_text())
                deposit, deposit_num = init_percentage_data(start_price, cells[4].get_text())
                description = re.sub(r'<br/>', '\n', cells[1].get_text())
                description = re.sub(r'\s+', ' ', description)

        item = {
            'Тип должника': debtor_type,
            'Должник': debtor,
            'Описание': description,
            'Начальная цена': start_price,
            'Форма торгов': content[rec_num]['вид торгов'],
            'Дата торгов': date,
            'Площадка': platform,
            'Шаг аукциона в процентах': step_price,
            'Шаг аукциона': step_price_num,
            'Задаток в процентах': deposit,
            'Задаток': deposit_num,
            'Арбитражный управляющий': receiver_name,
            'Email АУ': receiver_email,
            'Тел. АУ': receiver_num,
        }

        keys = item.keys()
        for elem in keys:
            print(f'{elem}: {item.get(elem)}')

        return item

    def get_rec_info(self, rec_id, my_filters=FORM_DATA):
        my_filters['ctl00$cphBody$txtTradeCode'] = rec_id
        content = self.get_record(rec_num=0, my_filters=my_filters)
        tr_content = get_trade_list(content)

        det_src, item_num = self.get_record_details(content, my_filters)
        soup = BeautifulSoup(det_src, 'html.parser')
        rows = soup.find('table', class_='lotInfo').find_all('tr', class_='odd')

        debtor = soup.find_all('table', class_='headInfo')
        debtor = debtor[1].find('tr').find_all('td')
        debtor_type = debtor[0].get_text().split()[0]
        debtor = tr_content[0]['должник']

        platform = tr_content[0]['площадка']
        date = tr_content[0]['дата торгов']

        r = re.compile('^[а-яА-Я]+$')
        receiver_name = soup.find_all('table', class_='headInfo')[2].find('tr').find_all('td')
        if receiver_name[0].get_text(strip=True).split()[0] == 'Арбитражный':
            receiver_name = receiver_name[1].get_text(strip=True).split()
            receiver_name = [elem for elem in filter(r.match, receiver_name)]
            receiver_name = receiver_name[:3]
            receiver_name = ' '.join(receiver_name)
        else:
            receiver_name = receiver_name[1].get_text(strip=True)

        info_box = soup.find_all('div', class_='msg')
        if re.search('Текст', info_box[0].get_text()):
            info_box = info_box[0].text
        else:
            info_box = info_box[1].text
        email_pattern = re.compile("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+")
        emails = re.findall(email_pattern, info_box)

        for i in range(len(emails)):
            if emails[i][-1] == '.' or emails[i][-1] == ')':
                emails[i] = emails[i][:-1]

        receiver_email = init_receiver_info(emails)

        num_pattern = re.compile(r"\b\+?[7,8][- (]*\d{3}[- )]*\d{3}[- ]*\d{2}[- ]*\d{2}\b", re.S)
        nums = re.findall(num_pattern, info_box)

        receiver_num = init_receiver_info(nums)

        start_price = "Нет информации"
        description = "Нет информации"
        step_price = "Нет информации"
        step_price_num = "Нет информации"
        deposit = "Нет информации"
        deposit_num = "Нет информации"

        if debtor_type == "Наименование":
            debtor_type = "Юридическое лицо"
        elif debtor_type == "ФИО":
            debtor_type = "Физическое лицо"
        else:
            debtor_type = "Не определено"

        for row in rows:
            cells = row.find_all('td')
            if cells[0].get_text() == item_num:
                start_price = float(cells[2].get_text().replace(' ', '').replace(',', '.'))
                step_price, step_price_num = init_percentage_data(start_price, cells[3].get_text())
                deposit, deposit_num = init_percentage_data(start_price, cells[4].get_text())
                description = re.sub(r'<br/>', '\n', cells[1].get_text())
                description = re.sub(r'\s+', ' ', description)

        item = {
            'Тип должника': debtor_type,
            'Должник': debtor,
            'Описание': description,
            'Начальная цена': start_price,
            'Форма торгов': tr_content[0]['вид торгов'],
            'Дата торгов': date,
            'Площадка': platform,
            'Шаг аукциона в процентах': step_price,
            'Шаг аукциона': step_price_num,
            'Задаток в процентах': deposit,
            'Задаток': deposit_num,
            'Арбитражный управляющий': receiver_name,
            'Email АУ': receiver_email,
            'Тел. АУ': receiver_num,
        }

        return item
