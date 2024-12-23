import asyncio
import json
import aiogram
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from config import *
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import *
from keybord import *
from smsactivate.api import SMSActivateAPI
from country import *
import requests
from CryptoPayAPI.CryptoPay import CryptoPay


cryptopay = CryptoPay(token=api_cryptobot)
sms = SMSActivateAPI(api_sms)

storage = MemoryStorage()
bot = Bot(token, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота")
    ])

class CheksSub(BaseMiddleware):
    async def on_process_callback_query(self, callback: types.CallbackQuery, data: dict):
        db_admin()

        if op_chek() == 0:
            pass

        else:
            if await chec_shanel(channels=chanals, user=callback.from_user.id):
                pass
            else:
                await callback.message.answer('Для того чтобы пользоваться нашим ботом, подпишитесь на каналы', reply_markup=show_canals())
                raise CancelHandler

    async def on_process_message(self, message: types.Message, data: dict):
        db_admin()

        if op_chek() == 0:
            pass
        else:
            if await chec_shanel(channels=chanals, user=message.from_user.id):
                pass
            else:
                await message.answer('Для того чтобы пользоваться нашим ботом, подпишитесь на каналы',
                                              reply_markup=show_canals())
                raise CancelHandler




async def RUB():
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    return round(float(data['Valute']['USD']['Value']), 2)


#Проверка подписки
async def chec_shanel(channels, user):
    db_admin()

    if op_chek() == 0:
        pass
    for channal in channels:
        chat_member = await bot.get_chat_member(chat_id=channal[1], user_id=user)
        if chat_member['status'] == 'left':
            return False
    return True

@dp.callback_query_handler(text='stop_input', state='*')
async def stop_input(callback: types.CallbackQuery, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await callback.message.edit_text('Вы вышли из режима ввода данных')





@dp.message_handler(commands=['Start'], state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    if message.chat.type == 'private':
        db_admin()
        db_start()
        db_url_ref()

        sym = message.text.split()[-1]
        run_update(sym)
        if op_chek() == 0:
            if chek_buttons() == 0:
                markup = kb
                with open('Halwa.jpg', 'rb') as photo:
                    await bot.send_photo(chat_id=message.from_user.id,
                                         photo=photo,
                                           caption='Добро пожаловать в бот для приема смс от различных сервисов\n'
                                                'Вы находитесь в главном меню', reply_markup=markup, parse_mode='HTML')
            else:
                markup = kbb
                with open('Halwa.jpg', 'rb') as photo:
                    await bot.send_photo(chat_id=message.from_user.id,
                                         photo=photo,
                                           caption='Добро пожаловать в бот для приема смс от различных сервисов\n'
                                                'Вы находитесь в главном меню', reply_markup=markup, parse_mode='HTML')
            if not user_exists(message.from_user.id):
                if message.from_user.username != None:
                    add_users(message.from_user.id)
                else:
                    add_users(message.from_user.id)
        else:
            if await chec_shanel(channels=chanals, user=message.from_user.id):
                with open('Halwa.jpg', 'rb') as photo:
                    await bot.send_photo(chat_id=message.from_user.id,
                                         photo=photo,
                                           caption='Добро пожаловать в бот для приема смс от различных сервисов\n'
                                                'Вы находитесь в главном меню', reply_markup=kb, parse_mode='HTML')
                if not user_exists(message.from_user.id):
                    if message.from_user.username != None:
                        add_users(message.from_user.id)
                    else:
                        add_users(message.from_user.id)

            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Для того чтобы пользоваться нашим ботом, подпишитесь на каналы',
                                       reply_markup=show_canals())

@dp.message_handler(text='🍹 Информация')
async def profile(message: types.Message):
    await message.answer('В данном разделе вы можете узнать следующее:\n'
                         '📃 Правила | https://telegra.ph/Pravila-magazina-09-20\n'
                         '🍹 Администрация | https://t.me/quant_pzdc\n'
                         '🛠️ Тех поддержка | https://t.me/xalvahelp\n'
                         '👹 Все проекты | https://t.me/xalvaproject1', disable_web_page_preview=True)

@dp.message_handler(text='💼 Мой профиль')
async def profile(message: types.Message):
    balance = chek_balance(message.from_user.id)
    await message.answer(f'👤 <b>Личный кабинет {message.from_user.first_name}</b>\n\n'
                         f'🆔 <b>ID:</b> <code>{message.from_user.id}</code>\n'
                         f'💸  <b>Баланс:</b> <code>{float(balance[0])}</code> Руб', parse_mode='HTML', reply_markup=ikb_money)


@dp.callback_query_handler(text='back')
async def pay(callback: types.CallbackQuery):
    await callback.message.edit_caption(
                           caption='Добро пожаловать в бот для приема смс от различных сервисов\n'
                                'Вы находитесь в главном меню',
                           parse_mode='HTML')


@dp.callback_query_handler(text='go_pay')
async def pay(callback: types.CallbackQuery):

    await callback.message.edit_text('Выберите платежную систему', reply_markup=ikb_payment)

class User_pay(StatesGroup):
    amount = State()

@dp.callback_query_handler(text='go_crypto')
async def pay(callback: types.CallbackQuery):
    await callback.message.edit_text('Укажите сумму пополнения\n'
                                     'Минимальная сумма пополнения: 0.1$', reply_markup=ikb_stop)
    await User_pay.amount.set()

@dp.message_handler(state=User_pay.amount)
async def fsm(message:types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text

    invoce = cryptopay.create_invoice(asset='USDT',
                                       amount=float(data['amount']),
                                       description='Пополнение баланса')


    await message.answer(f'Сумма к оплате {data["amount"]}$\n'
                         f'Пополнять в USDT', reply_markup=oplata_kb(id=invoce.invoice_id, url=invoce.pay_url, price=invoce.amount))
    await state.finish()

@dp.callback_query_handler(text_startswith='check')
async def cheks(callback: types.CallbackQuery):
    id_pay = callback.data.split('|')[1]
    amount = callback.data.split('|')[2]
    invoce = cryptopay.get_invoices()
    kurs = await RUB()

    info_komsa = komsa_chek()[0]

    if info_komsa == None:
        info_komsa = add_komsa()





    res = int(kurs) * int(amount)
    komsa = float(res) / 100 * int(info_komsa)
    result = float(res) - float(komsa)



    for i in invoce:
        if str(i.invoice_id) == str(id_pay):
            if i.status != 'paid':
                await callback.answer('Счет не оплачен', show_alert=True)
            else:
                add_balances(callback.from_user.id, result)
                add_all_balances(result)
                await callback.message.edit_text(f'Счет успешно оплачен, на баланс зачислено {res} Руб')
                await bot.send_message(ADMIN, f'Пользователь @{callback.from_user.username} успешно пополнил баланс на сумму {res}р')



@dp.callback_query_handler(text='done')
async def chek_subs(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if await chec_shanel(channels=chanals, user=message.from_user.id):
        if chek_buttons() == 0:
            markup = kb
            with open('Halwa.jpg', 'rb') as photo:
                await bot.send_photo(chat_id=message.from_user.id,
                                     photo=photo,
                                     caption='Добро пожаловать в бот для приема смс от различных сервисов\n'
                                             'Вы находитесь в главном меню', reply_markup=markup, parse_mode='HTML')
        else:
            markup = kbb
            with open('Halwa.jpg', 'rb') as photo:
                await bot.send_photo(chat_id=message.from_user.id,
                                     photo=photo,
                                     caption='Добро пожаловать в бот для приема смс от различных сервисов\n'
                                             'Вы находитесь в главном меню', reply_markup=markup, parse_mode='HTML')

        if not user_exists(message.from_user.id):
            if message.from_user.username != None:
                add_users(message.from_user.id)
            else:
                add_users(message.from_user.id)

    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Для того чтобы пользоваться нашим ботом, подпишитесь на каналы',
                               reply_markup=show_canals())




@dp.callback_query_handler(text_contains ='next_c', state='*')
async def next_country(call: types.CallbackQuery):

    i = call.data.split('|')[1]

    await call.message.edit_reply_markup(reply_markup=countryes(int(i)))

@dp.callback_query_handler(text_contains ='NEXT_man', state='*')
async def next_country(call: types.CallbackQuery):

    i = call.data.split('|')[1]

    await call.message.edit_reply_markup(reply_markup=countryes_smsman(int(i)))

@dp.message_handler(text='📨 Получить СМС', state='*')
async def wh_serv(message: types.Message):
    await message.answer('Выберите сервис', reply_markup=ikb_serv)

@dp.callback_query_handler(text='smsman')
async def sms_go(message: types.Message):

    with open('Halwa.jpg', 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption='<b>🌎 Выберите страну:</b>', reply_markup=countryes_smsman(0), parse_mode='HTML')



@dp.callback_query_handler(text='sms_activate')
async def sms_go(message: types.Message):

    with open('Halwa.jpg', 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption='<b>🌎 Выберите страну:</b>', reply_markup=countryes(0), parse_mode='HTML')





@dp.callback_query_handler(text_startswith='set_c|')
async def set_coontri(callback: types.CallbackQuery, state:FSMContext):
    strana = callback.data.split("|")[2]
    await callback.message.edit_caption(f'🌎 <b>Страна:</b>{strana}\n'
                                     f'📱 <b>Выберите сервис:</b>', reply_markup=service(0, strana=strana), parse_mode='HTML')


@dp.callback_query_handler(text_startswith='SMS_man|')
async def set_coontri_smsman(callback: types.CallbackQuery, state:FSMContext):

    country_id = callback.data.split("|")[1]
    strana = callback.data.split("|")[2]


    await callback.message.edit_caption(f'🌎 <b>Страна:</b>{strana}\n'
                                     f'📱 <b>Выберите сервис:</b>', reply_markup=service_smsman(0, strana=strana), parse_mode='HTML')

@dp.callback_query_handler(text_contains ='next_s', state='*')
async def next_country(call: types.CallbackQuery):

    text = call['message']['caption']
    text = ''.join(text)
    text = text.split('\n')[0]
    i = call.data.split('|')[1]
    text = text.split(':')[1]

    await call.message.edit_caption(caption=f'🌎 <b>Страна:</b>{text}\n📱 Выберите сервис', reply_markup=service(int(i), strana=text), parse_mode='HTML')


@dp.callback_query_handler(text_contains ='next_Sm', state='*')
async def next_country(call: types.CallbackQuery):
    print(call.data)
    text = call['message']['caption']
    text = ''.join(text)
    text = text.split('\n')[0]
    i = call.data.split('|')[1]
    text = text.split(':')[1]

    await call.message.edit_caption(caption=f'🌎 <b>Страна:</b>{text}\n📱 Выберите сервис', reply_markup=service_smsman(int(i), strana=text), parse_mode='HTML')

#sms_man
@dp.callback_query_handler(text_startswith='set_Sm')
async def set_coontri(callback: types.CallbackQuery, state:FSMContext):

    strana = callback.data.split('|')[-1]
    service = callback.data.split('|')[2]
    country_id = 0
    application_id = callback.data.split('|')[1]
    for v, k in COUNRTY_SMSMAN.items():
        if k == strana:
            country_id = v

    res = requests.get(f'https://api.sms-man.ru/control/get-prices?token=${api_smsMan}&country=${int(country_id)}').json()
    try:
        info = res[str(country_id)][application_id]
    except KeyError:
        await callback.answer('Свободных номер нет, повторите ваш запрос позже', show_alert=True)


    price = info['cost']
    count = info['count']
    if count == 0:
        await callback.answer('Номера закончились', show_alert=True)


    price = float(price) + float(PRICE_SmsMan)

    await callback.message.edit_caption(f'🌎 <b>Страна:</b> {strana}\n'
                                        f'📱 <b>Сервис:</b> {service}\n\n'
                                        f'<b>💰 Стоимость активации:</b> {float(price)} Руб.\n'
                                        f'<b>👌 Доступное количество:</b> {count} шт\n'
                                        f'<b>⌛ Время активации:</b> 20 минут.\n\n'
                                        f'<b>Для того чтобы получить номер телефона, нажмите 📲 Получить код</b>',
                                        parse_mode='HTML',
                                        reply_markup=await service_number_smsman(country_id, application_id, price))

@dp.callback_query_handler(text_startswith='PhoneSMS|')
async def set_coontri(callback: types.CallbackQuery, state:FSMContext):

    country_id = callback.data.split('|')[1]
    application_id = callback.data.split('|')[2]
    price = callback.data.split('|')[3]
    number = requests.get(
        f'https://api.sms-man.ru/control/get-number?token=${api_smsMan}&country_id={int(country_id)}&application_id={int(application_id)}').json()
    try:
        if number['error_msg'] == 'No numbers, try again...':
            return  await callback.answer('Свободных номер нет, повторите ваш запрос позже', show_alert=True)
    except KeyError:
        pass
    id = int(number['request_id'])

    sms = requests.get(f'https://api.sms-man.ru/control/get-sms?token={api_smsMan}&request_id={int(id)}').json()
    print(sms)
    number = sms['number']

    await callback.message.edit_caption(f'Ваш смс код: <code>Ожидаем</code>\n'
                                        f'Номер телефона: <code>{number}</code>\n\n'
                                        f'⚠️ Отменить активацию можно <u>ДО получения кода</u>', parse_mode='HTML', reply_markup=sms_replay_smsman(id, price))

@dp.callback_query_handler(text_startswith='man_sms|')
async def set_coontri(callback: types.CallbackQuery, state:FSMContext):
    await callback.message.delete()
    id = callback.data.split('|')[1]
    price = callback.data.split('|')[2]
    sms = requests.get(f'https://api.sms-man.ru/control/get-sms?token=${api_smsMan}&request_id={int(id)}').json()
    print(sms)
    number = sms['number']
    try:
        if sms['sms_code'] != None:
            with open('Halwa.jpg', 'rb') as photo:
                await bot.send_photo(chat_id=callback.from_user.id, photo=photo,
                                     caption=f'Ваш смс код: <code>{sms["sms_code"]}</code>\n'
                                             f'Номер телефона: <code>{number}</code>\n\n'
                                             f'⚠️ Отменить активацию можно <u>ДО получения кода</u>', parse_mode='HTML',
                                     reply_markup=sms_replay_smsman(id, price))

    except KeyError:
        with open('Halwa.jpg', 'rb') as photo:
            await bot.send_photo(chat_id=callback.from_user.id, photo=photo,
                                 caption=f'Ваш смс код: <code>Ожидаем</code>\n'
                                         f'Номер телефона: <code>{number}</code>\n\n'
                                         f'⚠️ Отменить активацию можно <u>ДО получения кода</u>', parse_mode='HTML',
                                 reply_markup=sms_replay_smsman(id, price))



#Уже использован
@dp.callback_query_handler(text_startswith='man_not')
async def set_coontri(callback: types.CallbackQuery, state:FSMContext):
    id = callback.data.split('|')[1]
    price = callback.data.split('|')[2]
    sms = requests.get(f'https://api.sms-man.ru/control/get-sms?token=${api_smsMan}&request_id={int(id)}').json()

    try:
        if sms['sms_code'] != None:
            minus_balance(callback.from_user.id, float(price))
            await callback.message.delete()
            await callback.message.answer('Спасибо за покупку!')

    except KeyError:
        res = requests.get(
            f'https://api.sms-man.ru/control/set-status?token=${api_smsMan}&request_id={int(id)}&status=reject').json()
        await callback.message.edit_caption(caption='<b>🌎 Выберите страну:</b>',
                                            reply_markup=countryes_smsman(0), parse_mode='HTML')


#Подтвердить
@dp.callback_query_handler(text_startswith='man_nkay')
async def set_coontri(callback: types.CallbackQuery, state:FSMContext):
    id = callback.data.split('|')[1]
    price = callback.data.split('|')[2]
    res = requests.get(f'https://api.sms-man.ru/control/set-status?token=${api_smsMan}&request_id={int(id)}&status=ready')
    minus_balance(callback.from_user.id, float(price))


#sms_activate
@dp.callback_query_handler(text_startswith='set_s_|')
async def set_coontri(callback: types.CallbackQuery, state:FSMContext):
    try:
        strana = callback.data.split('|')[3]

        kod_service = callback.data.split('|')[1]
        servise_kod = []
        for u, p in name_service.items():
            if p == int(kod_service):
                servise_kod.append(u)
        name = []
        for n, z in full_name.items():
            if n == int(kod_service):
                name.append(z)
        name = ''.join(name)

        kod_strana = []
        for m, s in COUNRTY.items():
            if s == strana:
                kod_strana.append(m)



        info = sms.getPrices(servise_kod[0], kod_strana[0])
        for q, r in info.items():
            cost = f'{q}:{r[servise_kod[0]]["cost"]}'
            counter = f'{q}:{r[servise_kod[0]]["count"]}'
            print(info)
            price  = cost.split(':')[1]
            count = counter.split(":")[1]


            phone_number = sms.getNumberV2(servise_kod[0])

            pricec = phone_number['activationCost']
            number_phone = phone_number['phoneNumber']
            result = float(pricec) + float(PRICE)


            if count == '0':
                await callback.answer('Номера закончились', show_alert=True)
            else:

                await callback.message.edit_caption(f'🌎 <b>Страна:</b> {strana}\n'
                                             f'📱 <b>Сервис:</b> {name}\n\n'
                                                 f'☎ <b>Номер телефона:</b> <code>{number_phone}</code>\n'
                                                 f'<b>💰 Стоимость активации:</b> {float(result)} Руб.\n'
                                                 f'<b>👌 Доступное количество:</b> {count} шт\n'
                                                 f'<b>⌛ Время активации:</b> 20 минут.\n\n'
                                                 f'<b>Скопируйте номер телефона, вставьте его в ваш сервис для регистрации и нажмите  📲 Получить код</b>' , parse_mode='HTML', reply_markup= await service_number(number_phone, phone_number['activationId'], int(result)))
    except Exception as e:
        print(e)
        await callback.answer('Номера закончились', show_alert=True)


@dp.callback_query_handler(text_startswith='phone')
async def phone_go(callback:types.CallbackQuery):

    price = callback.data.split('|')[3]
    id = callback.data.split('|')[2]
    number = callback.data.split('|')[1]
    phone_number = sms.getActiveActivations()
    print(phone_number['activeActivations'])
    for i in range(len(phone_number)):
        if phone_number['activeActivations'][i]['phoneNumber'] == number:
            sms_code = phone_number['activeActivations'][i]['smsCode']
            await callback.message.edit_caption(f'Ваш смс код: <code>{sms_code}</code>\n'
                                             f'Номер телефона: <code>{number}</code>', parse_mode='HTML', reply_markup=sms_replay(number, id, price))
        else:
            return await callback.answer('Доступных номер нет в наличии', show_alert=True)


@dp.callback_query_handler(text_startswith='go_sms')
async def phone_go(callback:types.CallbackQuery):
    try:

        await callback.message.delete()
        price = callback.data.split('|')[3]
        id = callback.data.split('|')[2]
        number = callback.data.split('|')[1]
        phone_number = sms.getActiveActivations()
        for i in range(len(phone_number)):
            if phone_number['activeActivations'][i]['phoneNumber'] == number:
                sms_code = phone_number['activeActivations'][i]['smsCode']
                if sms_code == None:
                    await callback.message.answer(f'Ваш смс код: <code>{sms_code}</code>\n\n'
                                                  f'Номер телефона: <code>{number}</code>', parse_mode='HTML', reply_markup=sms_replay(number, id, price))
                else:
                    await callback.message.answer(f'Ваш смс код: <code>{sms_code[0]}</code>', parse_mode='HTML', reply_markup=sms_replay(number, id, price))
    except Exception:
        await callback.message.delete()
        price = callback.data.split('|')[3]
        number = callback.data.split('|')[1]
        id = callback.data.split('|')[2]
        phone_number = sms.getActiveActivations()
        for i in range(len(phone_number)):
            if phone_number['activeActivations'][0]['phoneNumber'] == number:
                sms_code = phone_number['activeActivations'][0]['smsCode']
                if sms_code == None:
                    await callback.message.answer(f'Ваш смс код: <code>{sms_code}</code>\n\n'
                                                  f'Номер телефона: <code>{number}</code>', parse_mode='HTML',
                                                  reply_markup=sms_replay(number, id))
                else:
                    await callback.message.answer(f'Ваш смс код: <code>{sms_code[0]}</code>', parse_mode='HTML', reply_markup=sms_replay(number, id, price))

@dp.callback_query_handler(text_startswith='okay')
async def phone_go(callback:types.CallbackQuery):
    price = callback.data.split('|')[3]
    number = callback.data.split('|')[1]
    id = callback.data.split('|')[2]
    status = sms.setStatus(id=id, forward=number, status=8)
    if status == 'EARLY_CANCEL_DENIED':
        await callback.answer('Нельзя отменить номер в первые 2 минуты', show_alert=True)
    else:
        res = await callback.message.edit_text('Активации успешно отменена')
        await asyncio.sleep(30)
        await res.delete()

@dp.callback_query_handler(text_startswith='nkay')
async def phone_go(callback:types.CallbackQuery):
    price = callback.data.split('|')[3]
    number = callback.data.split('|')[1]
    id = callback.data.split('|')[2]
    status = sms.setStatus(id=id, forward=number, status=6)
    if status == 'ACCESS_ACTIVATION':
        await callback.message.edit_text('Сервис успешно активирован')
        minus_balance(callback.from_user.id, int(price))

@dp.callback_query_handler(text_startswith='not')
async def phone_go(callback:types.CallbackQuery):
    price = callback.data.split('|')[3]
    number = callback.data.split('|')[1]
    id = callback.data.split('|')[2]
    status = sms.setStatus(id=id, forward=number, status=8)
    if status == 'ACCESS_CANCEL':
        await callback.message.edit_text('Активации успешно отменена')


@dp.message_handler(commands=['admin'])
async def cmd_adm(message: types.Message):
    if message.from_user.id == ADMIN:
        await message.answer('Вы в админ панели', reply_markup=kb_admin)


@dp.message_handler(text='Общие пополнения')
async def tip_text(message: types.Message):
    if message.from_user.id == ADMIN:
        balance = all_balance_chek()
        await message.answer(f'Всего пополнений в боте на {balance} Рублей')

@dp.message_handler(text='ВКЛ (Заработать/Забрать)')
async def tip_text(message: types.Message):
    if message.from_user.id == ADMIN:
        on_buttons()
        await message.answer('Кнопки включены')

@dp.message_handler(text='ВЫКЛ (Заработать/Забрать)')
async def tip_text(message: types.Message):
    if message.from_user.id == ADMIN:
        off_buttons()
        await message.answer('Кнопки выключены')

@dp.message_handler(text='Статистика ссылок')
async def tip_text(message: types.Message):
    if message.from_user.id == ADMIN:
        info = url_chek()

        for i in range(len(info)):
            url = info[i][0]
            count = info[i][1]
            await message.answer(f'<code>{url}</code> - {count} переходов')

@dp.message_handler(text='Удалить все ссылки')
async def tip_text(message: types.Message):
    if message.from_user.id == ADMIN:
        url_delete()
        await message.answer('Все ссылки успешно удалены')

class URL_CREATE(StatesGroup):
    url = State()

@dp.message_handler(text='Создание ссылки')
async def tip_text(message: types.Message):
    if message.from_user.id == ADMIN:
        db_url_ref()
        await message.answer(f'Введите слово после start: \n'
                             f'http://t.me/{NICNAME_BOT}?start=', reply_markup=ikb_stop)
        await URL_CREATE.url.set()

@dp.message_handler(state=URL_CREATE.url)
async def create_url(message: types.Message, state:FSMContext):
    text = message.text
    await message.answer(f'Ваша ссылка готова: <code>http://t.me/{NICNAME_BOT}?start={text}</code>')
    add_url(f'http://t.me/{NICNAME_BOT}?start={text}', text)
    await state.finish()



@dp.message_handler(text='Включить ОП')
async def tip_text(message: types.Message):
    if message.from_user.id == ADMIN:
        on_subs()
        await message.answer('Обязательная подписка включена')

@dp.message_handler(text='💵 Заработать')
async def tip_text(message: types.Message):
    res = select_buton2()
    if res[-1] == 'no':
        if res[0] == 'text':
            await message.answer(f'{res[1]}')
        if res[0] == 'photo':
            await bot.send_photo(chat_id=message.from_user.id, photo=res[-1], caption=res[1])
        if res[0] == 'video':
            await bot.send_video(chat_id=message.from_user.id, video=res[-1], caption=res[1])
        if res[0] == 'animation':
            await bot.send_animation(chat_id=message.from_user.id, animation=res[-1], caption=res[1])
    else:
        buton = res[-1]
        url = buton.split('|')[1].strip()
        name = buton.split('|')[0]
        if res[0] == 'text':
            await message.answer(f'{res[1]}', reply_markup=kb_rassilka(buton=name, url=url))
        if res[0] == 'photo':
            await bot.send_photo(chat_id=message.from_user.id, photo=res[-2], caption=res[1], reply_markup=kb_rassilka(buton=name, url=url))
        if res[0] == 'video':
            await bot.send_video(chat_id=message.from_user.id, video=res[-2], caption=res[1], reply_markup=kb_rassilka(buton=name, url=url))
        if res[0] == 'animation':
            await bot.send_animation(chat_id=message.from_user.id, animation=res[-2], caption=res[1], reply_markup=kb_rassilka(buton=name, url=url))


@dp.message_handler(text='1$ за подписку')
async def tip_text(message: types.Message):
    res = select_buton()

    if res[-1] == 'no':
        if res[0] == 'text':
            await message.answer(f'{res[1]}')
        if res[0] == 'photo':
            await bot.send_photo(chat_id=message.from_user.id, photo=res[-1], caption=res[1])
        if res[0] == 'video':
            await bot.send_video(chat_id=message.from_user.id, video=res[-1], caption=res[1])
        if res[0] == 'animation':
            await bot.send_animation(chat_id=message.from_user.id, animation=res[-1], caption=res[1])
    else:
        buton = res[-1]
        url = buton.split('|')[1].strip()
        name = buton.split('|')[0]

        if res[0] == 'text':
            await message.answer(f'{res[1]}', reply_markup=kb_rassilka(buton=name, url=url))
        if res[0] == 'photo':
            await bot.send_photo(chat_id=message.from_user.id, photo=res[-2], caption=res[1], reply_markup=kb_rassilka(buton=name, url=url))
        if res[0] == 'video':
            await bot.send_video(chat_id=message.from_user.id, video=res[-2], caption=res[1], reply_markup=kb_rassilka(buton=name, url=url))
        if res[0] == 'animation':
            await bot.send_animation(chat_id=message.from_user.id, animation=res[-2], caption=res[1], reply_markup=kb_rassilka(buton=name, url=url))

@dp.message_handler(text='Выключить ОП')
async def tip_text(message: types.Message):
    if message.from_user.id == ADMIN:
        off_subs()
        await message.answer('Обязательная подписка выключена')

@dp.message_handler(text='Количество пользователей')
async def tip_text(message: types.Message):
    if message.from_user.id == ADMIN:
        res = all_users()
        await message.answer(f'Пользователей в системе: {len(res)}')

@dp.message_handler(text='Выход')
async def tip_text(message: types.Message):
    if message.from_user.id == ADMIN:

        if chek_buttons() == 0:
            markup = kb
            await message.answer('Выход из админ панели', reply_markup=markup)
        else:
            markup = kbb
            await message.answer('Выход из админ панели', reply_markup=markup)

class AdminKomsa(StatesGroup):
    komsa = State()

@dp.message_handler(text='Настройка комиссии')
async def tip_text(message: types.Message):
    if message.from_user.id == ADMIN:
        info_komsa = komsa_chek()[0]
        await message.answer(f'Текущая комиссия: {info_komsa}$\n\nВведите новую комиссию (Целое число)', reply_markup=ikb_stop)
        await AdminKomsa.komsa.set()

@dp.message_handler(state=AdminKomsa.komsa)
async def komsas(message: types.Message, state:FSMContext):
    komsa = int(message.text)
    komsa_update(komsa)
    await message.answer('Комиссия успешно изменена')
    await state.finish()


class AdminPhotoText(StatesGroup):
    text = State()
    photo = State()

@dp.message_handler(text='Рассылка')
async def ras(message: types.Message):
    if message.from_user.id == ADMIN:
        await message.answer('Выберите тип рассылки', reply_markup=ikb_tip_rassilka)

@dp.callback_query_handler(text='photo')
async def tip_text(callback: types.CallbackQuery):
    await callback.message.edit_text('Отправьте текст рассылки', reply_markup=ikb_stop)
    await AdminPhotoText.text.set()

@dp.message_handler(state=AdminPhotoText.text)
async def rasl_text(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await message.answer('Отправьте фото', reply_markup=ikb_stop)
    await AdminPhotoText.next()

@dp.message_handler(content_types=['photo'], state=AdminPhotoText.photo)
async def rasl_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    user = all_users()

    count = 0
    try:
        for i in range(len(user)):

            try:

                await bot.send_photo(chat_id=user[i][0], photo=data['photo'], caption=data['text'], parse_mode='HTML')
                count += 1
            except Exception as e:
                print(e)
                continue
        await bot.send_message(ADMIN, '✅Рассылка успешно отправлена\n'
                                  f'Сообщение получили: {count} человек')
        await state.finish()
    except Exception as e:
        await state.finish()
        print(e)

class AdminText(StatesGroup):
    text = State()

@dp.callback_query_handler(text='Texts')
async def tip_text(callback: types.CallbackQuery):
    await callback.message.edit_text('Отправьте текст рассылки', reply_markup=ikb_stop)
    await AdminText.text.set()

@dp.message_handler(state=AdminText.text)
async def rasl_text(message: types.Message, state:FSMContext):

    text = message.text
    user = all_users()
    count = 0
    try:
        for i in range(len(user)):
            try:
                await bot.send_message(user[i][0], f'{text}', parse_mode='HTML')
                count += 1
            except Exception:
                continue

        await bot.send_message(ADMIN, '✅Рассылка успешно отправлена\n'
                                  f'Сообщение получили: {count} человек')
        await state.finish()
    except Exception as e:
        await state.finish()
        print(e)

@dp.callback_query_handler(text='back_tip')
async def tip_text(callback: types.CallbackQuery):
    await callback.message.edit_text('Выберите кнопку', reply_markup=ikb_buttons)


@dp.message_handler(text='Редактирование (Заработать/Забрать)')
async def tip_text(message: types.Message):
    if message.from_user.id == ADMIN:
        db_new_buton()
        db_new_buton2()
        await message.answer('Выберите кнопку', reply_markup=ikb_buttons)

@dp.callback_query_handler(text_startswith='BUT')
async def but(callback: types.CallbackQuery):
    butons = callback.data.split('|')[1]
    await callback.message.edit_text(f'Кнопка <b>{butons}</b>\n\nВыберите тип загружаемого контента', reply_markup=ikb_tips_buton(butons))

class TEXT(StatesGroup):
    text = State()


@dp.callback_query_handler(text_startswith='Text')
async def but(callback: types.CallbackQuery, state:FSMContext):
    butons = callback.data.split('|')[1]
    await callback.message.edit_text('Напишите текст', reply_markup=ikb_stop)
    await TEXT.text.set()
    await state.update_data(butons=butons)


@dp.message_handler(state=TEXT.text)
async def txt(message:types.Message, state:FSMContext):
    text = message.text
    data = await state.get_data()
    if data['butons'] == '1$ за подписку':
        add_text('1$ за подписку', 'text', text, 0)
        await message.answer('Данные загружены')
        await state.finish()
        await message.answer('Желаете добавить кнопку?', reply_markup=add_but('1$ за подписку'))
    else:
        add_text2('💵 Заработать', 'text', text, 0)
        await message.answer('Данные загружены')
        await state.finish()
        await message.answer('Желаете добавить кнопку?', reply_markup=add_but('💵 Заработать'))

class PHOTO(StatesGroup):
    photo = State()

@dp.callback_query_handler(text_startswith='Photo')
async def but(callback: types.CallbackQuery, state:FSMContext):
    butons = callback.data.split('|')[1]
    await callback.message.edit_text('Отправьте фото и описание', reply_markup=ikb_stop)
    await PHOTO.photo.set()
    await state.update_data(butons=butons)


@dp.message_handler(content_types=['photo'], state=PHOTO.photo)
async def txt(message:types.Message, state:FSMContext):
    photo = message.photo[0].file_id
    text = message.caption
    data = await state.get_data()
    if data['butons'] == '1$ за подписку':
        add_text('1$ за подписку', 'photo', text, photo)
        await message.answer('Данные загружены')
        await message.answer('Желаете добавить кнопку?', reply_markup=add_but('1$ за подписку'))
        await state.finish()

    else:
        add_text2('💵 Заработать', 'photo', text, photo)
        await message.answer('Данные загружены')
        await state.finish()
        await message.answer('Желаете добавить кнопку?', reply_markup=add_but('💵 Заработать'))


class ANIMATION(StatesGroup):
    text = State()
    animation = State()

@dp.callback_query_handler(text_startswith='Gif')
async def but(callback: types.CallbackQuery, state:FSMContext):
    butons = callback.data.split('|')[1]
    await callback.message.edit_text('Отправьте текст', reply_markup=ikb_stop)
    await ANIMATION.text.set()
    await state.update_data(butons=butons)

@dp.message_handler(state=ANIMATION.text)
async def txt(message:types.Message, state:FSMContext):
    await state.update_data(text=message.text)
    await message.answer('Отправьте GIF')
    await ANIMATION.next()

@dp.message_handler(content_types=['animation'], state=ANIMATION.animation)
async def txt(message:types.Message, state:FSMContext):

    gif = message.animation['file_id']

    data = await state.get_data()
    if data['butons'] == '1$ за подписку':
        add_text('1$ за подписку', 'animation', data['text'], gif)
        await message.answer('Данные загружены')
        await state.finish()
        await message.answer('Желаете добавить кнопку?', reply_markup=add_but('1$ за подписку'))
    else:
        add_text2('💵 Заработать', 'animation', data['text'], gif)
        await message.answer('Данные загружены')
        await state.finish()
        await message.answer('Желаете добавить кнопку?', reply_markup=add_but('💵 Заработать'))



class VIDEO(StatesGroup):
    video = State()

@dp.callback_query_handler(text_startswith='Video')
async def but(callback: types.CallbackQuery, state:FSMContext):
    butons = callback.data.split('|')[1]
    await callback.message.edit_text('Отправьте видео и описание', reply_markup=ikb_stop)
    await VIDEO.video.set()
    await state.update_data(butons=butons)


@dp.message_handler(content_types=['video'], state=VIDEO.video)
async def txt(message:types.Message, state:FSMContext):

    video = message.video['file_id']
    text = message.caption
    data = await state.get_data()
    if data['butons'] == '1$ за подписку':
        add_text('1$ за подписку', 'video', text, video)
        await message.answer('Данные загружены')
        await state.finish()
        await message.answer('Желаете добавить кнопку?', reply_markup=add_but('1$ за подписку'))
    else:
        add_text2('1$ за подписку', 'video', text, video)
        await message.answer('Данные загружены')
        await state.finish()
        await message.answer('Желаете добавить кнопку?', reply_markup=add_but('💵 Заработать'))



class BUTTON(StatesGroup):
    keybord = State()

@dp.callback_query_handler(text_startswith='YES')
async def yes(callback:types.CallbackQuery, state:FSMContext):
    but = callback.data.split('|')[1]
    await callback.message.edit_text('Отправьте название кнопки и URL\n\n'
                         'Пример: Реклама|.https://www.youtube')
    await BUTTON.keybord.set()
    data = await state.update_data(butons=but)

@dp.message_handler( state=BUTTON.keybord)
async def txt(message:types.Message, state:FSMContext):
    data = await state.get_data()

    if data['butons'] == '1$ за подписку':
        add_keybord(message.text)
        await message.answer('Кнопка добавлена')
        await state.finish()
    else:
        add_keybord2(message.text)
        await message.answer('Кнопка добавлена')
        await state.finish()

@dp.callback_query_handler(text_startswith='NO')
async def yes(callback:types.CallbackQuery, state:FSMContext):
    but = callback.data.split('|')[1]
    if but == '1$ за подписку':
        add_keybord('no')
    else:
        add_keybord2('no')
    await callback.message.delete()

async def on_startup(_):
    await set_default_commands(dp)
    print('Bot started')


if __name__ == '__main__':
    dp.middleware.setup(CheksSub())
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)



