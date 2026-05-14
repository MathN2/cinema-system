import mysql.connector

def create_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2319"
    )

    cursor = conn.cursor()

    with open('cinema/data/schema.sql', 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    comandos = schema_sql.split(';')

    for comando in comandos:
        comando = comando.strip()

        if comando:
            try:
                cursor.execute(comando)
            except mysql.connector.Error as e:
                print(f"Erro ao executar comando SQL: {comando}")
                print(f"Error message: {e}")

    conn.commit()

    cursor.close()
    conn.close()
