from database import get_connection

def inserir_medida(distance: float):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO esp32_sensor (distance) VALUES (%s)", (distance,))
    conn.commit()
    cursor.close()
    conn.close()

def obter_medidas(limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, distance, data_hora FROM esp32_sensor ORDER BY data_hora DESC LIMIT %s", (limit,))
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": d[0], "distance": d[1], "data_hora": d[2]} for d in dados]
