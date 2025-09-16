from flask import Flask, request
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv('.env')

config = {
    'host': os.getenv('DB_HOST', 'localhost'),  # Obtém o host do banco de dados da variável de ambiente
    'user': os.getenv('DB_USER'),  # Obtém o usuário do banco de dados da variável de ambiente
    'password': os.getenv('DB_PASSWORD'),  # Obtém a senha do banco de dados da variável de ambiente
    'database': os.getenv('DB_NAME', 'imoveis'),  # Obtém o nome do banco de dados da variável de ambiente
    'port': int(os.getenv('DB_PORT', 5000)),  # Obtém a porta do banco de dados da variável de ambiente
    'ssl_ca': os.getenv('SSL_CA_PATH')  # Caminho para o certificado SSL
}

def connect_db():
    """Estabelece a conexão com o banco de dados usando as configurações fornecidas."""
    try:
        # Tenta estabelecer a conexão com o banco de dados usando mysql-connector-python
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        # Em caso de erro, imprime a mensagem de erro
        print(f"Erro: {err}")
        return None


app = Flask(__name__)

@app.route('/imoveis', methods=['GET'])
def get_imoveis():
    conn = connect_db()
    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM imoveis')
    data = cursor.fetchall()

    return data, 200

@app.route('/imoveis/<int:id>')
def get_imovel_info(id):
    conn = connect_db()
    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM imoveis WHERE id = %s', (id,))
    data = cursor.fetchone()

    return data, 200

@app.route("/imoveis", methods= ["POST"])
def criar_imovel():
    conn = connect_db()
    if conn is None:
        resp = {"erro":"Nao foi possivel conectar com o banco de dados"}
        return resp, 400
    cursor = conn.cursor(dictionary=True)
    data = request.get_json()
    cursor.execute("""
    INSERT INTO imoveis (
        bairro, cep, cidade, data_aquisicao, logradouro, tipo, tipo_logradouro, valor
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""", (data['bairro'], data['cep'], data['cidade'], data['data_aquisicao'], data['logradouro'], data['tipo'], data['tipo_logradouro'], data['valor']))
    conn.commit()

    return data, 201

@app.route("/imoveis/<int:id>", methods=['PUT'])
def atualizar_imovel(id):
    conn = connect_db()
    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500
    cursor = conn.cursor(dictionary=True)

    data = request.get_json()
    cursor.execute("UPDATE imoveis SET bairro = %s, cep = %s, cidade = %s, data_aquisicao = %s, logradouro = %s, tipo = %s, tipo_logradouro = %s, valor = %s WHERE id = %s",
                   (data['bairro'], data['cep'], data['cidade'], data['data_aquisicao'], data['logradouro'], data['tipo'], data['tipo_logradouro'], data['valor'], id,))
    conn.commit()

    cursor.execute('SELECT * FROM imoveis WHERE id = %s', (id,))
    data = cursor.fetchone()

    return data, 200

@app.route("/imoveis/<int:id>", methods=['DELETE'])
def apagar_imovel(id):
    conn = connect_db()
    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500
    cursor = conn.cursor(dictionary=True)

    cursor.execute("DELETE FROM imoveis WHERE id = %s", (id,))
    conn.commit()
    cursor.execute("SELECT * FROM imoveis")
    data = cursor.fetchall()

    return data, 200

@app.route('/imoveis/<tipo>', methods=["GET"])
def filtrar_imovel(tipo):
    conn = connect_db()
    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM imoveis WHERE tipo = %s", (tipo,))
    data = cursor.fetchall()

    return data, 200

@app.route('/imoveis/<cidade>', methods=["GET"])
def filtrar_por_cidade(cidade):
    conn = connect_db()
    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM imoveis WHERE cidade = %s", (cidade,))
    data = cursor.fetchall()

    return data, 200

if __name__ == '__main__':
    app.run(debug=True)

