import conexao

conexao_destino = conexao.conexao_destino.cursor()

def triggers(status):
    print("Triggers")

    numero = 0 if str(status).lower() == "desliga" else 1
    triggers = [
        "UPDATE RDB$TRIGGERS SET RDB$TRIGGER_INACTIVE =  %s WHERE RDB$TRIGGER_NAME = 'TBI_ICADREQ'" % numero,
        "UPDATE RDB$TRIGGERS SET RDB$TRIGGER_INACTIVE =  %s WHERE RDB$TRIGGER_NAME = 'TBU_ICADREQ'" % numero,
        "UPDATE RDB$TRIGGERS SET RDB$TRIGGER_INACTIVE = %s WHERE RDB$TRIGGER_NAME = 'TD_ICADREQ'" % numero,
        "UPDATE RDB$TRIGGERS SET RDB$TRIGGER_INACTIVE = %s WHERE RDB$TRIGGER_NAME = 'TI_ICADREQ'" % numero,
        "UPDATE RDB$TRIGGERS SET RDB$TRIGGER_INACTIVE = %s WHERE RDB$TRIGGER_NAME = 'TU_ICADREQ'" % numero,
    ]

    for cmd in triggers:
        conexao_destino.execute(cmd)

    conexao.commit()

def limpa_tabelas():

    triggers("desliga")

    print("Limpando Tabelas")

    tabelas = [
        "delete from licitcomiss",
        "delete from regpreco_saldo_ant",
        "delete from regpreco",
        "delete from regprecohis",
        "delete from regprecodoc",
        "delete from cadpro",
        "delete from cadpro_final",
        "delete from cadpro_lance",
        "delete from cadpro_proposta",
        "delete from cadpro_status",
        "delete from cadprolic_detalhe",
        "delete from cadprolic",
        "delete from prolic",
        "delete from prolics",
        "delete from cadlotelic",
        "delete from cadlic_sessao",
        "delete from cadlic",
        "delete from membros",
        "delete from comissao",
        "delete from icadorc",
        "delete from cadorc",
        "delete from icadped",
        "delete from fcadped",
        "delete from cadped",
        "delete from icadreq",
        "delete from requi",
        "delete from cadlote",
        "delete from cadest",
        "delete from cadsubgr",
        "delete from cadgrupo",
        "delete from centrocusto",
        "delete from destino",
        "delete from cadunimedida"
    ]

    for cmd in tabelas:
        conexao_destino.execute(cmd)

    conexao.commit()

def empresa():
    return (conexao_destino.execute("SELECT EMPRESA FROM TABEMPRESA t WHERE TIPO = 1"))

def exercicio():
    return int(conexao_destino.execute("SELECT mexer FROM CADCLI c"))

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