import conexao
import manutencao

destino = conexao.get_cursor()
origem = conexao.conexao_origem.cursor()

empresa = destino.execute("SELECT EMPRESA FROM CADCLI").fetchone()[0]

def cria_campos():
    print("Criando campos")
    manutencao.cria_campo("desfor","modulo")
    manutencao.cria_campo("desfor","id")
    manutencao.cria_campo("pt_cadpat","codant")
    manutencao.cria_campo("pt_cadpatd","codant")
    manutencao.cria_campo("pt_cadpatd","codant_1")
    manutencao.cria_campo("pt_cadpatd","codant_2")
    manutencao.cria_campo("pt_cadpats","codant")
    manutencao.cria_campo("pt_cadpats","codant_1")
    manutencao.cria_campo("pt_cadpats","codant_2")
    manutencao.cria_campo("pt_cadpats","codant_3")

    conexao.commit()

def trigger(bool):
    print("Desligando triggers")
    
    triggers = [
        "UPDATE RDB$TRIGGERS SET RDB$TRIGGER_INACTIVE = %d WHERE RDB$TRIGGER_NAME = 'TD_PT_MOVBEM_GEN'" % bool,
        "UPDATE RDB$TRIGGERS SET RDB$TRIGGER_INACTIVE = %d WHERE RDB$TRIGGER_NAME = 'TBD_PT_MOVBEM_BLOQUEIO'" % bool,
        "UPDATE RDB$TRIGGERS SET RDB$TRIGGER_INACTIVE = %d WHERE RDB$TRIGGER_NAME = 'TD_PT_CADPAT_GEN'" % bool,
    ]


    for trigger in triggers:
        destino.execute(trigger)
    
    conexao.commit()

def limpa_tabelas():
    print("Limpando Tabelas")

    comandos = [
        "UPDATE VEICULO SET CODIGO_BEM_PAR = NULL",
        "UPDATE CADCLI SET BLOQUEIOP = NULL",
        "DELETE FROM PT_CADPAT_EMPEN",
        "DELETE FROM PT_MOVBEM",
        "DELETE FROM PT_CADPAT",
        "DELETE FROM PT_CADPATS",
        "DELETE FROM PT_CADPATD",
        "DELETE FROM PT_CADPATG",
        "DELETE FROM PT_CADSIT",
        "DELETE FROM PT_CADAJUSTE",
        "DELETE FROM PT_CADTIP",
        "DELETE FROM PT_CADBAI",
        "DELETE FROM PT_TIPOMOV"
    ]

    for comando in comandos:
        destino.execute(comando)

    conexao.commit()