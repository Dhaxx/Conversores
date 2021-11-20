import fdb 
from fdb.fbcore import Cursor
import pyodbc

conexao_destino = fdb.connect(dsn="localhost:C:\Fiorilli\SCPI_8\Cidades\Igaracu_do_Tiete-PM\ARQ2021\SCPI2021.FDB", user='fscscpi8',
                     password='scpi', port=3050, charset='WIN1252')

conexao_origem = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;PORT=1433;DATABASE=siam2020;UID=sa;PWD=Dnal250304')

cursor_origem = conexao_origem.cursor()

cursor_destino = conexao_destino.cursor()

def commit():
    conexao_destino.commit()
