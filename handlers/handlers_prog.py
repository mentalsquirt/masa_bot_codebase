from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
import logging

import keyboards as kb
from texts.programme_texts import prog_texts


prog_router = Router()


# --------------------------------------PROGRAMMES--------------------------------------
"""
  initializes user's page and replies with needed text
"""
@prog_router.callback_query(F.data == 'programmes')
async def programmes_handler(callback: types.CallbackQuery, state: FSMContext):
  user_id = callback.from_user.id
  user_data = await state.get_data()
  user_data['page_prog'] = 0
  await state.update_data()
  await callback.message.answer(prog_texts["programmeMessage"](), reply_markup=kb.get_programmes_keyboard())
  await callback.answer()


"""
  accepts all the parameters needed to figure out how to update the message according to user's state
"""
async def programmes_page_update(callback: types.CallbackQuery, 
                                 callback_data: kb.progCallbackFactory, 
                                 state: FSMContext,
                                 new_text: str=prog_texts["programmeMessage"]()):
  user_data = await state.get_data()
  category_str = user_data['category'] if callback_data.action == 'list' else callback_data.programme
  try:
    await callback.message.edit_text(new_text,
                                     reply_markup=kb.get_programmes_keyboard(category=category_str,
                                                                             profPage=user_data.get('page_prog', 0)))
  except TelegramBadRequest as e:
    logging.error(f"Failed to edit programmes message: {e}")


"""
  looks at the button's action and changes the variables to represent the state needed
"""
@prog_router.callback_query(kb.progCallbackFactory.filter(F.action != 'registration'))
async def programmes_callback_handler(callback: types.CallbackQuery,
                                      callback_data: kb.progCallbackFactory,
                                      state: FSMContext):
  user_id = callback.from_user.id
  user_data = await state.get_data()
  current_page = user_data.get('page_prog', 0)
  new_text = prog_texts[callback_data.programme]()

  if callback_data.action == 'next':
    current_page = 1
  elif callback_data.action == 'back':
    current_page = 0
  elif callback_data.action == 'menu':
    current_page = 0
  elif callback_data.action == 'deeper':
    user_data['category'] = callback_data.programme
  elif callback_data.action == 'list':
    new_text = prog_texts[user_data['category']]()
  elif callback_data.action == 'stay':
    user_data['current_prog'] = callback_data.programme

  user_data['page_prog'] = current_page
  await state.update_data(user_data)
  await programmes_page_update(callback, callback_data, state, new_text)
  await callback.answer()
