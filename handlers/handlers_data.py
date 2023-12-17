import sys
import requests
import logging
import os
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

import keyboards as kb
from texts.programme_texts import prog_data
from utility import append_to_log
from handlers.handlers_menu import main_menu_handler

data_router = Router()

# --------------------------------------SENDER--------------------------------------

async def send_by_webhook(callback: types.CallbackQuery, state: FSMContext, apply=False):
  try:
    webhook_url = os.environ["WEBHOOK_URL"]
  except KeyError:
    logging.error("environment variable WEBHOOK_URL not set")
    sys.exit(1)
  user_data = await state.get_data()
  data_to_send = {
      'id': user_data['id'],
      'name': user_data['name'],
      'phone': user_data['phone'],
      'email': user_data['email']
  }
  if apply:
    data_to_send['apply'] = prog_data[user_data['current_prog']]
  try:
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, headers=headers, json=data_to_send, timeout=10)

    if response.status_code != 200:
      logging.error(f"Failed to send data to webhook: {response.content}")
      await callback.message.answer("Упс! Что-то пошло не так, попробуй заново.")
      return

    logging.info(f"sent {callback.from_user.id}'s data")
    await callback.message.edit_text("<b>Сообщение отправлено!!</b>")
    await callback.message.answer("С тобой выйдут на связь как можно раньше! :)\nХоть ожидание и не продлится долго, можешь в это время узнать больше о Маса:",
                                  reply_markup=kb.replyMenu)
  except TelegramBadRequest as e:
    logging.error(f"failed to edit a message: {e}")
  except Exception as e:
    logging.error(f"Failed to send data: {e}")
    await callback.message.answer("Упс! Что-то пошло не так, попробуй заново.")
  await main_menu_handler(callback.message, state)


"""
  sends the message, stores log for user and calls main menu
"""
@data_router.callback_query(kb.senderCallbackFactory.filter())
async def data_sender(callback: types.CallbackQuery, callback_data: kb.senderCallbackFactory, state: FSMContext):
  if callback_data.data == "sendData":
    try:
      await send_by_webhook(callback, state, apply=True)
      await append_to_log(callback, state)
    except Exception as e:
      logging.error(e)
      await callback.message.answer("Упс! Что-то пошло не так, попробуй заново.")
  else:
    await callback.message.delete()
    await callback.message.answer("Окей, посмотри другие программы и точно найдёшь себе что-нибудь по душе! ;)", reply_markup=kb.replyMenu)
    await main_menu_handler(callback.message, state)
  await callback.answer()
