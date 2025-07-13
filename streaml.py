import streamlit as st
#import pyqrcode
import qrcode
from io import BytesIO
#from annotated_text import annotated_text


RATES = st.secrets['rates']
RATES2 = st.secrets['rates2']

logo_image_name = "pic_logo.png"
giant_str_logo = st.secrets["pics"][logo_image_name.split(".")[0]]
im_logo = Image.open(io.BytesIO(base64.decodebytes(bytes(giant_str_logo, "utf-8"))))
st.logo(np.array(im_logo), size='large')

password = ''
initial_cards = st.secrets['anketa']['card_types']

def generate_qr_code(data: str):
    qr_img = qrcode.make(data)
    buffered = BytesIO()
    qr_img.save(buffered, format="PNG")
    return buffered.getvalue()

# def on_change(card_type):
#     if card_type:
#         card_type = card_type.split(":star:")[0]
#     for number,i in enumerate(initial_cards):
#         if i == card_type:
#             st.session_state["card_index"] = number
#     #st.write(card_type)

# def on_change():
#     if "card_type" in st.session_state:
#         if st.session_state['card_type']:
#             card_type = st.session_state["card_type"].split(":star:")[0]
#             for number, i in enumerate(initial_cards):
#                 if i == card_type:
#                     st.session_state["card_index"] = number
# def on_change():
#     """Обработчик изменения выбора карты"""
#     if "card_type_radio" in st.session_state:
#         selected = st.session_state.card_type_radio
#         clean_type = selected.split(":star:")[0].strip()
#         if clean_type in initial_cards:
#             st.session_state.clean_card_type = clean_type
#             st.session_state.card_index = initial_cards.index(clean_type)

def on_change():
    # Проверяем, что значение существует в session_state
    if "card_type_radio" not in st.session_state:
        return
        
    selected = st.session_state.card_type_radio
    
    # Защита от None и пустых значений
    if not selected:
        return
    
    # Извлекаем чистый тип карты (без рекомендаций)
    clean_type = selected.split(":star:")[0].strip()
    if clean_type in initial_cards:
        st.session_state.clean_card_type = clean_type
        st.session_state.card_index = initial_cards.index(clean_type)

def rec(name:str, country:str):
    rec_no = 999
    cards = []
    if any(sub.lower() in name.lower() for sub in st.secrets['anketa']['fav_names'][12:16]):
        rec_no = 2
    elif any(sub.lower() in name.lower() for sub in st.secrets['anketa']['fav_names'][0:1]):
        rec_no = 0
    elif any(sub.lower() in name.lower() for sub in st.secrets['anketa']['fav_names'][1:3]):
        rec_no = 1
    elif any(sub.lower() in name.lower() for sub in st.secrets['anketa']['fav_names'][3:6]):   
        rec_no = 4
    elif any(sub.lower() in name.lower() for sub in st.secrets['anketa']['fav_names'][6:12]): 
        rec_no = 3
    elif country in st.secrets['anketa']['countries'][2:4] and not any(sub.lower() in name.lower() for sub in st.secrets['anketa']['fav_names']):
        rec_no = 2

    for number,i in enumerate(initial_cards):
        if number != rec_no:
            cards.append(i)
        else:
            cards.append(i+":star: :orange[рекомендовано для вас]")
    #on_change(card_type)
    return cards

if st.query_params:
    if 'clean_card_type' not in st.session_state:
        st.session_state.clean_card_type = st.query_params["card_type"]

    name = st.query_params["name"]
    pol = st.query_params["pol"]
    pol_index = 0 if pol == 'Ж' else 1
    country = st.query_params["country"]
    for number,i in enumerate(st.secrets['anketa']['countries']):
        if i == country:
            country_index = number
    current_card_type = st.query_params["card_type"]
    if "card_index" not in st.session_state:
        for number,i in enumerate(initial_cards):
            if i == current_card_type:
                st.session_state["card_index"] = number
    currency = [i for i in st.query_params["currency"].split("_")]
    defaults = currency

    if "role_index" in st.query_params:
        role_index = int(st.query_params["role_index"])
    else: 
        role_index=None

    if "name2" in st.query_params:
        name2 = st.query_params["name2"] 
    else: 
        name2 = ""
    
    wishes = st.query_params["wishes"]

    password = st.text_input("Введите пароль")
else:
    # if 'card_index' not in st.session_state:
    #     st.session_state.card_index = 0
    # if "card_type_radio" not in st.session_state:
    #     st.session_state.card_type_radio = 0
    if 'clean_card_type' not in st.session_state:
        st.session_state.clean_card_type = ""#initial_cards[0]


    name = ""
    pol_index = None
    if "card_index" not in st.session_state:
        st.session_state["card_index"] = None
    country_index=None
    if "card_type" not in st.session_state:
        st.session_state["card_type"] = None
    card_type = ""
    currency = ""
    role_index = None
    name2 = ""
    defaults = None
    wishes = ""



if not st.query_params or password == st.secrets['DEVMODE']:

    #
    st.title(st.secrets['anketa']['titles'][0])

    # 1
    name = st.text_input("1\. Ваше имя :", value=name, placeholder=st.secrets['anketa']['fav_names'][0])
    st.write("")

    # 2
    pol = st.radio("2\. Выберите пол :", ["Ж","M"], 
                        horizontal=True, captions=st.secrets['anketa']['pol'],
                        index=pol_index)
    st.write("")

    # 3
    country = st.selectbox("3\. Выберите ваш регион :", st.secrets['anketa']['countries'],
                           index=country_index,
                           on_change=on_change())
    st.write("")
    

    recommended = rec(name,  country)
    # 4
    card_type = st.radio("4\. Выберите тип карты :", recommended, 
                        horizontal=False, 
                        captions=st.secrets['anketa']['descriptions'],
                        index=st.session_state["card_index"],
                        key="card_type_radio",
                        on_change=on_change())
    current_card_type = st.session_state.clean_card_type
    st.write("")
    # if recommended is not None:
    #     st.session_state["card_index"] = recommended.index(card_type)
    # if st.session_state["card_type"]:
    #     card_type = st.session_state["card_type"].split(":star:")[0]
        
    # for number,i in enumerate(initial_cards):
    #     if i == card_type:
    #         st.session_state["card_index"] = number
    #st.write(card_type)

    
    # st.caption(st.secrets['anketa']['descriptions_extra'][0])
    # st.caption(st.secrets['anketa']['descriptions_extra'][1])

    every_cur = [f'{i} , {st.secrets.cur[i]["forms"][4]}' for i in RATES.keys()] + st.secrets['anketa']['main_cur'] + st.secrets['anketa']['not_convertable_cur']
    disabled = False
    

    if current_card_type == initial_cards[0]:
        # st.write("111")
        defaults = st.secrets['anketa']['main_cur']
        disabled = True
        every_cur = [f'{i} , {st.secrets.cur[i]["forms"][4]}' for i in RATES.keys()] + st.secrets['anketa']['main_cur'] + st.secrets['anketa']['not_convertable_cur']
    elif current_card_type == initial_cards[1]:
        # st.write("222")
        defaults = st.secrets['anketa']['not_convertable_cur'][0:1]
        disabled = True
        every_cur = [f'{i} , {st.secrets.cur[i]["forms"][4]}' for i in RATES.keys()] + st.secrets['anketa']['main_cur'] + st.secrets['anketa']['not_convertable_cur']
    elif current_card_type == initial_cards[2]:
        # st.write("333")
        #defaults = None
        every_cur = [f'{i} , {st.secrets.cur[i]["forms"][4]}' for i in RATES.keys()]
        disabled = False
    elif current_card_type == initial_cards[3]:
        # st.write("444")
        defaults = st.secrets['anketa']['not_convertable_cur'][1:2]
        disabled = True
        every_cur = [f'{i} , {st.secrets.cur[i]["forms"][4]}' for i in RATES.keys()] + st.secrets['anketa']['main_cur'] + st.secrets['anketa']['not_convertable_cur']    
    elif current_card_type == initial_cards[4]:
        #st.write("555")
        defaults = st.secrets['anketa']['not_convertable_cur'][2:]
        disabled = True
        every_cur = [f'{i} , {st.secrets.cur[i]["forms"][4]}' for i in RATES.keys()] + st.secrets['anketa']['main_cur'] + st.secrets['anketa']['not_convertable_cur']   
        
        additional_info = st.radio("4\.1\. Вы :", st.secrets['anketa']['add_info'][0], 
                        horizontal=True, captions=st.secrets['anketa']['add_info'][1],
                        index=role_index)
        if additional_info == st.secrets['anketa']['add_info'][0][0]:
            role_index = 0
            name2 = st.text_input("4\.2\."+st.secrets['anketa']['add_info'][2][0], 
                                  placeholder=st.secrets['anketa']['fav_names'][0],
                                  value=name2)
        elif additional_info == st.secrets['anketa']['add_info'][0][1]:  
            role_index = 1
            name2 = st.text_input("4\.2\."+st.secrets['anketa']['add_info'][2][1], 
                                  placeholder=st.secrets['anketa']['fav_names'][0],
                                  value=name2)
    # else:
    #     st.write("666")

    # 5
    currency = st.multiselect(
        "5\. Выберите до 3 валют для карты (включительно) :",
        options=every_cur,
        default=defaults,
        disabled=disabled,
        max_selections=3
    )
    st.write("Валюты вашей карты :")
    if currency:
        for i in currency:
            st.write(f"- {i}")
    else:
        st.write(f"- не выбрано")
    st.write("")
    
    # 6
    wishes = st.text_area("6\. Ваши дополнительные пожелания. Возможно , мы их учтём.",
                          value=wishes)
    st.write("")

    #st.badge("Условия :")
    #annotated_text(('Условия :', '', '#fea'))
    st.subheader("7\. Условия")
    st.write(st.secrets['anketa']['rules'][0])
    st.caption(st.secrets['anketa']['rules'][1]) 
    st.caption(st.secrets['anketa']['rules'][2])
    st.caption(st.secrets['anketa']['rules'][3])
    st.caption(st.secrets['anketa']['rules'][4])
    st.caption(st.secrets['anketa']['rules'][5])
    st.caption(st.secrets['anketa']['rules'][6])
    st.write("   ")
    st.write("   ")
    check_yes = st.checkbox(st.secrets['anketa']['rules'][7])

    # button
    if st.button("Подтвердить"):
        if check_yes:
            if current_card_type == initial_cards[4] and (role_index is None or name2 == ""):
                st.write("Заполните дополнительные поля к пункту 4")
            else:
                if name and pol and country and current_card_type and currency:
                    #if ВСЕ ПОЛЯ ЗАПОЛНЕНЫ
                    currency_merged = '_'.join(cur for cur in currency)
                    #
                    query_params = {"name": name, 
                                    "pol": pol,
                                    "country":country,
                                    "card_type": current_card_type, 
                                    "currency": currency_merged,
                                    "role_index": role_index,
                                    "name2" : name2,
                                    "wishes": wishes}

                    url =f"{st.secrets['create_page']}/?name={query_params['name']}&pol={query_params['pol']}&country={query_params['country']}&card_type={query_params['card_type']}&currency={query_params['currency']}&wishes={query_params['wishes']}"+(current_card_type == initial_cards[4])*f"&role_index={role_index}&name2={name2}"
        
                    qr_bytes = generate_qr_code(url)

                    st.success("""Анкета успешно заполнена.  
                            Сфотографируйте или заскриньте QR-код и отправьте нам.""")
                    st.image(qr_bytes, width=st.secrets['qr_size'])

                    #st.write(url)
                else:
                    st.write("Вы заполнили не все поля.")
        else:
            st.write("Пожалуйста, ознакомьтесь с условиями.")
    


    st.divider()
    st.caption(st.secrets['anketa']['descriptions_extra'][0])
    st.caption(st.secrets['anketa']['descriptions_extra'][1])

    with st.expander(st.secrets['anketa']['titles'][1]):

        curs_left = RATES.keys()
        curs_right = RATES.keys()

        for from_cur in curs_left:
            st.subheader(f"{from_cur}")
            st.caption(f"{st.secrets.cur[from_cur]['forms'][4]}")
            
            for to_cur in curs_right:
        
                if from_cur == to_cur:
                    continue
                rate_from = RATES[from_cur]
                rate_to = RATES[to_cur]

                x = 1
                y = round(rate_to / rate_from, 4)
                st.metric(label="", value =f"{x} {from_cur} = {y} {to_cur}")
            st.divider()

        st.subheader(f"NSN")
        st.caption(f"{st.secrets.cur['NSN']['forms'][4]}")
        for to_cur in RATES2.keys():
            if to_cur == 'NSN':
                continue
            rate_from = RATES2['NSN']
            rate_to = RATES2[to_cur]

            x = 10
            y = round(x*rate_to / rate_from, 0)
            st.metric(label="", value =f"{x} NSN = {y} {to_cur}")
