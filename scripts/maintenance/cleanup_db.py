import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("DB_USER", "root")
pwd = os.getenv("DB_PASSWORD", "")
host = os.getenv("DB_HOST", "127.0.0.1")
port = os.getenv("DB_PORT", "3306")
dbname = os.getenv("DB_NAME", "financetrack")

try:
    conn = mysql.connector.connect(user=user, password=pwd, host=host, port=port, database=dbname)
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM categorias WHERE name LIKE '%Teste%'")
    targets = cur.fetchall()
    print('Categorias para remover:', targets)

    for cat_id, name in targets:
        cur.execute("DELETE FROM transacoes WHERE category_id = %s", (cat_id,))
        cur.execute("DELETE FROM categorias WHERE id = %s", (cat_id,))
        print(f'Removido: {name} (id={cat_id})')

    conn.commit()

    cur.execute("SELECT id, name, user_id FROM categorias ORDER BY user_id, name")
    print('Categorias atuais:')
    for row in cur.fetchall():
        print(f'  id={row[0]}, name={row[1]}, user_id={row[2]}')

    cur.close()
    conn.close()
except Exception as e:
    print('Erro:', e)