import conexao
import ferramentas

origem = conexao.cursor_origem
destino = conexao.cursor_destino
empresa = ferramentas.empresa()

# CONVERTENDO GRUPOS
def grupos():
    print("Convertendo Grupos")

    ferramentas.cria_campo("cadgrupo","conv_tipo")
    ferramentas.cria_campo("cadgrupo","conv_nro")

    insert = destino.prep("""insert into cadgrupo
                                (grupo, nome, balco_tce,
                                ocultar)
                            values (?,?,
                                    ?,?)""")

    origem.execute("""select distinct
	    substring(codigo, 1, 3) as grupo,
	    c.descricao
    from
	    catalogo c
    where
	    codigo like '___.00000.0000'""")

    for row in origem:
        grupo = row.grupo
        nome = row.descricao[:45]
        balco_tce = None
        ocultar = 'N'

        destino.execute(insert,(grupo, nome, balco_tce, ocultar))
    
    conexao.commit()

def subgrupos():
    print("Convertendo Subgrupos")

    insert = destino.prep("""insert into cadsubgr
                                (grupo, subgrupo, nome, ocultar, codant) 
                            values (?,?,?,
                                      ?,?)""")

    origem.execute("""select distinct
	    substring(codigo, 1, 3) as grupo,
	    c.descricao, codigo
    from
	    catalogo c
    where
	    codigo like '___.00000.0000'""")

    for row in origem:
        grupo = row.grupo
        subgrupo = "000"
        nome = row.descricao[:45]
        ocultar = 'N'
        codant = row.codigo

        destino.execute(insert,(grupo, subgrupo, nome, ocultar, codant))
    
    conexao.commit()

def unidade_medida():
    print("Convertendo Unidades de Medida")

    insert = destino.prep("""insert into
            cadunimedida(sigla,
            descricao,
            sigla_bbm)
        values (?,?,?)""")

    origem.execute("""select
	    cod_unidade,
	    descricao
    from
	    unidade u""")

    for row in origem:
        sigla = row.cod_unidade
        descricao = row.descricao[:45]
        sigla_bbm = sigla

        destino.execute(insert,(sigla, descricao, sigla_bbm))
        
    
    conexao.commit()

def produtos():
    print("Inserindo Produtos")

    insert = destino.prep("""INSERT INTO CADEST 
                (CADPRO,
                GRUPO,
                SUBGRUPO,
                CODIGO,
                DISC1,
                QUANMIN,
                QUANMAX,
                UNID1)
            VALUES (?,?,?,
                    ?,?,?,
                    ?,?)""")

    insert_subgp = destino.prep("""insert into cadsubgr
                                  (grupo, subgrupo, nome, ocultar, codant) values (?,?,?,?,?)""")

    origem.execute("""select record_number, catalogo, descricao, estoque_minimo, estoque_maximo, 
                      case when trim(unidade) = '' then null else unidade end as unidade, plano, status from material order by catalogo""")

    ultimo_sgp = 0

    lista_sgp = destino.execute("""select subgrupo, nome, grupo, codant from cadsubgr c """).fetchallmap()

    cod = 0
    grupo_anterior = '0'
    grupo_original = '0'

    for row in origem:
        grupo_original = row.catalogo[:3] 

        if grupo_anterior == grupo_original:
            cod += 1
        else:
            grupo_anterior = grupo_original
            cod = 1
            ultimo_sgp = 0

        if (cod % 1000) == 0:
            cod = 1
            ultimo_sgp += 1
            nome = next(x['nome'] for x in lista_sgp if x['grupo'] == row.catalogo[:3])
            ocultar = 'N'
            codant = next(x['codant'] for x in lista_sgp if x['grupo'] == row.catalogo[:3])

            destino.execute(insert_subgp,(row.catalogo[:3], str(ultimo_sgp).zfill(3), nome, ocultar, codant))

       
        grupo = row.catalogo[:3]
        subgrupo = str(ultimo_sgp).zfill(3)
        codigo = str(cod).zfill(3)
        cadpro = grupo + "." + subgrupo + "." + codigo
        disc1 = row.descricao[:45]
        quanmin = row.estoque_minimo
        quanmax = row.estoque_maximo
        unid1 = row.unidade

        destino.execute(insert,(cadpro, grupo, subgrupo, codigo, disc1, quanmin, quanmax, unid1))

    conexao.commit()

def almoxarifado():
    print("Convertendo Destino")

    insert = destino.prep("""INSERT INTO DESTINO 
                            (COD,
	                         DESTI,
	                         EMPRESA)
                            VALUES (?,?,?)""")

    origem.execute("""select cod_alm, descricao, responsavel  from almoxari""")

    for row in origem:
        cod = str(row.cod_alm).zfill(9)
        desti = str(row.descricao).strip()
        empresa = "1"

        destino.execute(insert,(cod, desti, empresa))     
    
    conexao.commit()

def centrocusto():
    print("Inserindo centro de custo")

    insert = conexao.cursor_destino.prep("""INSERT INTO CENTROCUSTO 
                             (poder,
	                          orgao,
	                          destino,
	                          ccusto,
	                          descr,
	                          codccusto,
	                          empresa,
	                          ocultar)
                            VALUES (?,?,?,?,?,
                                    ?,?,?)""")

    insert_cconversao = conexao.cursor_destino.prep("""INSERT INTO DESTINO 
                            (COD,
	                         DESTI,
	                         EMPRESA)
                            VALUES (?,?,?)""")

    origem.execute("""select DISTINCT r.cod_alm ,
	                        case when trim(r.DESTINO) = '' then null else r.DESTINO end as destino, 
	                        case when trim(r.ORGAO) = '' then null else r.ORGAO end as orgao ,
	                        d.DESCRICAO as descricao 
                      from
	                        requisic r
                      left join destino d on
	                        r.DESTINO = d.CODIGO 
                      order by COD_ALM """)

    i = 0
    flag = 0

    for row in origem:
        i += 1
        poder = row.orgao[:2] if row.orgao != None else '01'
        orgao = row.orgao[3:5] if row.orgao != None else '01'

        if str(row.cod_alm) == "     " and flag == 0:
            cod = "0".zfill(9)
            desti = "CONVERSAO"
            empresa = "1"
            flag = 1

            conexao.cursor_destino.execute(insert_cconversao,(cod, desti, empresa))     

        destino = "000000000" if str(row.cod_alm) == "     " else str(row.cod_alm).zfill(9)
        ccusto = str(i) if i < 1000 else "001" 
        descr = str(row.descricao).strip()
        codccusto = i 
        empresa = "1"
        ocultar = 'N'

        conexao.cursor_destino.execute(insert,(poder, orgao, destino, ccusto, descr, codccusto, empresa, ocultar))

    conexao.commit()






