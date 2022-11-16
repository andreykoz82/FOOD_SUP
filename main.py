from scripts.helper_func import create_connection
from scripts.helper_func import read_txt_file
from scripts.helper_func import create_record
from scripts.helper_func import to_excel
from scripts.helper_func import get_data_to_export
from scripts.helper_func import check_for_case
from scripts.helper_func import check_for_box
import streamlit as st
from PIL import Image
from datetime import datetime


database = r"db\food_sup.db"
items_txt = r"db\actual_items.txt"
box_1 = Image.open(r'img\box_1.png')
box_2 = Image.open(r'img\box_2.png')

conn = create_connection(database)

items = read_txt_file(items_txt)

st.header("Ввод информации:")

col1, col2 = st.columns(2)

with col1:
    st.header("Выберите данные")
    prod_line = st.selectbox(
    'Производственная линия:',
    ('ИМА С21', 'ИМА С50.1', 'ИМА С50.2', 
    'ИМА С51', 'ББЛ-1', 'ББЛ-2', 'ББЛ-3', 
    'Консумаш'))
    actual_item = st.selectbox('Номенклатура', items)

with col2:
    st.header("Введите данные")
    production_order = st.text_input('Номер заказа')
    batch_number = st.text_input('Номер серии:')

st.header("Агрегация:")

case_sn = st.text_input('Номер короба:')

col1, col2, col3, col4, col5 = st.columns(5, gap='small')

with col1:
    box_1_sn = st.text_input('1', label_visibility='hidden')
    if not box_1_sn:
        st.image(box_1)
    else:
        st.image(box_2)
with col2:
    box_2_sn = st.text_input('2', label_visibility='hidden')
    if not box_2_sn:
        st.image(box_1)
    else:
        st.image(box_2)
with col3:
    box_3_sn = st.text_input('3', label_visibility='hidden')
    if not box_3_sn:
        st.image(box_1)
    else:
        st.image(box_2)
with col4:
    box_4_sn = st.text_input('4', label_visibility='hidden')
    if not box_4_sn:
        st.image(box_1)
    else:
        st.image(box_2)
with col5:
    box_5_sn = st.text_input('5', label_visibility='hidden')
    if not box_5_sn:
        st.image(box_1)
    else:
        st.image(box_2)

col6, col7, col8, col9, col10 = st.columns(5, gap='small')

with col6:
    box_6_sn = st.text_input('6', label_visibility='hidden')
    if not box_6_sn:
        st.image(box_1)
    else:
        st.image(box_2)
with col7:
    box_7_sn = st.text_input('7', label_visibility='hidden')
    if not box_7_sn:
        st.image(box_1)
    else:
        st.image(box_2)
with col8:
    box_8_sn = st.text_input('8', label_visibility='hidden')
    if not box_8_sn:
        st.image(box_1)
    else:
        st.image(box_2)
with col9:
    box_9_sn = st.text_input('9', label_visibility='hidden')
    if not box_9_sn:
        st.image(box_1)
    else:
        st.image(box_2)
with col10:
    box_10_sn = st.text_input('10', label_visibility='hidden')
    if not box_10_sn:
        st.image(box_1)
    else:
        st.image(box_2)

if st.button('Агрегировать'):

    check_case = check_for_case(conn=conn, case_sn=case_sn)

    box_search = []
    case_with_boxes = (box_1_sn, box_2_sn, box_3_sn, box_4_sn, box_5_sn, box_6_sn, box_7_sn, box_8_sn, box_9_sn, box_10_sn)
    for box in case_with_boxes:
        if check_for_box(conn, box_sn=box) is None:
            box_search.append(None)
        else:
            box_search.append(check_for_box(conn, box_sn=box)[0])

    if check_case:
        st.write("Короб уже существует")
    elif any((True for x in case_with_boxes if x in set(box_search))):
        st.write("Пачка уже существует")
    else:
        now = datetime.today().isoformat()
        box_1_record = (now, production_order, actual_item, prod_line, batch_number, case_sn, box_1_sn)
        box_2_record = (now, production_order, actual_item, prod_line, batch_number, case_sn, box_2_sn)
        box_3_record = (now, production_order, actual_item, prod_line, batch_number, case_sn, box_3_sn)
        box_4_record = (now, production_order, actual_item, prod_line, batch_number, case_sn, box_4_sn)
        box_5_record = (now, production_order, actual_item, prod_line, batch_number, case_sn, box_5_sn)
        box_6_record = (now, production_order, actual_item, prod_line, batch_number, case_sn, box_6_sn)
        box_7_record = (now, production_order, actual_item, prod_line, batch_number, case_sn, box_7_sn)
        box_8_record = (now, production_order, actual_item, prod_line, batch_number, case_sn, box_8_sn)
        box_9_record = (now, production_order, actual_item, prod_line, batch_number, case_sn, box_9_sn)
        box_10_record = (now, production_order, actual_item, prod_line, batch_number, case_sn, box_10_sn)

        create_record(conn, box_1_record)
        create_record(conn, box_2_record)
        create_record(conn, box_3_record)
        create_record(conn, box_4_record)
        create_record(conn, box_5_record)
        create_record(conn, box_6_record)
        create_record(conn, box_7_record)
        create_record(conn, box_8_record)
        create_record(conn, box_9_record)
        create_record(conn, box_10_record)

        st.write('Успешно агрегировано')
else: 
    st.write('Ошибка агрегации')


df = get_data_to_export(conn, task=(production_order, batch_number))

df_xlsx = to_excel(df)
st.download_button(label='📥 Скачать данные по агрегации',
                                data=df_xlsx ,
                                file_name= f'data_{production_order}.xlsx')