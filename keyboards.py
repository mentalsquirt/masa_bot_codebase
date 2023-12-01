from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


# --------------------------------------MENU--------------------------------------
replyMenu = ReplyKeyboardMarkup(keyboard=[
  [KeyboardButton(text="Главное меню")], 
  [KeyboardButton(text="FAQ")],
  [KeyboardButton(text="Профиль")]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню навигации')

startMenuInline = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text="О нас", callback_data='about')],
  [InlineKeyboardButton(text="Программы", callback_data='programmes')],
  [InlineKeyboardButton(text="Гранты и виза", callback_data='grants_visas')]
])


# --------------------------------------REGISTRATION--------------------------------------
class regCallbackFactory(CallbackData, prefix='reg'):
  action: str
  text: str

def get_profile_keyboard(registration: bool, category: str = 'None') -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()
  if registration:
    if category == 'None':
      builder.button(text='Редактировать', callback_data=regCallbackFactory(action="deeper", text='regEdit'))
      builder.button(text='История', callback_data=regCallbackFactory(action = "deeper", text='regHistory'))
    if category == "regEdit":
      builder.button(text="Имя", callback_data=regCallbackFactory(action="edit", text='regEditName'))
      builder.button(text="Телефон", callback_data=regCallbackFactory(action="edit", text='regEditPhone'))
      builder.button(text="Почта", callback_data=regCallbackFactory(action="edit", text='regEditEmail'))
    if category != 'None':
      builder.button(text='К профилю', callback_data=regCallbackFactory(action='menu', text="None"))
  else:
    builder.button(text='Зарегистрироваться', callback_data=regCallbackFactory(action='rega', text='rega'))
  builder.adjust(3, 1)
  return builder.as_markup()



# --------------------------------------SEND--------------------------------------
class senderCallbackFactory(CallbackData, prefix='sendData'):
  data: str

def get_confirmation_keyboard():
  builder = InlineKeyboardBuilder()
  builder.button(text='Да, хочу!', callback_data=senderCallbackFactory(data='sendData'))
  builder.button(text='Нет, не сейчас', callback_data=senderCallbackFactory(data='dontSendData'))
  builder.adjust(2)
  return builder.as_markup()

def get_yes_or_no():
  builder = InlineKeyboardBuilder()
  builder.button(text='Да', callback_data="confirmYes")
  builder.button(text='Нет', callback_data="confirmNo")
  builder.adjust(2)
  return builder.as_markup()


# --------------------------------------ABOUT--------------------------------------
class aboutCallbackFactory(CallbackData, prefix='about'):
  data: str
  
def get_about_keyboard() -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()
  builder.button(text='Сообщество Маса', callback_data=aboutCallbackFactory(data='aboutCommunity'))
  builder.button(text='Контактные данные', callback_data=aboutCallbackFactory(data='aboutContacts'))
  builder.button(text='Наш блог', callback_data=aboutCallbackFactory(data='aboutBlog'))
  builder.button(text='Выпускникам', callback_data=aboutCallbackFactory(data='aboutGraduates'))
  builder.button(text='Родителям', callback_data=aboutCallbackFactory(data='aboutParents'))
  builder.adjust(1, 2, 2)
  return builder.as_markup()



# --------------------------------------PROGRAMMES--------------------------------------
class progCallbackFactory(CallbackData, prefix='prog'):
  action: str
  programme: str

"""
  helper functions with which we build new keyboards according to the user's state
"""
def get_academic_keyboard():
  builder = InlineKeyboardBuilder()
  builder.button(text="Oranim — Pre M.A.", callback_data=progCallbackFactory(action='stay', programme="progOranimPreMA"))
  builder.button(text="Ariel University — B.A.", callback_data=progCallbackFactory(action='stay', programme="progArielBA"))
  builder.button(text="Ariel University — M.A", callback_data=progCallbackFactory(action='stay', programme="progArielMA"))
  builder.button(text="Ariel University — Research", callback_data=progCallbackFactory(action='stay', programme="progArielResearch"))
  builder.button(text="Masa Oranim — English for the Workplace", callback_data=progCallbackFactory(action='stay', programme="progOranimEnglish"))
  builder.button(text="Oranim - A.T.I. Intensive", callback_data=progCallbackFactory(action='stay', programme="progOranimATI"))
  return builder

def get_internship_keyboard():
  builder = InlineKeyboardBuilder()
  builder.button(text="Shilton Betar — Media", callback_data=progCallbackFactory(action='stay', programme="progShiltonMedia"))
  builder.button(text="Israel Way — Career Growth", callback_data=progCallbackFactory(action='stay', programme="progWayCareer"))
  builder.button(text="Tlalim — Start", callback_data=progCallbackFactory(action='stay', programme="progTlalimStart"))
  builder.button(text="Masa Israel XP — Master plus Status", callback_data=progCallbackFactory(action='stay', programme="progXPMaster"))
  builder.button(text="Masa Sachlav — Top Israel Interns", callback_data=progCallbackFactory(action='stay', programme="progSachlavTop"))
  return builder

def get_professional_keyboard(profPage: int):
  builder = InlineKeyboardBuilder()
  if profPage == 0: 
    builder.button(text="Shilton Betar — Media", callback_data=progCallbackFactory(action='stay', programme="progShiltonMedia"))
    builder.button(text="Israel Way — Melamedia", callback_data=progCallbackFactory(action='stay', programme="progWayMelamedia"))
    builder.button(text="Israel Way — Web/Graphic Design", callback_data=progCallbackFactory(action='stay', programme="progWayWeb"))
    builder.button(text="Sachlav — Ofek", callback_data=progCallbackFactory(action='stay', programme="progSachlavOfek"))
    builder.button(text="Masa Israel XP — Young Doctors", callback_data=progCallbackFactory(action='stay', programme="progXPDoctors"))
    builder.button(text="Masa Israel XP — Young Dentists", callback_data=progCallbackFactory(action='stay', programme="progXPDentists"))
    builder.button(text="Tlalim — Culinary Art", callback_data=progCallbackFactory(action='stay', programme="progCulinaryArt"))
    builder.button(text="Masa Israel XP — Master plus Status", callback_data=progCallbackFactory(action='stay', programme="progXPMaster"))
    builder.button(text="Tlalim — Digital Design", callback_data=progCallbackFactory(action='stay', programme="progTlalimDigitalDesign"))
    builder.button(text="Tlalim — Extreme Surfing", callback_data=progCallbackFactory(action='stay', programme="progTlalimSurfing"))
    builder.button(text="—>", callback_data=progCallbackFactory(action='next', programme='progProfAll'))
  if profPage == 1: 
    builder.button(text="Tlalim — Group Facilitation", callback_data=progCallbackFactory(action='stay', programme="progTlalimGroup"))
    builder.button(text="Tlalim — Video Production", callback_data=progCallbackFactory(action='stay', programme="progTlalimVideo"))
    builder.button(text="Tlalim — MDL: Masa Doctors License", callback_data=progCallbackFactory(action='stay', programme="progTlalimMDL"))
    builder.button(text="Tlalim — Digital Marketing", callback_data=progCallbackFactory(action='stay', programme="progTlalimDigitalMarket"))
    builder.button(text="Tlalim — Red Sea Divers", callback_data=progCallbackFactory(action='stay', programme="progTlalimDivers"))
    builder.button(text="Tlalim — Motion Design", callback_data=progCallbackFactory(action='stay', programme="progTlalimMotion"))
    builder.button(text="Tlalim — WEB Development", callback_data=progCallbackFactory(action='stay', programme="progTlalimWeb"))
    builder.button(text="Tlalim — Hotel Administration", callback_data=progCallbackFactory(action='stay', programme="progTlalimHotel"))
    builder.button(text="Tlalim — JAVA ANDROID Development", callback_data=progCallbackFactory(action='stay', programme="progTlalimJavaAndroid"))
    builder.button(text="Masa Israel XP — Hi-Tech", callback_data=progCallbackFactory(action='stay', programme="progXPHiTech"))
    builder.button(text="Nitzana — Masa Desert Challange", callback_data=progCallbackFactory(action='stay', programme="progNitzanaDesert"))
    builder.button(text="<—", callback_data=progCallbackFactory(action='back', programme='progProfAll')) 
  return builder
  
def get_language_keyboard():
  builder = InlineKeyboardBuilder()
  builder.button(text="Shilton Betar — Mabat Maof", callback_data=progCallbackFactory(action='stay', programme="progShiltonMaof"))
  builder.button(text="Israel Way — English in the City", callback_data=progCallbackFactory(action='stay', programme="progWayEnglish"))
  builder.button(text="Israel Way — Hebrew in the City", callback_data=progCallbackFactory(action='stay', programme="progWayHebrew"))
  builder.button(text="Sachlav — Ofek", callback_data=progCallbackFactory(action='stay', programme="progSachlavOfek"))
  builder.button(text="Masa Sachlav — Top Israel Interns", callback_data=progCallbackFactory(action='stay', programme="progSachlavTop"))
  builder.button(text="Masa Oranim — English for the Workplace", callback_data=progCallbackFactory(action='stay', programme="progOranimEnglish"))
  builder.button(text="Masa Israel XP — Master plus Status", callback_data=progCallbackFactory(action='stay', programme="progXPMaster"))
  return builder
  
def get_medicine_keyboard():
  builder = InlineKeyboardBuilder()
  builder.button(text="Masa Israel XP — Young Doctors", callback_data=progCallbackFactory(action='stay', programme="progXPDoctors"))
  builder.button(text="Masa Israel XP — Young Dentists", callback_data=progCallbackFactory(action='stay', programme="progXPDentists"))
  builder.button(text="Masa Tlalim — Pharmacist in Israel", callback_data=progCallbackFactory(action='stay', programme="progTlalimPharmacist"))
  builder.button(text="Tlalim — MDL: Masa Doctors License", callback_data=progCallbackFactory(action='stay', programme="progTlalimMDL"))
  return builder
  
def get_tech_keyboard():
  builder = InlineKeyboardBuilder()
  builder.button(text="Sachlav — Ofek", callback_data=progCallbackFactory(action='stay', programme="progSachlavOfek"))
  builder.button(text="MasaTech", callback_data=progCallbackFactory(action='stay', programme="progMasaTech"))
  builder.button(text="Tlalim — WEB Development", callback_data=progCallbackFactory(action='stay', programme="progTlalimWeb"))
  builder.button(text="Tlalim — JAVA ANDROID Development", callback_data=progCallbackFactory(action='stay', programme="progTlalimJavaAndroid"))
  builder.button(text="Masa Israel XP — Hi-Tech", callback_data=progCallbackFactory(action='stay', programme="progXPHiTech"))
  return builder


"""
  only this function is being called outside of the keyboards file — the rest are helpers to build the desired keyboard
"""
def get_programmes_keyboard(category: str = "None", profPage: int = 0) -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()
  if category == "None":  # list of all categories
    builder.button(text="Академические программы", callback_data=progCallbackFactory(action='deeper', programme="progAcademicAll"))
    builder.button(text="Стажировки", callback_data=progCallbackFactory(action='deeper', programme="progInternshipAll"))
    builder.button(text="Профессиональные курсы", callback_data=progCallbackFactory(action='deeper', programme="progProfAll"))
    builder.button(text="Языковые курсы", callback_data=progCallbackFactory(action='deeper', programme="progLanguageAll"))
    builder.button(text="Врачи и стоматологи", callback_data=progCallbackFactory(action='deeper', programme="progMedicineAll"))
    builder.button(text="IT & MasaTech", callback_data=progCallbackFactory(action='deeper', programme="progTechAll"))
    builder.button(text="Remote", callback_data=progCallbackFactory(action='deeper', programme="progRemoteAll"))
    builder.button(text='Я не могу выбрать...', callback_data=progCallbackFactory(action='stay', programme="progHelper"))
  if category == "progAcademicAll":
    builder = get_academic_keyboard()
  if category == "progInternshipAll":
    builder = get_internship_keyboard()
  if category == "progProfAll":
    builder = get_professional_keyboard(profPage)
  if category == "progLanguageAll":
    builder = get_language_keyboard()
  if category == "progMedicineAll":
    builder = get_medicine_keyboard()
  if category == "progTechAll":
    builder = get_tech_keyboard()
  if category == "progRemoteAll":
    builder.button(text="Masa Remote",
                   callback_data=progCallbackFactory(action='stay', programme="progMasaRemote"))
  if "All" not in category \
  and "None" not in category \
  and "progHelper" not in category:
    builder.button(text="Связаться с организатором",
                   callback_data=progCallbackFactory(action='registration', programme="None"))
    builder.button(text="К списку <—",
                   callback_data=progCallbackFactory(action='list', programme="None"))
  if category != "None":
    builder.button(text="Все категории",
                   callback_data=progCallbackFactory(action='menu', programme="None"))
  builder.adjust(1, repeat=True)
  return builder.as_markup()
    


# --------------------------------------GRANTS/VISAS--------------------------------------
def get_grants_visas_keyboard() -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()
  builder.button(text="Гранты",
                 callback_data='grants')
  builder.button(text="Визы",
                 callback_data='visas')
  return builder.as_markup()



# --------------------------------------GRANTS--------------------------------------
class grantCallbackFactory(CallbackData, prefix='grant'):
  data: str

def get_grants_keyboard() -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()
  builder.button(text="О грантах",
                 callback_data=grantCallbackFactory(data="grantAbout"))
  builder.button(text="Условия",
                 callback_data=grantCallbackFactory(data="grantRequirements"))
  builder.adjust(2)
  return builder.as_markup()



# --------------------------------------VISAS--------------------------------------
class visasCallbackFactory(CallbackData, prefix='visas'):
  data: str

def get_visas_keyboard() -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()
  builder.button(text="Виза Маса А2",
                 callback_data=visasCallbackFactory(data="visasA2"))
  builder.button(text="Виза B1 (Masa Tech)",
                 callback_data=visasCallbackFactory(data="visasB1"))
  builder.button(text="Под конец программы",
                 callback_data=visasCallbackFactory(data="visasEnd"))
  builder.button(text="Несовершеннолетним",
                 callback_data=visasCallbackFactory(data="visasUnderage"))
  builder.adjust(2, 1, 1)
  return builder.as_markup()



# --------------------------------------FAQ--------------------------------------
class faqCallbackFactory(CallbackData, prefix='faq'):
  action: str
  question: str

def get_faq_keyboard(page: int = 0) -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()
  has_next_page = 0 <= page < 1
  if page == 0:
    builder.button(text="Что такое Маса?",
                   callback_data=faqCallbackFactory(action='stay', question='faqMasa'))
    builder.button(text="Какие программы Маса существуют сегодня?",
                   callback_data=faqCallbackFactory(action='stay', question='faqProgram'))
    builder.button(text="Как определяется стоимость программы?",
                   callback_data=faqCallbackFactory(action='stay', question='faqCost'))
    builder.button(text="Кто такие «провайдеры»?",
                   callback_data=faqCallbackFactory(action='stay', question='faqProvider'))
    builder.button(text="Могу ли я работать во время программы?",
                   callback_data=faqCallbackFactory(action='stay', question='faqWork'))
    builder.button(text="Эмигрантам стран бывшего СССР",
                   callback_data=faqCallbackFactory(action='stay', question="faqRusForeignResidents"))
    builder.button(text="Отпуск во время программы?",
                   callback_data=faqCallbackFactory(action='stay', question='faqVacation'))
    builder.button(text="Безопасность и защита",
                   callback_data=faqCallbackFactory(action='stay', question='faqParticipantSafety'))
  if page == 1:
    builder.button(text="Правила безопасности при поездках в Израиль",
                   callback_data=faqCallbackFactory(action='stay', question="faqSafety"))
    builder.button(text="Кто имеет право на получение гранта Маса?",
                   callback_data=faqCallbackFactory(action='stay', question='faqGrant'))
    builder.button(text="Получаю ли я грант «на руки»?",
                   callback_data=faqCallbackFactory(action='stay', question="faqGrantHandout"))
    builder.button(text="Отказ от программы — потеря гранта?",
                   callback_data=faqCallbackFactory(action='stay', question="faqLostGrant"))
    builder.button(text="Где и когда подаётся заявка на грант?",
                   callback_data=faqCallbackFactory(action='stay', question='faqApply'))
    builder.button(text="Англоязычные программы",
                   callback_data=faqCallbackFactory(action="stay", question="faqGrantEnglish"))
    builder.button(text="Иврит",
                   callback_data=faqCallbackFactory(action="stay", question="faqGrantHebrew"))
    builder.button(text="Дополнительная информация",
                   callback_data=faqCallbackFactory(action='stay', question='faqContact'))
  
  # pagination
  if page != 0:
    builder.button(text="<—",
                   callback_data=faqCallbackFactory(action='back', question="None"))
  if has_next_page:
    builder.button(text="—>",
                   callback_data=faqCallbackFactory(action='next', question="None"))
  builder.adjust(1, repeat=True)
  return builder.as_markup()

