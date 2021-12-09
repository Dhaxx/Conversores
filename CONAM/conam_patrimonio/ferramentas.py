import conexao

conexao_destino = conexao.conexao_destino.cursor()

def triggers(status):
    print("Triggers")

    numero = 0 if str(status).lower() == "desliga" else 1
    triggers = [
        "UPDATE RDB$TRIGGERS SET RDB$TRIGGER_INACTIVE =  %s WHERE RDB$TRIGGER_NAME = 'TD_PT_MOVBEM_GEN'" % numero,
        "UPDATE RDB$TRIGGERS SET RDB$TRIGGER_INACTIVE =  %s WHERE RDB$TRIGGER_NAME = 'TBD_PT_MOVBEM_BLOQUEIO'" % numero,
        "UPDATE RDB$TRIGGERS SET RDB$TRIGGER_INACTIVE = %s WHERE RDB$TRIGGER_NAME = 'TD_PT_CADPAT_GEN'" % numero,
        "UPDATE RDB$TRIGGERS SET RDB$TRIGGER_INACTIVE = %s WHERE RDB$TRIGGER_NAME = 'TU_PT_CADPAT_BLOQUEIO'" % numero,
        "UPDATE RDB$TRIGGERS SET RDB$TRIGGER_INACTIVE = %s WHERE RDB$TRIGGER_NAME = 'TBI_PT_CADPAT_SINC'" % numero
    ]

    for cmd in triggers:
        conexao_destino.execute(cmd)

    conexao.commit()

def limpa_tabelas():

    triggers("desliga")

    print("Limpando Tabelas")

    tabelas = [
        'delete from pt_tipomov',
        'delete from pt_movbem',
        'delete from pt_cadpat',
        'delete from pt_cadpats',
        'delete from pt_cadpatd',
        'delete from pt_cadpatg',
        'delete from pt_cadsit',
        'delete from pt_cadtip',
        'delete from pt_cadbai',
        "delete from pt_cadajuste",
        "delete from pt_cadresponsavel"
    ]

    for cmd in tabelas:
        conexao_destino.execute(cmd)

    conexao.commit()

def empresa():
    return int(conexao_destino.execute("SELECT empresa from cadcli").fetchone()[0])

def exercicio():
    return int(conexao_destino.execute("SELECT mexer FROM CADCLI c").fetchone()[0])

# Função de criar campo passando o nome da tabela e a coluna a ser criada
def cria_campo(nome_tabela, nome_campo):
    resultado = conexao_destino.execute(   # Aqui realiza-se uma verificação para validar se a coluna em questão já é existente
        "select count(*) from rdb$relation_fields where rdb$relation_name = '{tabela}' and(rdb$field_name = '{campo}')".format(tabela=nome_tabela.upper(), campo=nome_campo.upper())).fetchone()[0]

    # Se houver a coluna, através do return sairemos da função
    if(resultado == 1): return

    # caso não haja, executa-se um alter table na DB destino inserindo o novo campo
    conexao_destino.execute("alter table {tabela} add {campo} varchar(80)".format(
            tabela=nome_tabela, campo=nome_campo))
    
    conexao.commit()