from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import logging

import utility as util
import keyboards as kb
from texts.base_texts import base_texts
from texts.faq_texts import faq_texts
from texts.grants_texts import grants_texts

menu_router = Router()

# ------------------------------------START------------------------------------
@menu_router.message(Command('start'))
async def start_handler(message: Message, state: FSMContext):
  let_pass = await util.state_checker(state)
  if not let_pass:
    return
  await state.update_data(id=message.from_user.id)
  # need to show reply keyboard first
  await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=kb.replyMenu)
  # now show the main UI using inline keyboards layout
  await message.answer(base_texts["startMessage"](), reply_markup=kb.startMenuInline)



# ------------------------------------MAIN MENU------------------------------------
@menu_router.message(F.text.lower().in_(["menu", "главное меню", "меню"]))
async def main_menu_handler(message: Message, state: FSMContext):
  let_pass = await util.state_checker(state)
  if not let_pass:
    return
  await message.answer(base_texts["menuMessage"](), reply_markup=kb.startMenuInline)



# --------------------------------------ABOUT--------------------------------------
@menu_router.callback_query(F.data == 'about')
async def about_page(callback: types.CallbackQuery):
  await callback.message.answer(base_texts["aboutMessage"](), reply_markup=kb.get_about_keyboard())
  await callback.answer()



@menu_router.callback_query(kb.aboutCallbackFactory.filter())
async def about_callback_handler(callback: types.CallbackQuery,
                                 callback_data: kb.aboutCallbackFactory):
  await callback.message.edit_text(base_texts[callback_data.data](), reply_markup=kb.get_about_keyboard())
  await callback.answer()



# --------------------------------------FAQ--------------------------------------
@menu_router.message(F.text.lower() == "faq")
async def faq_handler(message: Message, state: FSMContext):
  let_pass = await util.state_checker(state)
  if not let_pass:
    return

  user_data = await state.get_data()
  user_data['page_faq'] = 0
  await state.update_data(user_data)
  await message.answer(faq_texts["faqMessage"](), reply_markup=kb.get_faq_keyboard())



"""
  needed to update the text and the keyboard of the message
"""
async def faq_page_update(message: Message, state: FSMContext, new_text: str=faq_texts["faqMessage"]()):
  user_data = await state.get_data()
  try:
    await message.edit_text(new_text, reply_markup=kb.get_faq_keyboard(page=user_data['page_faq']))
  except TelegramBadRequest as e:
    logging.error(f"Failed to edit faq message: {e}")
    


"""
  changes the page variable and saves the current state of the user
"""
@menu_router.callback_query(kb.faqCallbackFactory.filter(F.action.in_(['next', 'back'])))
async def faq_callback_change_page(callback: types.CallbackQuery, callback_data: kb.faqCallbackFactory, state: FSMContext):
  if callback_data.action == 'next':
    await state.update_data(page_faq=1)
    await faq_page_update(callback.message, state)
  else:
    await state.update_data(page_faq=0)
    await faq_page_update(callback.message, state)

  await callback.answer()


@menu_router.callback_query(kb.faqCallbackFactory.filter(F.action == 'stay'))
async def faq_callback_question(callback: types.CallbackQuery, callback_data: kb.faqCallbackFactory, state: FSMContext):
  user_data = await state.get_data()
  await faq_page_update(callback.message, state, faq_texts[callback_data.question]())
  await callback.answer()



# --------------------------------------GRANTS/VISAS--------------------------------------
@menu_router.callback_query(F.data == 'grants_visas')
async def grants_visas_handler(callback: types.CallbackQuery):
  await callback.message.answer(grants_texts["grantsVisasMessage"](), reply_markup=kb.get_grants_visas_keyboard())
  await callback.answer()
  
  

# --------------------------------------GRANTS--------------------------------------
@menu_router.callback_query(F.data == 'grants')
async def grants_handler(callback: types.CallbackQuery):
  await callback.message.answer(grants_texts["grantsMessage"](), reply_markup=kb.get_grants_keyboard())
  await callback.answer()
 


async def grants_page_update(message: Message, new_text: str=grants_texts["grantsMessage"]()):
  try:
    await message.edit_text(new_text, reply_markup=kb.get_grants_keyboard())
  except TelegramBadRequest as e:
    logging.error(f"Failed to edit grants message: {e}")



@menu_router.callback_query(kb.grantCallbackFactory.filter())
async def grants_callback_handler(callback: types.CallbackQuery, callback_data: kb.grantCallbackFactory):
  await grants_page_update(callback.message, grants_texts[callback_data.data]())
  await callback.answer()
  
  

# --------------------------------------VISAS--------------------------------------
@menu_router.callback_query(F.data == 'visas')
async def visas_handler(callback: types.CallbackQuery):
  await callback.message.answer(grants_texts["visasMessage"](), reply_markup=kb.get_visas_keyboard())
  await callback.answer()
  


async def visas_page_update(message: Message, new_text: str=grants_texts["visasMessage"]()):
  try:
    await message.edit_text(new_text, reply_markup=kb.get_visas_keyboard())
  except TelegramBadRequest as e:
    logging.error(f"Failed to edit visas message: {e}")
    


@menu_router.callback_query(kb.visasCallbackFactory.filter())
async def visas_callback_handler(callback: types.CallbackQuery, callback_data: kb.visasCallbackFactory):
  await visas_page_update(callback.message, grants_texts[callback_data.data]())
  await callback.answer()

# no match
@menu_router.message()
async def message_handler(message: Message):
  await message.answer("Упс, я не понимаю эту команду :(\nНапиши /start, чтобы начать работу с ботом")
