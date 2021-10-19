import conexao
import base

destino = conexao.get_cursor()

def converte_bens():
    print("Convertendo bens Patrimoniais")
  
    destino.execute("DELETE FROM PT_MOVBEM")
    destino.execute("DELETE FROM PT_CADPAT")


    sql = """
    SELECT
        P.NRO,
        P.NRO_PATR,
        P.NOME,
        P.DESCRICAO,
        P.FLG_INCORP,
        P.FLG_MODAL,
        P.AQUIS_DATA,
        P.AQUIS_VALOR,
        P.AQUIS_NRO_DOC,
        P.ESTCON_NRO,
        P.LEI,
        P.OBS,
        P.BX_DOC_ESPECIE,
        P.BX_DOC_NUMERO,
        P.BX_DOC_DATA,
        P.BX_NRO_PROC,
        P.BX_MOTIVO,
        P.BX_VALOR,
        P.FLG_MODAL_BX,
        P.FO_PES_NRO,
        P.BPESP_NRO,
        P.FLG_BEM_TERC,
        P.NRO_EMPENHO,
        P.DT_EMPENHO,
        P.DT_VIDA_UTIL,
        P.DT_GARANTIA,
        P1.DEPSEC_NRO,
        COALESCE(COALESCE(P3.VLR_BASE_CALC, P2.VLR_BASE_CALC),0) AS VLR_BASE_CALC,
	    COALESCE(COALESCE(P3.VLR_RESIDUAL, P2.VLR_RESIDUAL),0) AS VLR_RESIDUAL,
        E.PLCTRZ_CDCONT_NRO
    FROM
        SYSTEM.D3_BEM_PATR P
    LEFT JOIN SYSTEM.D3_BP_DS P1 ON
        P1.BEPA_NRO = P.NRO
    LEFT JOIN SYSTEM.D3_BP_VALOR P2 ON
        P2.BEPA_NRO = P.NRO
        AND (COALESCE(P2.FLG_REAVALIADO, 'N') = 'N')
    LEFT JOIN SYSTEM.D3_BP_VALOR P3 ON
        P3.BEPA_NRO = P.NRO
        AND (COALESCE(P3.FLG_REAVALIADO, 'N') = 'S')
    LEFT JOIN SYSTEM.D3_BP_ESPECIE E ON
        E.NRO = P.BPESP_NRO
    WHERE
        (COALESCE(P1.FLG_ADQTRANSF, 'A') = 'A')
    """

    insert= destino.prep("""INSERT
	    INTO
            PT_CADPAT (
            CODIGO_PAT,
            EMPRESA_PAT,
            CODIGO_GRU_PAT,
            CODIGO_SET_PAT,
            CODIGO_SET_ATU_PAT,
            CHAPA_PAT,
            NOTA_PAT,
            ORIG_PAT,
            CODIGO_FOR_PAT,
            CODIGO_TIP_PAT,
            CODIGO_SIT_PAT,
            DISCR_PAT,
            DATAE_PAT,
            DTLAN_PAT,
            DT_CONTABIL,
            VALAQU_PAT,
            VALDES_PAT,
            VALATU_PAT,
            QUAN_PAT,
            VALRES_PAT,
            PERCENTEMP_PAT,
            PERCENQTD_PAT,
            DAE_PAT,
            CODANT,
            OBS_PAT)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""")

    

    tipo_origem = {1:"C", 3:"O", 4:"D", 8:"S", 9:"P", 13:"F"}

    for row in conexao.get(sql):
        codigo_pat= row["nro"]
        empresa_pat= base.empresa
        codigo_gru_pat= 1
        codigo_set_pat= row["depsec_nro"]
        codigo_set_atu_pat= row["depsec_nro"]
        chapa_pat= str(row['nro_patr']).zfill(6) 
        nota_pat= str(row["aquis_nro_doc"]).zfill(10)
        orig_pat= "D" if row["flg_modal"] == "3" else "C"
        codigo_for_pat= row["fo_pes_nro"]
        codigo_tip_pat= row["bpesp_nro"]
        codigo_sit_pat= row["estcon_nro"]
        discr_pat= row["nome"]
        datae_pat= row["aquis_data"]
        dtlan_pat= row["aquis_data"]
        dt_contabil= row["aquis_data"]
        valaqu_pat= row["aquis_valor"]
        valdes_pat= 0
        valatu_pat= row["vlr_base_calc"]
        quan_pat= 1
        valres_pat= row["vlr_residual"]
        percentemp_pat= None 
        percenqtd_pat= None
        dae_pat= None
        codant= row["nro"]
        obs_pat = row["descricao"]

            

        destino.execute(insert, (codigo_pat,empresa_pat,codigo_gru_pat,codigo_set_pat,codigo_set_atu_pat,chapa_pat,
                                nota_pat,orig_pat,codigo_for_pat,codigo_tip_pat,codigo_sit_pat,discr_pat,datae_pat,
                                dtlan_pat,dt_contabil,valaqu_pat,valdes_pat,valatu_pat,quan_pat,valres_pat,percentemp_pat,
                                percenqtd_pat,dae_pat,codant, obs_pat))
   
    conexao.commit()

def mov_aquisicao():
    print("Convertendo Movimentação Bens Patrimoniais [AQUISIÇÃO]")

    bens_convertidos = destino.execute("""
        SELECT
            P.CODIGO_PAT,
            P.DISCR_PAT,
            P.DATAE_PAT,
            P.CODIGO_CPL_PAT,
            P.CODIGO_SET_PAT,
            P.VALAQU_PAT,
            P.BALCO_PAT
        FROM
	        PT_CADPAT P
        ORDER BY
	        P.CODIGO_PAT""").fetchallmap()
    
    insert = destino.prep("""
        INSERT INTO
            PT_MOVBEM (EMPRESA_MOV,
            CODIGO_MOV,
            CODIGO_PAT_MOV,
            DATA_MOV,
            DT_CONTABIL,
            TIPO_MOV,
            CODIGO_CPL_MOV,
            BALCO_MOV,
            CODIGO_SET_MOV,
            VALOR_MOV,
            DOCUMENTO_MOV,
            HISTORICO_MOV) 
        VALUES 
            (?,?,?,?,
            ?,?,?,?,
            ?,?,?,?)""")

    i = 0

    for row in bens_convertidos:
        i += 1
        empresa_mov= base.empresa
        codigo_mov= i
        codigo_pat_mov= row["codigo_pat"]
        data_mov= row["datae_pat"]
        dt_contabil= row["datae_pat"]
        tipo_mov= "A"
        codigo_cpl_mov= row["codigo_cpl_pat"]
        balco_mov= row["balco_pat"]
        codigo_set_mov= row["codigo_set_pat"]
        valor_mov= row["valaqu_pat"]
        documento_mov= "CONVERSÃO"
        historico_mov= "AQUISIÇÃO DE BEM PATRIMONIAL"

        destino.execute(insert,(empresa_mov,codigo_mov,codigo_pat_mov,data_mov,dt_contabil,tipo_mov,codigo_cpl_mov,
                                balco_mov,codigo_set_mov,valor_mov,documento_mov,historico_mov))

    conexao.commit()

def transferencias():
    print("Convertendo Movimentação Bens Patrimoniais [TRANSFERENCIA]")

    destino.execute("DELETE FROM PT_MOVBEM where TIPO_MOV= 'T'")

    sql= """
    SELECT P1.BEPA_NRO, P1.TR_DOC_DATA, P1.TR_DOC_ESPECIE, P1.TR_DOC_NUMERO, P1.DEPSEC_NRO 
     FROM SYSTEM.D3_BP_DS P1 
     WHERE P1.FLG_ADQTRANSF ='T' 
     ORDER BY P1.BEPA_NRO, P1.TR_DOC_DATA, P1.DEPSEC_NRO

    """
    
    insert = destino.prep("""
    INSERT INTO
        PT_MOVBEM (CODIGO_MOV,
        EMPRESA_MOV,
        CODIGO_PAT_MOV,
        DATA_MOV,
        TIPO_MOV,
        CODIGO_SET_MOV,
        HISTORICO_MOV,
        VALOR_MOV)
    VALUES (?,?,?,
            ?,?,?,
            ?,?)
    """)

    i= int(destino.execute("SELECT max(codigo_mov) FROM PT_MOVBEM pm ").fetchone()[0])

    for row in conexao.get(sql):
        i += 1
        codigo_mov= i
        empresa_mov= base.empresa
        codigo_pat_mov= row["bepa_nro"]
        data_mov= row["tr_doc_data"]
        tipo_mov= "T"
        codigo_set_mov= row["depsec_nro"]
        historico_mov= row["tr_doc_numero"]
        valor_mov= 0

        destino.execute(insert,(codigo_mov, empresa_mov, codigo_pat_mov, data_mov, tipo_mov, codigo_set_mov, historico_mov, valor_mov))

    conexao.commit()

def mov_baixas():
    print("Lançando Movimentação de Baixas")

    sql = """
    SELECT P.NRO,  
        P.BX_DOC_ESPECIE, P.BX_DOC_NUMERO, P.BX_DOC_DATA, P.BX_NRO_PROC, P.BX_MOTIVO, P.BX_VALOR, P.FLG_MODAL_BX 
        FROM SYSTEM.D3_BEM_PATR P  
        WHERE (P.BX_DOC_DATA IS NOT NULL)
    """

    insert = destino.prep("""
    INSERT INTO PT_MOVBEM (CODIGO_MOV, EMPRESA_MOV, HISTORICO_MOV, CODIGO_BAI_MOV, TIPO_MOV, CODIGO_PAT_MOV, DATA_MOV, VALOR_MOV) VALUES (?,?,?,?,?,?,?,?)
    """)

    update = destino.prep("""
    UPDATE PT_CADPAT SET DTPAG_PAT= ?, CODIGO_BAI_PAT = ? WHERE CODIGO_PAT = ? 
    """)

    listagem_valores = destino.execute("SELECT CODIGO_PAT, VALAQU_PAT, VALATU_PAT FROM PT_CADPAT pc ").fetchallmap()

    listagem_baixas = destino.execute("""SELECT DESCRICAO_BAI , codigo_bai FROM PT_CADBAI pc """).fetchallmap()

    i= int(destino.execute("SELECT max(codigo_mov) FROM PT_MOVBEM pm ").fetchone()[0])

    for row in conexao.get(sql):
        i += 1
        codigo_mov= i
        empresa_mov= base.empresa
        historico_mov= row["bx_motivo"]
        codigo_bai_mov= next((x["CODIGO_BAI"] for x in listagem_baixas if x["DESCRICAO_BAI"] == row["bx_motivo"]), 2)
        tipo_mov= "B"
        codigo_pat_mov= row["nro"]
        data_mov= row["bx_doc_data"]

        localiza_valor= next(x for x in listagem_valores if x["CODIGO_PAT"] == row["nro"])

        valor_mov= (localiza_valor["VALATU_PAT"] * -1) if localiza_valor["VALATU_PAT"] > 0.0 else (localiza_valor["VALAQU_PAT"] * -1)


        destino.execute(insert,(codigo_mov,empresa_mov,historico_mov,codigo_bai_mov,tipo_mov,codigo_pat_mov,data_mov,valor_mov))
        destino.execute(update,(data_mov,codigo_bai_mov,codigo_pat_mov))
    conexao.commit()

def depreciacoes():
    sql = """
    SELECT  d.BPVLR_BEPA_NRO, d.VALOR, d.PORCENT, TO_DATE(ano || '-' || mes || '-' || '1','YYYY-MM-DD') AS BPVLR_DATA_AVAL,
	(SELECT DEPSEC_NRO  FROM SYSTEM.D3_BP_DS P1 WHERE P1.BEPA_NRO = d.BPVLR_BEPA_NRO 
	ORDER  BY DATA_INICIO DESC fetch first 1 row only) AS DEPSEC_NRO 
	FROM SYSTEM.D3_DEPR_CORR d
    """

    insert = destino.prep("""
    INSERT INTO
        PT_MOVBEM (CODIGO_MOV,
        EMPRESA_MOV,
        CODIGO_PAT_MOV,
        DATA_MOV,
        TIPO_MOV,
        CODIGO_CPL_MOV,
        CODIGO_SET_MOV,
        VALOR_MOV,
        HISTORICO_MOV,
        LOTE_MOV,
        PERCENTUAL_MOV, 
        DEPRECIACAO_MOV)
    VALUES (?,?,?,?,
            ?,?,?,?,
            ?,?,?,?)
    """)

    i= int(destino.execute("SELECT max(codigo_mov) FROM PT_MOVBEM pm ").fetchone()[0])

    for row in conexao.get(sql):
        i += 1
        codigo_mov = i
        empresa_mov = base.empresa
        codigo_pat_mov = row["bpvlr_bepa_nro"]
        data_mov = row["bpvlr_data_aval"]
        tipo_mov = "R"
        codigo_cpl_mov ="123810101"
        codigo_set_mov = row["depsec_nro"]
        valor_mov = (row["valor"]) * -1
        historico_mov = "DEPRECIAÇÃO"
        lote_mov = 0
        percentual_mov = row["porcent"]
        depreciacao_mov = "S"

        destino.execute(insert, (codigo_mov, empresa_mov, codigo_pat_mov, data_mov, tipo_mov, codigo_cpl_mov, codigo_set_mov, valor_mov, historico_mov, lote_mov, percentual_mov, depreciacao_mov))

    conexao.commit()

        