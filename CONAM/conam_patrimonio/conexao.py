import fdb 
from fdb.fbcore import Cursor
import pyodbc

conexao_destino = fdb.connect(dsn="localhost:F:\Fiorilli\Cidades\Igaracu-PM\ARQ2021\SCPI2021.FDB", user='fscscpi8',
                     password='scpi', port=3050, charset='WIN1252')

conexao_origem = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;PORT=1433;DATABASE=patrimon;Trusted_Connection=yes')

cursor_origem = conexao_origem.cursor()

cursor_destino = conexao_destino.cursor()

def commit():
    conexao_destino.commit()

def get_cursor_fb():
    return conexao_destino.cursor()

def get_cursor_ms():
    return conexao_origem.cursor()
