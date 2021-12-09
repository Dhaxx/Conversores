import conexao
import ferramentas

cur_ms = conexao.get_cursor_ms()
destino = conexao.get_cursor_fb()
empresa = ferramentas.empresa()

def converte_bens():
    print("Convertendo bens Patrimoniais")
  
    destino.execute("DELETE FROM PT_MOVBEM")
    destino.execute("DELETE FROM PT_CADPAT")
    destino.execute("update cadcli set bloqueiop = null")

    ferramentas.cria_campo("PT_CADPAT","CODANT1")
    ferramentas.cria_campo("PT_CADPAT","CODANT2")

    cur_ms.execute(
        """
        select
            1 as grupo ,
            n_bem,
            'M' as tipobem,
            n_chapa,
            cod_setor,
            n_docfiscal,
            n_fornecedor,
            descricao,
            data_aquisic,
            data_incorpora,
            vl_incorporacao,
            vl_atual,
            null as escritura,
            null as area,
            replace(conta_plano, '.', '') as conta,
            coalesce(n_empenho,'') as n_empenho,
            coalesce(ano_empenho,'') as ano_empenho ,
            cod_resp ,
            c.codigo_conta as tipo
        from
            moveis m
        left join contdepr c on
            c.conta = m.conta_plano
        union
                                    select
            2
                                    ,
            n_bem,
            'I' as tipobem,
            null,
            null,
            '0000000000',
            null,
            descricao,
            data_aquisicao,
            data_incorpora,
            vl_incorporacao,
            vl_atual,
            escritura,
            area,
            replace(conta_plano, '.', '') as conta,
            '',
            '',
            cod_resp ,
            c.codigo_conta
        from
            imoveis i
        left join contdepr c on
            c.conta = i.conta_plano
        where
            n_bem <> ''
        order by
            tipobem asc
        """)

    insert = """insert into pt_cadpat (codigo_pat,
                    empresa_pat,
                    codigo_gru_pat,
                    chapa_pat,
                    codigo_set_pat,
                    codigo_set_atu_pat,
                    nota_pat,
                    orig_pat,
                    codigo_for_pat,
                    codigo_tip_pat,
                    codigo_sit_pat,
                    discr_pat,
                    datae_pat,
                    dtlan_pat,
                    codigo_bai_pat,
                    valaqu_pat,
                    valatu_pat,
                    quan_pat,
                    valres_pat,
                    dt_contabil,
                    codant1,
                    codant2,
                    escr_pat,
                    areatot_pat,
                    codigo_cpl_pat,
                    codigo_resp_pat , 
                    nempg_pat , 
                    anoemp_pat)
                values(?,?,?,?,?,?,
                       ?,?,?,?,?,?,
                       ?,?,?,?,?,?,
                       ?,?,?,?,?,?,
                       ?,?,?,?)"""

    codigo_pat = 0
    sequencia_imoveis = 0

    for row in cur_ms:
        codigo_pat += 1
        empresa_pat = empresa
        codigo_gru_pat = row.grupo

        if row.grupo == 1:
            chapa_pat = row.n_chapa[-6:]
        else:
            sequencia_imoveis += 1
            chapa_pat = str(sequencia_imoveis).zfill(6)

        codigo_set_pat = row.cod_setor
        codigo_set_atu_pat = codigo_set_pat
        nota_pat = row.n_docfiscal
        orig_pat = 'C'
        codigo_for_pat = None if row.n_fornecedor == "00000" else row.n_fornecedor
        codigo_tip_pat = row.tipo
        codigo_sit_pat = 1
        discr_pat = row.descricao.strip()
        datae_pat = row.data_aquisic
        dtlan_pat = row.data_incorpora
        codigo_bai_pat = None
        valaqu_pat = row.vl_incorporacao
        valatu_pat = row.vl_atual
        quan_pat = 1
        valres_pat = 0
        dt_contabil = dtlan_pat
        codant1 = row.tipobem
        codant2 = row.n_bem
        escr_pat = row.escritura
        areatot_pat = row.area
        codigo_cpl_pat = row.conta[:9]
        codigo_resp_pat = row.cod_resp
        nempg_pat = row.n_empenho if row.n_empenho.strip() != '' else None
        anoemp_pat=  row.ano_empenho if row.ano_empenho.strip() != '' else None

        destino.execute(insert,(codigo_pat,empresa_pat,codigo_gru_pat,chapa_pat,codigo_set_pat,
                                codigo_set_atu_pat,nota_pat,orig_pat,codigo_for_pat,codigo_tip_pat,
                                codigo_sit_pat,discr_pat,datae_pat,dtlan_pat,codigo_bai_pat,
                                valaqu_pat,valatu_pat,quan_pat,valres_pat,dt_contabil,codant1,
                                codant2,escr_pat,areatot_pat, codigo_cpl_pat, codigo_resp_pat , nempg_pat , anoemp_pat))
    conexao.commit()  

def movimentacao():
    print("Lançando Movimentação de Baixas")

    insert = destino.prep("""insert into pt_movbem(codigo_mov,
                                    empresa_mov,
                                    codigo_pat_mov,
                                    data_mov,
                                    codigo_set_mov,
                                    valor_mov,
                                    documento_mov,
                                    historico_mov,
                                    percentual_mov,
                                    dt_contabil,
                                    tipo_mov,
                                    codigo_cpl_mov)
                                values (?,?,?,?,
                                        ?,?,?,?,
                                        ?,?,?,?)""")

    sql = """select i.n_bem,
                    case
                        m.tipo_documento when 'AD' then 'A'
                        when 'AI' then 'A'
                        when 'AV' then 'R'
                        WHEN 'BX' then 'B'
                    END as tipo_mov,
                    i.descricao,
                    m.data,
                    m.cod_setor,
                    case
                        m.tipo_documento when 'BX' then m.vl_movimento * -1
                        else m.vl_movimento 
                    end as valor,
                    m.n_documento,
                    'I' as tipobem,
                    replace(m.conta_plano, '.', '') as conta,
                    m.tipo_bx 
                from
                    imoveis i
                inner join moviment m on
                    (i.n_bem = m.n_bem)
                    and m.conta_plano like '1.2.3.2%'
                    where m.status <> 'P'
                UNION 
                select
                    mv.n_bem,
                    case
                        m.tipo_documento
                    when 'AV' then 'R'
                        when 'GT' then 'T'
                        when 'DO' then 'T'
                        when 'BX' then 'B'
                        when 'DT' then 'T'
                        when 'AM' then 'A'
                    end as tipo_mov,
                        mv.descricao,
                        m.[DATA],
                        m.cod_setor,
                    case 
                        m.tipo_documento 
                    when 'DO' then m.vl_movimento * 0
                        when 'BX' then m.vl_movimento * -1
                        when 'DT' then m.vl_movimento * 0
                        else m.vl_movimento
                    end as valor,
                        m.n_documento,
                        'M' as tipobem,
                        replace(m.conta_plano, '.', '') as conta,
                        m.tipo_bx 
                from
                    moveis mv
                inner join moviment m on
                    (mv.n_bem = m.n_bem)
                    and m.conta_plano like '1.2.3.1%'
                    where m.status <> 'P'
                ORDER by
                    tipobem"""

                
    cur_ms.execute(sql)

    update_baixa = destino.prep("""update pt_cadpat set dtpag_pat= ?, codigo_bai_pat = ?, codigo_cpl_pat = ? where codigo_pat = ? """)

    lista_bens = destino.execute("select codigo_pat, chapa_pat, valaqu_pat, valatu_pat, codant1, codant2 from pt_cadpat pc ").fetchallmap()

    codigo_mov = 0

    for row in cur_ms:        
        codigo_mov += 1
        empresa_mov = empresa
        codigo_pat_mov = next((x['codigo_pat'] for x in lista_bens if x['codant2'] == row.n_bem and x['codant1'] == row.tipobem), None)
        data_mov = row.data
        codigo_set_mov = row.cod_setor if row.cod_setor != '     ' else None
        valor_mov = row.valor
        documento_mov = row.n_documento.strip()
        historico_mov = row.descricao.strip()
        codigo_bai_mov = row.tipo_bx  if row.tipo_mov == 'B' else None
        percentual_mov = 0
        dt_contabil = data_mov
        tipo_mov = row.tipo_mov
        codigo_cpl_mov = row.conta[:9]

        destino.execute(insert,(codigo_mov, empresa_mov, codigo_pat_mov, data_mov, codigo_set_mov, valor_mov, documento_mov, 
                                historico_mov, percentual_mov, dt_contabil, tipo_mov, codigo_cpl_mov))
        if tipo_mov == 'B':
            destino.execute(update_baixa,(data_mov,codigo_bai_mov,codigo_cpl_mov,codigo_pat_mov))

    conexao.commit()  
