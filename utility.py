# ------------------------------------UTILITY------------------------------------
import phonenumbers
import logging
import re
from datetime import datetime
from aiogram import types
from aiogram.fsm.context import FSMContext



async def state_checker(state: FSMContext) -> bool:
  current_state = await state.get_state()
  return current_state is None or current_state == "RegistrationState:user_registered"


def is_valid_email(email) -> bool:
  # comprehensive email regex pattern
  email_regex = r"^(?![^\x00-\x7F])[\w.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
  return bool(re.match(email_regex, email))


def is_valid_phone(phone) -> bool:
  try:
    input_number = phonenumbers.parse(phone)
    return phonenumbers.is_valid_number(input_number)
  except phonenumbers.phonenumberutil.NumberParseException:
    return False


def is_valid_name(name: str) -> bool:
    name_regex = r"^[A-ZА-Я][a-zа-я]+( [A-ZА-Я][a-zа-я]+)*$"
    return bool(re.match(name_regex, name))



"""
  saves "datetime | the program user has applied to"
  into the "log" key of the db
"""
async def append_to_log(callback: types.CallbackQuery,
                        state: FSMContext):
  current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  user_data = await state.get_data()
  current_prog = user_data.get('current_prog', 0)

  try:
    log_entry = f"{current_time} | {current_prog}"
    user_log = user_data.get("log", [])
    user_log.append(log_entry)
    await state.update_data(log=user_log)
  except KeyError as e:
    callback.message.answer("Упс! Что-то пошло не так, начни сначала.")
    logging.error(f"Failed to add log into the database: {e}")
