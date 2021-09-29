import fdb
import cx_Oracle


dsn_origem = cx_Oracle.makedsn(
    'localhost', 
    '1521', 
    service_name='ORCLPDB1.localdomain',
)

conexao_origem = cx_Oracle.connect(
    user='system', 
    password='Oradoc_db1', 
    dsn=dsn_origem
)

#conexao_destino = fdb.connect(dsn= 'localhost/3050:C:\\Fiorilli\\SCPI_8\\Cidades\\Taquarituba - CM\\ARQ2021\\SCPI2021.FDB', user='fscscpi8',
#                     password='scpi', charset='WIN1252')

conexao_destino = None

def set_connection(server,port,database):
    global conexao_destino
    
    conexao_destino =  fdb.connect(dsn= f'{server}/{port}:{database}', user='fscscpi8',
                    password='scpi', charset='WIN1252')

def get_cursor():
    return conexao_destino.cursor()

def commit():
    conexao_destino.commit()

internal_cursor = conexao_origem.cursor()

def get(sql):
    internal_cursor.execute(sql)
    columns = [i[0].lower() for i in internal_cursor.description]
    return [dict(zip(columns, row)) for row in internal_cursor]