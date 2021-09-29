import conexao
import base

destino = conexao.get_cursor()

def tipos_mov():
    print("Inserindo tipos de movimentação")

    insert = destino.prep("INSERT INTO PT_TIPOMOV (CODIGO_TMV, DESCRICAO_TMV) VALUES (?, ?)")

    valores = [
        ("A", "AQUISIÇÃO"),
        ("B", "BAIXA"),
        ("T", "TRANSFERÊNCIA"),
        ("R", "PR. CONTÁBIL"),
        ("P", "TRANS. PLANO")
        ]

    destino.executemany(insert, valores)

    conexao.commit()

def tipos_ajuste():
    print ("Inserindo Tipos de Ajuste")

    insert = destino.prep("INSERT INTO PT_CADAJUSTE (CODIGO_AJU, EMPRESA_AJU, DESCRICAO_AJU) VALUES (?, ?, ?)")

    valores = [(1, base.empresa, "REAVALIAÇÃO(ANTES DO CORTE)")]

    destino.executemany(insert, valores)

    conexao.commit()

def baixas():
    print ("Inserindo Baixas")

    insert = destino.prep("INSERT INTO PT_CADBAI (CODIGO_BAI, EMPRESA_BAI, DESCRICAO_BAI) VALUES (?, ?, ?)")

    sql = """
    SELECT
	    DISTINCT P.BX_MOTIVO 
    FROM
	    SYSTEM.D3_BEM_PATR P 
    WHERE
	    (P.BX_MOTIVO IS NOT NULL)
    ORDER BY
	    P.BX_MOTIVO"""

    i= 0

    for row in conexao.get(sql):
        i += 1
        codigo_bai = i
        empresa_bai = base.empresa
        descricao_bai = row["bx_motivo"]

        destino.execute(insert, (codigo_bai,empresa_bai, descricao_bai))

        conexao.commit()

def tipos_bens():
    print ("Inserindo tipos de bens")

    insert = destino.prep("INSERT INTO PT_CADTIP(CODIGO_TIP, EMPRESA_TIP, DESCRICAO_TIP) VALUES (?, ?, ?)")

    sql = """
    SELECT
	    E.NRO,
	    E.NOME
    FROM
    	SYSTEM.D3_BP_ESPECIE E
    ORDER BY
    	E.NRO"""

    for row in conexao.get(sql):
        codigo_tip = row["nro"]
        descricao_tip = row["nome"]

        destino.execute(insert,(codigo_tip,base.empresa,descricao_tip))
    
    conexao.commit()

def situacao():
    print("Convertendo situação")

    insert = destino.prep("INSERT INTO PT_CADSIT (CODIGO_SIT, EMPRESA_SIT, DESCRICAO_SIT) VALUES (?, ?, ?)")

    sql = """
    SELECT
	    C.NRO,
	    C.NOME
    FROM
	    SYSTEM.D3_EST_CONSERV C
    ORDER BY
	    C.NRO
    """

    for row in conexao.get(sql):
        codigo_sit = row["nro"]
        descricao_sit = row["nome"]

        destino.execute(insert,(codigo_sit,base.empresa,descricao_sit))

    conexao.commit()

def converte_grupos():
    print ("Convertendo grupos")
    
    insert = destino.prep("""INSERT INTO PT_CADPATG (CODIGO_GRU,EMPRESA_GRU,NOGRU_GRU) VALUES (?,?,?)""")

    codigo_gru = 1
    nogru_gru = "Geral"

    destino.execute(insert, (codigo_gru,base.empresa,nogru_gru))

    conexao.commit()

def converte_unidades():
    print ("Convertendo Unidades")

    insert = destino.prep("INSERT INTO PT_CADPATD (EMPRESA_DES, CODIGO_DES, NAUNI_DES, OCULTAR_DES, CODANT) VALUES (?, ?, ?, ?, ?)")

    sql = """
    SELECT
        DS.NRO,
        DS.NOME,
        DS.FLG_DEPSEC,
        DS.FLG_ATIVO,
        DS.DEPSEC_NRO
    FROM
	    SYSTEM.DEPTO_SECAO DS
    WHERE
	    DS.DEPSEC_NRO IS NULL
    ORDER BY
	    DS.NRO
    """
    i= 0

    for row in conexao.get(sql):
        i += 1
        empresa_des = base.empresa
        codigo_des = i
        nauni_des = row["nome"]
        ocultar_des = "N"
        codant = row["nro"]

        if row["flg_ativo"] == "N":
            ocultar_des = "S"

        destino.execute(insert,(empresa_des,codigo_des,nauni_des,ocultar_des,codant))
    
    conexao.commit()

def converte_subunidades():
    print("Convertendo Sub-Unidades")

    insert = destino.prep("INSERT INTO PT_CADPATS (EMPRESA_SET, CODIGO_SET, CODIGO_DES_SET, NOSET_SET) VALUES (?, ?, ?, ?)")

    sql = """
    SELECT
        DS.NRO,
        DS.NOME,
        DS.FLG_DEPSEC,
        DS.FLG_ATIVO,
        CAST(DS.DEPSEC_NRO AS int) AS COD
    FROM
	    SYSTEM.DEPTO_SECAO DS
    WHERE
	    DS.DEPSEC_NRO IS NOT NULL
    ORDER BY
	    DS.NRO
    """

    lista_codant = destino.execute("""
    SELECT
	    CODIGO_DES, CAST(CODANT AS INTEGER) AS CODANT 
    FROM
	    PT_CADPATD
    """).fetchallmap()


    for row in conexao.get(sql):
        empresa_set = base.empresa
        codigo_set = row["nro"]
        codigo_des_set = next(x['codigo_des'] for x in lista_codant if x["codant"] == row["cod"])
        noset_set = row["nome"]

        destino.execute(insert,(empresa_set,codigo_set,codigo_des_set,noset_set))

    conexao.commit()



     
