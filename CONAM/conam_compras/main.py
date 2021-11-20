import conexao
import cadastros
import ferramentas

cursor_origem = conexao.conexao_origem.cursor()
cursor_destino = conexao.conexao_destino.cursor()

def main():
    # LIMPANDO TABELAS
    ferramentas.limpa_tabelas()

    # CRIANDO CAMPOS
    ferramentas.cria_campo("CADSUBGR","CODANT")
    ferramentas.cria_campo("CENTROCUSTO","CODANT1")
    ferramentas.cria_campo("CENTROCUSTO","CODANT2")
    ferramentas.cria_campo("DESFOR","MODULO")
    ferramentas.cria_campo("DESFOR","ID")
    ferramentas.cria_campo("CADEST","CODANT")
    ferramentas.cria_campo("REQUI","REQUI_ANT")
    ferramentas.cria_campo("REQUI","REQUI_ANT1")
    ferramentas.cria_campo("REQUI","REQUI_ANT2")
    ferramentas.cria_campo("REQUI","REQUI_ANT3")
    ferramentas.cria_campo("CADLICITACAO","CODANT1")
    ferramentas.cria_campo("CADLICITACAO","CODANT2")
    ferramentas.cria_campo("CADLIC","CODANT1")
    ferramentas.cria_campo("CADLIC","CODANT2")
    ferramentas.cria_campo("CADPED","CODANT1")
    ferramentas.cria_campo("CADPED","CODANT2")

    cadastros.grupos()
    cadastros.subgrupos()
    cadastros.unidade_medida()
    cadastros.produtos()
    cadastros.almoxarifado()
    cadastros.centrocusto()

    ferramentas.triggers("liga")
    

if __name__ == "__main__":
    main()