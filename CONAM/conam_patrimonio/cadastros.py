import conexao
import ferramentas

cur_fb = conexao.get_cursor_fb()
cur_ms = conexao.get_cursor_ms()
empresa = ferramentas.empresa()

def tipos_mov():
    print('Inserindo tipos de movimentação')
    
    insert = cur_fb.prep("insert into pt_tipomov (codigo_tmv, descricao_tmv) values (?, ?)")

    valores = [
        ("A", "AQUISIÇÃO"),
        ("B", "BAIXA"),
        ("T", "TRANSFERÊNCIA"),
        ("R", "PR. CONTÁBIL"),
        ("P", "TRANS. PLANO")
    ]

    cur_fb.executemany(insert, valores)

    conexao.commit()

def tipos_ajuste():
    print ("Inserindo Tipos de Ajuste")

    insert = cur_fb.prep("insert into pt_cadajuste (codigo_aju, empresa_aju, descricao_aju) values (?, ?, ?)")

    valores = [(1, 1, "REAVALIAÇÃO(ANTES DO CORTE)")]

    cur_fb.executemany(insert, valores)

    conexao.commit()

def baixas():
    print ("Inserindo Baixas")

    insert = cur_fb.prep("insert into pt_cadbai (codigo_bai, empresa_bai, descricao_bai) values (?, ?, ?)")

    cur_ms.execute("SELECT  codigo, descricao from baixas b");

    for row in cur_ms:        
        codigo_bai = row.codigo
        empresa_bai = empresa
        descricao_bai = row.descricao.strip()

        cur_fb.execute(insert, (codigo_bai, empresa_bai, descricao_bai))

    conexao.commit()

def tipos_bens():
    print("Inserindo Tipos de Bens")

    insert = cur_fb.prep("insert into pt_cadtip(codigo_tip, empresa_tip, descricao_tip) values (?, ?, ?)")

    cur_ms.execute("SELECT codigo_conta , desc_conta  FROM contdepr c")

    for row in cur_ms:        
        codigo_tip = row.codigo_conta
        empresa_tip = empresa
        descricao_tip = row.desc_conta.strip()

        cur_fb.execute(insert, (codigo_tip, empresa_tip, descricao_tip))
        
    conexao.commit()

def situacao():
    print("Convertendo Situações")

    insert = cur_fb.prep("INSERT INTO PT_CADSIT (CODIGO_SIT, EMPRESA_SIT, DESCRICAO_SIT) VALUES (?, ?, ?)")

    cur_fb.execute(insert, (1, 1, "BOM"))

    conexao.commit()

def converte_grupos():
    print ("Convertendo grupos")
    
    insert = cur_fb.prep("""insert into pt_cadpatg (codigo_gru,empresa_gru,nogru_gru) values (?,?,?)""")

    codigo_gru = 1
    nogru_gru = "Movéis"

    cur_fb.execute(insert, (codigo_gru,1,nogru_gru))

    codigo_gru = 2
    nogru_gru = "Imovéis"

    cur_fb.execute(insert, (codigo_gru,1,nogru_gru))

    conexao.commit()

def converte_responsaveis():
    print ("Convertendo responsaveis")

    insert = cur_fb.prep("""insert into pt_cadresponsavel(codigo_resp, nome_resp) values(?,?)""")

    cur_ms.execute("select cod_resp,descricao from responsa r")

    for row in cur_ms:
        codigo_resp = row.cod_resp
        nome_resp = row.descricao.strip()

        cur_fb.execute(insert, (codigo_resp, nome_resp))

    conexao.commit()

def converte_unidades():
    print ("Convertendo unidades")

    insert = cur_fb.prep("""INSERT INTO pt_cadpatd(empresa_des,
	                                                codigo_des,
                                                    nauni_des,
                                                    ocultar_des)
                             VALUES (?,?,?,?)""")

    empresa_des = empresa
    codigo_des = 1
    nauni_des = cur_fb.execute("select clnt1 from cadcli").fetchone()[0]
    ocultar_des = "N"
    
    cur_fb.execute(insert, (empresa_des, codigo_des, nauni_des, ocultar_des))

    conexao.commit()

def converte_subunidades():
    print("Convertendo Sub-Unidades")

    insert = cur_fb.prep("insert into pt_cadpats (empresa_set, codigo_set, codigo_des_set, noset_set, responsa_set, codigo_resp_set) values (?, ?, ?, ?, ?, ?)")

    cur_ms.execute(
        """
        select
            s.cod_setor ,
            s.descricao ,
            r.descricao as responsavel,
            r.cod_resp 
        from
            setor s
        left join responsa r on
            r.cod_resp = s.cod_resp
        """)

    for row in cur_ms:
        empresa_set = empresa
        codigo_set = row.cod_setor
        codigo_des_set = 1
        noset_set = row.descricao.strip()
        responsa_set = row.responsavel.strip() if row.responsavel is not None else None
        codigo_resp_set = row.cod_resp 

        cur_fb.execute(insert,(empresa_set, codigo_set, codigo_des_set, noset_set, responsa_set, codigo_resp_set))
    
    conexao.commit()