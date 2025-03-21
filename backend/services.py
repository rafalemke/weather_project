from database import get_connection

def inserir_temperatura(valor: float):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO temperatura (valor) VALUES (%s)", (valor,))
    conn.commit()
    cursor.close()
    conn.close()

def obter_temperaturas(limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, valor, data_hora FROM temperatura ORDER BY data_hora DESC LIMIT %s", (limit,))
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": d[0], "valor": d[1], "data_hora": d[2]} for d in dados]
