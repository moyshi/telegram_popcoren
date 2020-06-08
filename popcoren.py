import Tele
import yaml
import io

with open('names1.yml', 'r') as date_b:
    dict_names, dict_id = yaml.load(date_b)


@Tele.bot(chat_id=-1001053283203, filters='document')
def message(update):
    if update['document']['file_unique_id'] not in dict_id:
        dict_names[update['document']['file_name'].split('.')[0].replace('פופקורן טיים ', '')] =\
            update['document']['file_id']
        Tele.send_document(-1001298973820,
                           update['document']['file_id'],
                           caption=update['document']['file_name'].split('.')[1].replace('פופקורן טיים ', ''))
    with io.open('names1.yml', 'w', encoding='utf8') as outfile:
        yaml.dump([dict_names, dict_id], outfile)


@Tele.bot(chat_id=694895985, filters='caption')
def message(update):
    if update['document']['file_unique_id'] in dict_id:
        del dict_names[dict_id[update['document']['file_unique_id']]]
        dict_names[update['caption']] =\
            update['document']['file_id']
        dict_id[update['document']['file_unique_id']] =\
            update['caption']
    else:
        dict_names[update['caption']] =\
            update['document']['file_id']
        dict_id[update['document']['file_unique_id']] =\
            update['caption']
    with io.open('names1.yml', 'w', encoding='utf8') as outfile:
        yaml.dump([dict_names, dict_id], outfile)


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
            for mmil in text.split():
                if mmil in h:
                    list_t.append(n)
                    break
    if len(list_t) == 1:
        Tele.send_document(update['chat']['id'], dict_names[list_t[0]], reply_to_message_id=str(update['message_id']))
    elif len(list_t) > 1:
        list_ms = []
        for t_n in list_t:
            list_ms.append([{t_n: t_n + '#1#' + str(update['message_id']) + '#1#' + str(update['from']['id'])}])
        update.reply(text='מצאתי לך כמה סרטים בשם הזה אנא בחר',
                     reply_markup=Tele.InlineKeyboard(list_ms))


@Tele.bot('data')
def data(update):
    if str(update['from']['id']) == update['data'].split('#1#')[2]:
        Tele.send_document(update['message']['chat']['id'],
                           dict_names[update['data'].split('#1#')[0]],
                           reply_to_message_id=update['data'].split('#1#')[1])
        Tele.delete_message(update['message']['chat']['id'], update['message']['message_id'])


Tele.account('1088772965:AAGqPf0I78OxDH8bvqZ9eERmm-8mlxVJk-Q')
Tele.bot_run(multi=True)
