import psycopg2                           # Psycopg is the most popular PostgreSQL database adapter for the Python programming language.
from   dotenv     import load_dotenv      # Library used for dealing with variables inside python
import os                                 
from   contextlib import contextmanager


load_dotenv()                             # line of command to assist on the use of information inside .env without exposing them.

DATABASE   = os.getenv ('DATABASE')
HOST       = os.getenv ('HOST')
USERSERVER = os.getenv ('USERSERVER')
PASSWORD   = os.getenv ('PASSWORD')
PORT       = os.getenv ('PORT')


@contextmanager
def instance_cursor():
    connection = psycopg2.connect(database = DATABASE, host= HOST, user= USERSERVER, password= PASSWORD, port= PORT)
    cursor     = connection.cursor()             # apoint a cursor to be able to do the dids with the sql
    try:
        yield cursor
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print('Conexão com PostgreSQL fechada')




def runQuery_commit(query):
    '''function responsable with the commit querys'''
    connection = psycopg2.connect(database= DATABASE, host= HOST, user= USERSERVER, password= PASSWORD, port = PORT)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    if (connection):
        cursor.close()
        connection.close()
        print('Conexao com PostgreSQL fechada')


def runQuery_fetchall(query):
    ''''''
    # function responsable with the fetch querys
    with instance_cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()



def criar_tabela(): 
    ''' creating a table inside postgresql'''
    query = '''
        CREATE TABLE REGISTROS(
            nome    varchar(255),
            usuario varchar(255),
            senha   varchar(255)
        )
    '''
    return runQuery_commit(query)


def add_registro(nome, user, senha):
    '''adding information to the table'''
    query = f'''
    INSERT INTO REGISTROS VALUES
    {nome, user, senha}
    '''
    return runQuery_commit(query)


def consulta_geral():
    '''consulting informations on the table'''
    query = '''
    SELECT * 
    FROM REGISTROS    
    '''
    return runQuery_fetchall(query)


def consulta_nome(user):
    '''verifying user names inside the table'''
    query = f'''
    SELECT nome, usuario, senha
    FROM REGISTROS
    WHERE usuario = '{user}'
    '''
    return runQuery_fetchall(query)


# ---------------------------------- /// -------------------------
