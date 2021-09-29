import conexao

destino = conexao.get_cursor()

def cria_campo(nome_tabela, nome_campo):
    resultado = destino.execute(   
        "select count(*) from rdb$relation_fields where rdb$relation_name = '{tabela}' and(rdb$field_name = '{campo}')".format(tabela=nome_tabela.upper(), campo=nome_campo.upper())).fetchone()[0]

    if(resultado == 1): return

    destino.execute("alter table {tabela} add {campo} varchar(20)".format(
            tabela=nome_tabela, campo=nome_campo))

    conexao.commit()
    

