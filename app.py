import streamlit as st
import pandas as pd
import plotly.express as px
from src.inference import prever_perfil, buscar_demanda_reversa

st.set_page_config(
    page_title="Radar de Empregabilidade RS | ODS 8",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Radar de Empregabilidade & Demanda Ocupacional (RS)")
st.markdown(
    "Sistema de apoio à decisão profissional baseado em microdados do **Novo CAGED** "
    "alinhado à **ODS 8 (Meta 8.6 — Trabalho Decente e Inserção Jovem)**."
)

tab1, tab2, tab3 = st.tabs([
    "🎓 Modo Estudante (Inferência de Perfil)",
    "🧭 Radar Reverso (Demanda por Região)",
    "📋 Sobre o Projeto & ODS 8",
])

# ==========================================
# ABA 1: INFERÊNCIA DE PERFIL DO ESTUDANTE
# ==========================================
with tab1:
    st.subheader("Simule suas probabilidades de absorção no mercado gaúcho")
    col_form, col_res = st.columns([1, 2], gap="large")

    with col_form:
        with st.form("form_perfil"):
            municipio = st.selectbox(
                "Município (RS)",
                ["Porto Alegre", "Caxias do Sul", "Canoas", "Pelotas", "Santa Maria", "Novo Hamburgo", "Passo Fundo"],
            )
            idade = st.slider("Idade", min_value=16, max_value=65, value=23)
            sexo = st.selectbox("Sexo", ["Feminino", "Masculino"])
            escolaridade = st.selectbox(
                "Grau de Instrução",
                [
                    "Médio Completo",
                    "Técnico / Pós-Médio",
                    "Superior Incompleto",
                    "Superior Completo",
                    "Pós-Graduação",
                ],
            )
            area_interesse = st.selectbox(
                "Grande Área de Interesse (CBO)",
                [
                    "Tecnologia e Dados",
                    "Administração e Negócios",
                    "Engenharia e Indústria",
                    "Saúde e Ciências Biológicas",
                    "Comércio e Serviços",
                ],
            )
            modo_neutro = st.checkbox(
                "Ativar Modo Neutro (ignorar filtro de sexo para mitigar viés histórico)",
                value=False,
            )
            submitted = st.form_submit_button("Analisar Oportunidades", use_container_width=True)

    with col_res:
        if submitted:
            payload = {
                "municipio": municipio,
                "idade": idade,
                "sexo": None if modo_neutro else sexo,
                "escolaridade": escolaridade,
                "area_interesse": area_interesse,
                "modo_neutro": modo_neutro,
            }
            resultado = prever_perfil(payload)
            df_top = pd.DataFrame(resultado["top_ocupacoes"])

            st.success(f"Análise concluída para **{municipio}** ({escolaridade}).")

            # Destaque da Ocupação Principal (Nome completo + Código CBO)
            top1 = df_top.iloc[0]
            tendencia = top1["tendencia_salario_pct"]
            sinal = "+" if tendencia > 0 else ""

            st.markdown(
                f"""
                <div style="background-color: #1E2530; padding: 14px 18px; border-radius: 8px; border-left: 4px solid #00C896; margin-bottom: 14px;">
                    <span style="font-size: 13px; color: #9BA3AF; text-transform: uppercase; letter-spacing: 0.5px;">Ocupação Mais Provável (CBO {top1['cbo_codigo']})</span><br>
                    <span style="font-size: 20px; font-weight: 700; color: #FFFFFF;">{top1['ocupacao']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Métricas de destaque com Tendência Salarial (Média Móvel 3m)
            m1, m2, m3 = st.columns(3)
            m1.metric(
                label="Afinidade com o Perfil",
                value=f"{top1['probabilidade']*100:.0f}%",
                delta=f"CBO {top1['cbo_codigo']}",
                delta_color="off",
                help=f"Classificação Brasileira de Ocupações (Subgrupo {top1['cbo_codigo']}): {top1['ocupacao']}",
            )
            m2.metric(
                label="Salário Estimado de Entrada",
                value=f"R$ {top1['salario_estimado']:,.2f}",
                delta=f"{sinal}{tendencia:.1f}% (média móvel 3m)",
                help="Variação percentual do salário médio de admissão nos últimos 3 meses em relação ao trimestre anterior.",
            )
            m3.metric(
                label="Saldo de Vagas (12m)",
                value=f"+{top1['saldo_vagas_12m']} vagas",
                delta="Expansão líquida",
            )

            # Gráfico de barras das Top 5 ocupações
            fig = px.bar(
                df_top,
                x="probabilidade",
                y="ocupacao",
                orientation="h",
                text=df_top["probabilidade"].apply(lambda x: f"{x*100:.0f}%"),
                title="Top 5 Ocupações (CBO) Inferidas pelo Modelo",
                labels={"probabilidade": "Probabilidade Estimada", "ocupacao": "Ocupação (CBO)"},
            )
            fig.update_layout(yaxis=dict(autorange="reversed"), height=320)
            st.plotly_chart(fig, use_container_width=True)

            # Bloco de Tradução Prática para a vida do estudante
            maior_volume = df_top.sort_values(by="saldo_vagas_12m", ascending=False).iloc[0]
            with st.expander("💡 O que esses números significam na prática para você?", expanded=True):
                st.markdown(
                    f"- **Alvo Principal:** Seu perfil tem maior afinidade técnica com **{top1['ocupacao']}** (CBO {top1['cbo_codigo']}).\n"
                    f"- **Porta de Entrada Rápida:** Se precisar de absorção imediata em **{municipio}**, a ocupação correlata com maior volume de contratações abertas é **{maior_volume['ocupacao']}** (+{maior_volume['saldo_vagas_12m']} vagas no último ano).\n"
                    f"- **Termômetro de Remuneração:** Use a faixa de **R$ {top1['salario_estimado']:,.2f}** como referência realista para pretensão salarial inicial na região."
                )

            # Trilha gerada por IA
            st.info(resultado["trilha_recomendada"])
        else:
            st.info("👈 Preencha seu perfil ao lado e clique em **Analisar Oportunidades** para rodar a inferência.")

# ==========================================
# ABA 2: ENGENHARIA REVERSA DE DEMANDA
# ==========================================
with tab2:
    st.subheader("Radar Reverso: Onde há maior escassez e absorção de profissionais?")
    st.caption(
        "O Índice de Aquecimento cruza o saldo líquido de admissões com a variação real do salário "
        "de entrada nos últimos 12 meses para identificar polos regionais com alta demanda."
    )

    area_radar = st.selectbox(
        "Selecione a Área Profissional para rastrear demanda no RS:",
        [
            "Tecnologia e Dados",
            "Administração e Negócios",
            "Engenharia e Indústria",
            "Saúde e Ciências Biológicas",
            "Logística e Transporte",
        ],
    )

    df_radar = pd.DataFrame(buscar_demanda_reversa(area_radar))

    # Mapa Geográfico Interativo do RS
    fig_mapa = px.scatter_mapbox(
        df_radar,
        lat="lat",
        lon="lon",
        size="saldo_liquido",
        color="indice_aquecimento",
        hover_name="municipio",
        hover_data={
            "lat": False,
            "lon": False,
            "saldo_liquido": True,
            "variacao_salarial_pct": True,
            "indice_aquecimento": True,
        },
        color_continuous_scale="Viridis",
        size_max=32,
        zoom=5.6,
        center={"lat": -30.2, "lon": -53.0},
        mapbox_style="carto-darkmatter",
        title=f"Mapa de Calor Ocupacional (RS) — {area_radar}",
        labels={
            "saldo_liquido": "Saldo de Vagas (12m)",
            "variacao_salarial_pct": "Alta Salarial (%)",
            "indice_aquecimento": "Índice de Aquecimento",
        },
    )
    fig_mapa.update_layout(height=420, margin={"r": 0, "t": 40, "l": 0, "b": 0})
    st.plotly_chart(fig_mapa, use_container_width=True)

    c1, c2 = st.columns([3, 2])
    with c1:
        fig_radar = px.bar(
            df_radar,
            x="municipio",
            y="indice_aquecimento",
            color="variacao_salarial_pct",
            text="indice_aquecimento",
            title=f"Ranking de Aquecimento Municipal — {area_radar}",
            labels={
                "municipio": "Município (RS)",
                "indice_aquecimento": "Índice de Aquecimento (0-100)",
                "variacao_salarial_pct": "Alta Salarial (%)",
            },
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with c2:
        st.markdown("**Detalhamento dos Indicadores (12 meses)**")
        cols_exibir = ["municipio", "saldo_liquido", "variacao_salarial_pct", "indice_aquecimento"]
        st.dataframe(df_radar[cols_exibir], use_container_width=True, hide_index=True)

# ==========================================
# ABA 3: DOCUMENTAÇÃO E ODS 8
# ==========================================
with tab3:
    st.markdown("""
    ### Justificativa e Alinhamento com a ODS 8
    * **Objetivo:** ODS 8 — Trabalho Decente e Crescimento Econômico (Meta 8.6).
    * **Fonte de Dados:** Microdados do Novo CAGED (Ministério do Trabalho e Emprego) — recorte Rio Grande do Sul.
    * **Arquitetura de IA:** Pipeline híbrido combinando modelos supervisionados (`LightGBM` / `Scikit-Learn`) para classificação ocupacional e regressão salarial com IA Generativa (`Gemini API`) para orientação de carreira.
    """)