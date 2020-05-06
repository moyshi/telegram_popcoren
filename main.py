import Tele
import yaml

with open('names1.yml', 'r') as date_b:
    dict_names = yaml.load(date_b)


@Tele.bot(chat_id=-1001053283203, filters='document')
def message(update):
    dict_names[update['document']['file_name'].split('.')[1].replace('פופקורן טיים ', '')] =\
        update['document']['file_id']
    Tele.send_document(-1001298973820, update['document']['file_id'])


@Tele.bot(chat_id=-1001298973820, filters='document')
def message(update):
    dict_names[update['document']['file_name'].split('.')[1].replace('פופקורן טיים ', '')] =\
        update['document']['file_id']


@Tele.bot('text')
def message(update):
    text = update['text']
    list_t = []
    for n in dict_names:
        if 10 > len(n) > 6:
            h = n[:-len(n) // 4:]
        elif 14 > len(n) > 9:
            h = n[:-len(n) // 3:]
        elif 17 > len(n) > 13:
            h = n[:-len(n) // 2:]
        elif 20 > len(n) > 16:
            h = n[:-len(n) // 2 - 2:]
        elif 24 > len(n) > 19:
            h = n[:-len(n) // 2 - 4:]
        elif len(n) > 23:
            h = n[:-len(n) // 2 - 6:]
        else:
            h = n
        if h in text:
            list_t.append(n)
    if len(list_t) == 1:
        Tele.send_document(update['chat']['id'], dict_names[list_t[0]], reply_to_message_id=str(update['message_id']))
    elif len(list_t) > 1:
        list_ms = []
        for t_n in list_t:
            list_ms.append([{t_n: t_n + '#1#' + str(update['message_id'])}])
        update.reply(text='מצאתי לך כמה סרטים בשם הזה אנא בחר',
                     reply_markup=Tele.InlineKeyboard(list_ms))


@Tele.bot('data')
def data(update):
    Tele.send_document(update['message']['chat']['id'],
                       dict_names[update['data'].split('#1#')[0]],
                       reply_to_message_id=update['data'].split('#1#')[1])


Tele.account('1088772965:AAGqPf0I78OxDH8bvqZ9eERmm-8mlxVJk-Q')
Tele.bot_run(multi=True)
