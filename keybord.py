from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from smsactivate.api import SMSActivateAPI
from config import api_sms, chanals
from country import COUNRTY, name_service, full_name, COUNRTY_SMSMAN, name_service_smsman



def show_canals():
    keyword = InlineKeyboardMarkup(row_width=1)
    for chanal in chanals:
        btn = InlineKeyboardButton(text=chanal[0], url=chanal[2])
        keyword.insert(btn)
    btn_Done = InlineKeyboardButton('Я ПОДПИСАЛСЯ', callback_data='done')
    keyword.insert(btn_Done)
    return keyword

ikb_serv = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('SmsActivate', callback_data='sms_activate'),
     InlineKeyboardButton('SmsMan', callback_data='smsman')]
])

kb = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder='🍭 XAለVA')
kb1 = KeyboardButton('📨 Получить СМС')
kb2 = KeyboardButton('💼 Мой профиль')
kb3 = KeyboardButton('🍹 Информация')
kb.add(kb1).add(kb2,kb3)


kbb = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder='🍭 XAለVA')
kbb1 = KeyboardButton('📨 Получить СМС')
kbb2 = KeyboardButton('💼 Мой профиль')
kbb3 = KeyboardButton('🍹 Информация')
kb4 = KeyboardButton('1$ за подписку')
kb5 = KeyboardButton('💵 Заработать')
kbb.add(kbb1).add(kbb2,kbb3).add(kb4,kb5)


sms = SMSActivateAPI(api_sms)

def countryes_smsman(i):
    keyboard = InlineKeyboardMarkup(row_width=3)
    btn = []
    navigation = []
    i = int(i)
    stop = i + 15
    num = 0
    for ids in COUNRTY_SMSMAN:
        num += 1
        if i < num:
            if i < stop:
                country_name = COUNRTY_SMSMAN.get(ids)
                btn.append(InlineKeyboardMarkup(text=country_name,
                                                      callback_data=f'SMS_man|{ids}|{country_name}'))
                i += 1
    keyboard.add(*btn)
    if i > 15:
        navigation.append(InlineKeyboardButton(text='◀️', callback_data=f'NEXT_man|{i - 30}'))

    if len(btn) == 15:
        navigation.append(InlineKeyboardButton(text='➡️', callback_data=f'NEXT_man|{i}'))
    keyboard.add(*navigation)
    keyboard.add(InlineKeyboardButton(text='🔘 Меню', callback_data='back'))
    return keyboard


def countryes(i):
    keyboard = InlineKeyboardMarkup(row_width=3)
    btn = []
    navigation = []
    i = int(i)
    stop = i + 15
    num = 0
    for ids in COUNRTY:
        num += 1
        if i < num:
            if i < stop:
                country_name = COUNRTY.get(ids)
                btn.append(InlineKeyboardMarkup(text=country_name,
                                                      callback_data=f'set_c|{ids}|{country_name}'))
                i += 1
    keyboard.add(*btn)
    if i > 15:
        navigation.append(InlineKeyboardButton(text='◀️', callback_data=f'next_c|{i - 30}'))

    if len(btn) == 15:
        navigation.append(InlineKeyboardButton(text='➡️', callback_data=f'next_c|{i}'))
    keyboard.add(*navigation)
    keyboard.add(InlineKeyboardButton(text='🔘 Меню', callback_data='back'))
    return keyboard

def service_smsman(i, strana):
    keyboard = InlineKeyboardMarkup(row_width=3)
    btn = []
    navigation = []
    i = int(i)
    stop = i + 15
    num = 0
    for ids in name_service_smsman:
        num += 1
        if i < num:
            if i < stop:
                country_name = name_service_smsman.get(ids)
                btn.append(InlineKeyboardMarkup(text=country_name,
                                                      callback_data=f'set_Sm|{ids}|{country_name}|{strana}'))
                i += 1
    keyboard.add(*btn)
    if i > 15:

        navigation.append(InlineKeyboardButton(text='◀️', callback_data=f'next_Sm|{i - 30}|{strana}'))

    if len(btn) == 15:
        navigation.append(InlineKeyboardButton(text='➡️', callback_data=f'next_Sm|{i}|{strana}'))
    keyboard.add(*navigation)
    keyboard.add(InlineKeyboardButton(text='⤵ Меню', callback_data='back'))
    return keyboard

def service(i, strana):
    keyboard = InlineKeyboardMarkup(row_width=3)
    btn = []
    navigation = []

    i = int(i)
    stop = i + 15
    num = 0
    for ids in full_name:
        num += 1
        if i < num:
            if i < stop:
                country_name = full_name.get(ids)
                btn.append(InlineKeyboardMarkup(text=country_name,
                                                      callback_data=f'set_s_|{ids}|{country_name}|{strana}'))
                i += 1
    keyboard.add(*btn)
    if i > 15:

        navigation.append(InlineKeyboardButton(text='◀️', callback_data=f'next_s|{i - 30}|{strana}'))

    if len(btn) == 15:
        navigation.append(InlineKeyboardButton(text='➡️', callback_data=f'next_s|{i}|{strana}'))
    keyboard.add(*navigation)
    keyboard.add(InlineKeyboardButton(text='⤵ Меню', callback_data='back'))
    return keyboard

async def service_number_smsman( countri, service, price):
    ikb_phone = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('📲 Получить код', callback_data=f'PhoneSMS|{countri}|{service}|{price}')],
        [InlineKeyboardButton('⤵ Меню', callback_data='back')]

    ])
    return ikb_phone

async def service_number(service, id, price):
    ikb_phone = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('📲 Получить код', callback_data=f'phone|{service}|{id}|{price}')],
        [InlineKeyboardButton('⤵ Меню', callback_data='back')]

    ])
    return ikb_phone


ikb_money =InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('💰 Пополнить баланс', callback_data='go_pay')],
    [InlineKeyboardButton('⤵ Меню', callback_data='back')]
])



def sms_replay_smsman(id, price):
    ikb_sms =InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('🔁 Обновить', callback_data=f'man_sms|{id}|{price}')],
        # [InlineKeyboardButton('⛔ Завершить активацию', callback_data=f'man_ok|{id}')],
        [InlineKeyboardButton('✅ Подтвердить активацию', callback_data=f'man_nkay|{id}|{price}')],
        [InlineKeyboardButton('⚠ Номер уже использован', callback_data=f'man_not|{id}|{price}')],

    ])
    return ikb_sms


def sms_replay(number, id, price):
    ikb_sms =InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('🔁 Обновить', callback_data=f'go_sms|{number}|{id}|{price}')],
        [InlineKeyboardButton('⛔ Завершить активацию', callback_data=f'okay|{number}|{id}|{price}')],
        [InlineKeyboardButton('✅ Подтвердить активацию', callback_data=f'nkay|{number}|{id}|{price}')],
        [InlineKeyboardButton('⚠ Номер уже использован', callback_data=f'not|{number}|{id}|{price}')],

    ])
    return ikb_sms

ikb_payment =InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('🐳 Crypto Bot', callback_data='go_crypto')],
    [InlineKeyboardButton('⤵ Меню', callback_data='back')]
])

ikb_buttons =InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('1$ за подписку', callback_data='BUT|1$ за подписку')],
    [InlineKeyboardButton('💵 Заработать', callback_data='BUT|💵 Заработать')]
])

def add_but(buton):
    ikb_add_but =InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Да', callback_data=f'YES|{buton}')],
        [InlineKeyboardButton('Нет', callback_data=f'NO|{buton}')]
    ])
    return ikb_add_but

def kb_rassilka(buton, url):
    ikb_reklama = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(buton, url=url)],
    ])
    return ikb_reklama


def ikb_tips_buton(buton):
    ikb_tips =InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Текст', callback_data=f'Text|{buton}')],
        [InlineKeyboardButton('Фото', callback_data=f'Photo|{buton}')],
        [InlineKeyboardButton('Гифка', callback_data=f'Gif|{buton}')],
        [InlineKeyboardButton('Видео', callback_data=f'Video|{buton}')],
        [InlineKeyboardButton('Назад', callback_data='back_tip')]
    ])
    return ikb_tips

def oplata_kb(id: str, url: str, price):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.insert(InlineKeyboardButton(text='💰 Оплатить', url=url))
    kb.add(InlineKeyboardButton(text='🔄 Проверить', callback_data=f'check|{id}|{price}'))
    kb.add(InlineKeyboardButton(text='🔙Назад', callback_data='back'))
    return kb


kb_admin = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
kb1 = KeyboardButton('Количество пользователей')
kb2 = KeyboardButton('Рассылка')
kb3 = KeyboardButton('Общие пополнения')
kb4 = KeyboardButton('Настройка комиссии')
kb5 = KeyboardButton('Создание ссылки')
kb6 = KeyboardButton('Удалить все ссылки')
kb7 = KeyboardButton('Выход')
kb8 = KeyboardButton('Статистика ссылок')
kb9 = KeyboardButton('Включить ОП')
kb10 = KeyboardButton('Выключить ОП')
kb11 = KeyboardButton('ВКЛ (Заработать/Забрать)')
kb12 = KeyboardButton('ВЫКЛ (Заработать/Забрать)')
kb13 = KeyboardButton('Редактирование (Заработать/Забрать)')
kb_admin.add(kb1,kb2,kb3,kb4,kb5,kb6,kb8,kb9,kb10,kb11,kb12,kb13, kb7)




ikb_tip_rassilka = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Текст/Фото', callback_data='photo'),
     InlineKeyboardButton('Текст', callback_data='Texts')]
])

ikb_stop = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Выйти из режима ввода данных', callback_data='stop_input')]
])

