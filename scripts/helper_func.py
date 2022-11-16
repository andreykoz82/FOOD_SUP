import sqlite3
import pandas as pd
from io import BytesIO

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_record(conn, task):
    """
    Create a new task
    :param conn:
    :param task: tuple of data
    :return:
    """

    sql = ''' INSERT INTO food_sup_data(date, production_order, item, production_line, 
                                batch_number, case_sn, box_sn)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

    return cur.lastrowid

def read_txt_file(filename):
    items = []
    with open(filename,  encoding = 'utf-8') as file:
        for line in file:
            items.append(line.rstrip())
    return items

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_data_to_export(conn, task):
    sql = f''' SELECT * FROM food_sup_data WHERE production_order="{task[0]}" AND batch_number="{task[1]}";'''
    df = pd.read_sql_query(sql, conn)
    return df

def check_for_case(conn, case_sn):
    cur = conn.cursor()
    cur.execute("""SELECT case_sn FROM food_sup_data WHERE case_sn=?""", (case_sn, ))
    return cur.fetchone()

def check_for_box(conn, box_sn):
    cur = conn.cursor()
    cur.execute("""SELECT box_sn FROM food_sup_data WHERE box_sn=?""", (box_sn, ))
    return cur.fetchone()
