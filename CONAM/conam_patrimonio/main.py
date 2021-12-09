import conexao
import cadastros
import ferramentas
import bens

cursor_origem = conexao.conexao_origem.cursor()
cursor_destino = conexao.conexao_destino.cursor()

def main():
    # LIMPAR TABELAS
    # ferramentas.limpa_tabelas()

    # INSERINDO DADOS
    # cadastros.tipos_mov()
    # cadastros.tipos_ajuste()
    # cadastros.baixas()
    # cadastros.tipos_bens()
    # cadastros.situacao()
    # cadastros.converte_grupos()
    # cadastros.converte_responsaveis()
    # cadastros.converte_unidades()
    # cadastros.converte_subunidades()

    # # INSERINDO BENS
    bens.converte_bens()
    bens.movimentacao()


    ferramentas.triggers("liga")


if __name__ == "__main__":
    main()

