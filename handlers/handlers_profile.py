from aiogram import Router, types, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging

import utility as util
import keyboards as kb
from texts.base_texts import base_texts
from texts.programme_texts import prog_data
from handlers.handlers_prog import programmes_handler
from handlers.handlers_data import send_by_webhook


class RegistrationState(StatesGroup):
  user_registered = State()
  waiting_for_name = State()
  waiting_for_phone = State()
  waiting_for_phone_confirmation = State()
  waiting_for_email = State()
  waiting_for_email_confirmation = State()
  
class EditingState(StatesGroup):
  edit_name = State()
  edit_phone = State()
  edit_email = State()

  
profile_router = Router()

# --------------------------------------REGISTRATION--------------------------------------
"""
  register from prog page callback handler
"""
@profile_router.callback_query(kb.progCallbackFactory.filter(F.action == 'registration'))
async def send_registration_check(callback: types.CallbackQuery, state: FSMContext):
  user_id = callback.from_user.id
  current_state = await state.get_state()
  user_data = await state.get_data()

  if current_state == "RegistrationState:user_registered" and user_data['id'] == user_id:
    await callback.message.answer(f"<b>Ты уверен, что хочешь отправить свои данные для связи организаторам программы {prog_data[user_data['current_prog']][0]}?</b>",
                                  reply_markup=kb.get_confirmation_keyboard())
  else:
    await callback.message.answer(base_texts["baseRegister"](), reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationState.waiting_for_name)

  await callback.answer()



"""
  ask the email
"""
@profile_router.message(RegistrationState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
  name = message.text

  if util.is_valid_name(name):
    await state.update_data(id=message.from_user.id, name=name)
    await message.answer("<b>Теперь введи свою электронную почту:</b>")
    await state.set_state(RegistrationState.waiting_for_email)
  else:
    await message.answer("<b>Неправильный формат имени. Имя должно начинаться с заглавной буквы, содержать не менее двух слов и \
состоять только из букв латиницы и кириллицы.\n\nПопробуй ещё раз!</b>")


"""
  sure?, test and save the email
"""
@profile_router.message(RegistrationState.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
  email = message.text

  if util.is_valid_email(email):
    await state.update_data(email=email)
    await message.answer(f"Ты уверен(-a), что <b>{email}</b> — твоя электронная почта?",
                          reply_markup=kb.get_yes_or_no())
    await state.set_state(RegistrationState.waiting_for_email_confirmation)
  else:
    await message.answer("<b>Неправильный формат электронной почты. Попробуй ещё раз.</b>")


"""
  confirm email, ask phone
"""
@profile_router.callback_query(RegistrationState.waiting_for_email_confirmation)
async def process_email_confirmation(callback: types.CallbackQuery, state: FSMContext):
  await callback.message.delete()

  if callback.data == 'confirmYes':
    await callback.message.answer("<b>Отлично! Почти закончили.\nТеперь введи, пожалуйста, действующий номер телефона через «+»:</b>")
    await state.set_state(RegistrationState.waiting_for_phone)
  elif callback.data == 'confirmNo':
    await callback.message.answer("<b>Введи адрес электронной почты ещё раз:</b>")
    await state.set_state(RegistrationState.waiting_for_email)
  else:
    await callback.message.answer("<b>Что-то пошло не так. Попробуй ещё раз.</b>")

  await callback.answer()



"""
  confirms phone
"""
@profile_router.message(RegistrationState.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
  phone = message.text

  if util.is_valid_phone(phone):
    await state.update_data(phone=phone)
    await message.answer(f"Ты уверен(-a), что <b>{phone}</b> — твой номер телефона?", reply_markup=kb.get_yes_or_no())
    await state.set_state(RegistrationState.waiting_for_phone_confirmation)
  else:
    await message.answer("<b>Неправильный формат номера телефона. Попробуй ещё раз.</b>")



"""
  final stage of the registration process
"""
@profile_router.callback_query(RegistrationState.waiting_for_phone_confirmation)
async def process_phone_confirmation(callback: types.CallbackQuery, state: FSMContext):
  await callback.message.delete()

  if callback.data == 'confirmYes':
    user_id = callback.from_user.id
    user_data = await state.get_data()
    await send_by_webhook(callback, state)
    await state.set_state(RegistrationState.user_registered)
    current_prog = user_data.get('current_prog', 0)

    # send data to program manager
    if current_prog != 0:
      await callback.message.answer(f"<b>Успешная регистрация! Теперь ты можешь достучаться до организаторов программ в один клик!</b>\n\n\
Ты уверен, что хочешь отправить свои данные для связи организаторам программы {prog_data[current_prog][0]}?",
                                    reply_markup=kb.get_confirmation_keyboard())
    else:
      await callback.message.answer("<b>Успешная регистрация! Теперь ты можешь достучаться до организаторов программ в один клик!</b>",
                                    reply_markup=kb.replyMenu)
      await programmes_handler(callback, state)

    logging.info(f"registered user's ID: {user_id}, phone: {user_data['phone']}, email: {user_data['email']}")
  elif callback.data == 'confirmNo':
    await callback.message.answer("<b>Введи номер телефона ещё раз:</b>")
    await state.set_state(RegistrationState.waiting_for_phone)
  else:
    await callback.message.answer("Что-то пошло не так. Попробуй ещё раз.")

  await callback.answer()



# ------------------------------------PROFILE------------------------------------
"""
  profile text handler — shows inline markup message
"""
@profile_router.message(F.text.lower().in_(["профиль", "profile"]))
async def profile_handler(message: Message, state: FSMContext):
  let_pass = await util.state_checker(state)
  
  if not let_pass:
    return
  
  user_id = message.from_user.id
  user_data = await state.get_data()
  logged_in = await state.get_state() == "RegistrationState:user_registered" and user_data['id'] == user_id
  new_texts = {
    True: lambda: base_texts["profileMessage"]().format(name, phone, email),
    False: lambda: base_texts["profileMessageLoggedOut"]() 
  }

  if logged_in:
    name = user_data.get("name")
    phone = user_data.get("phone")
    email = user_data.get("email")
    logged_in = True

  await message.answer(new_texts[logged_in](),
                       reply_markup=kb.get_profile_keyboard(logged_in))



"""
  util for updating the message with profile keyboard
"""
async def profile_message_update(callback: types.CallbackQuery,
                                 callback_data: kb.regCallbackFactory,
                                 state: FSMContext, 
                                 new_text: str):
  user_id = callback.from_user.id
  user_data = await state.get_data()
  logged_in = await state.get_state() == "RegistrationState:user_registered" and user_data['id'] == user_id

  try:
    await callback.message.edit_text(new_text,
                                     reply_markup=kb.get_profile_keyboard(registration=logged_in,
                                                                          category=callback_data.text))
  except TelegramBadRequest as e:
    logging.error(f"Failed to edit profiles message: {e}")



"""
  compose a log entry into readable text for the user
"""
async def history_text_constructor(callback: types.CallbackQuery, state: FSMContext):
  user_data = await state.get_data()
  text = base_texts["regHistory"]()
  
  try:
    log = user_data['log']
    entries = [f"\n\n • Дата и время: <b>{entry[:19]}</b>;\nПрограмма: <b>{prog_data[entry[22:]][0]}</b>" for entry in log]
    text += ''.join(entries)
  except KeyError as e:  # USER HAS NO LOGS YET
    logging.warning(f"Failed to construct history text — no log entries yet: {e}")
    await callback.message.delete()
    await callback.message.answer(base_texts["regHistoryNoLogs"](),
                                  reply_markup=kb.InlineKeyboardBuilder().button(text="Программы", callback_data='programmes').as_markup())
  return text



"""
  handles callbacks from profile page
"""
@profile_router.callback_query(kb.regCallbackFactory.filter())
async def profile_callback_handler(callback: types.CallbackQuery, 
                                   callback_data: kb.regCallbackFactory,
                                   state: FSMContext):
  # registration
  if callback_data.action == "rega":
    await send_registration_check(callback, state)

  # edit data
  elif callback_data.action == 'edit':
    if callback_data.text == 'regEditName':
      item = 'имя'
    elif callback_data.text == 'regEditPhone':
      item = 'телефон'
    elif callback_data.text == 'regEditEmail':
      item = 'почту'
    await callback.message.answer(f"<b>Вы хотите изменить {item}</b>\n\nПожалуйста, внесите новые данные:")
    await state.set_state(f"EditingState:edit_{callback_data.text[7:].lower()}")

  # goes to the profile page and show all user data
  elif callback_data.action == "menu":
    user_data = await state.get_data()
    new_text = base_texts["profileMessage"]().format(user_data["name"], user_data["phone"], user_data["email"])
    await profile_message_update(callback, callback_data, state, new_text)

  # goes to the history of applications page
  elif callback_data.text == "regHistory":
    new_text = await history_text_constructor(callback, state)
    await profile_message_update(callback, callback_data, state, new_text)

  else:
    new_text = base_texts[callback_data.text]()
    await profile_message_update(callback, callback_data, state, new_text)
  await callback.answer()


"""
  edit user's personal data handlers
"""
@profile_router.message(EditingState.edit_name)
async def edit_data_name(message: Message,
                         state: FSMContext):
  new_name = message.text

  if util.is_valid_name(new_name):
    await state.update_data(name=new_name)
    await message.answer("Имя успешно обновлено! Возвращаю тебя на страничку с профилем.")
    await state.set_state(RegistrationState.user_registered)
    await profile_handler(message, state)
  else:
    await message.answer("<b>Неправильный формат имени. Имя должно начинаться с заглавной буквы, содержать не менее двух слов и \
состоять только из букв латиницы и кириллицы.\n\nПопробуй ещё раз!</b>")


@profile_router.message(EditingState.edit_phone)
async def edit_data_phone(message: Message,
                          state: FSMContext):
  new_phone = message.text

  if util.is_valid_phone(new_phone):
    await state.update_data(phone=new_phone)
    await message.answer("Телефон успешно обновлён! Возвращаю тебя на страничку с профилем.")
    await state.set_state(RegistrationState.user_registered)
    await profile_handler(message, state)
  else:
    await message.answer("<b>Неправильный формат номера телефона. Попробуй ещё раз.</b>")
 
 
@profile_router.message(EditingState.edit_email)
async def edit_data_email(message: Message,
                          state: FSMContext):
  new_email = message.text

  if util.is_valid_email(new_email):
    await state.update_data(email=new_email)
    await message.answer("Почта успешно обновлена! Возвращаю тебя на страничку с профилем.")
    await state.set_state(RegistrationState.user_registered)
    await profile_handler(message, state)
  else:
    await message.answer("<b>Неправильный формат электронной почты. Попробуй ещё раз.</b>")
    

