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

            top1 = df_top.iloc[0]
            m1, m2, m3 = st.columns(3)
            m1.metric("Ocupação Mais Provável", f"CBO {top1['cbo_codigo']}", f"{top1['probabilidade']*100:.0f}% de afinidade")
            m2.metric("Salário Estimado de Entrada", f"R$ {top1['salario_estimado']:,.2f}")
            m3.metric("Saldo de Vagas (12m)", f"+{top1['saldo_vagas_12m']} vagas")

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
            st.info(resultado["trilha_recomendada"])
        else:
            st.info("👈 Preencha seu perfil ao lado e clique em **Analisar Oportunidades** para rodar a inferência.")

with tab2:
    st.subheader("Radar Reverso: Onde há maior escassez e absorção de profissionais?")
    st.caption(
        "O Índice de Aquecimento cruza o saldo líquido de admissões com a variação real do salário "
        "de entrada nos últimos 12 meses para identificar mercados com alta demanda."
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
        st.dataframe(df_radar, use_container_width=True, hide_index=True)

with tab3:
    st.markdown("""
    ### Justificativa e Alinhamento com a ODS 8
    * **Objetivo:** ODS 8 — Trabalho Decente e Crescimento Econômico (Meta 8.6).
    * **Fonte de Dados:** Microdados do Novo CAGED (Ministério do Trabalho e Emprego) — recorte Rio Grande do Sul.
    * **Arquitetura de IA:** Pipeline híbrido combinando modelos supervisionados (`LightGBM` / `Scikit-Learn`) para classificação ocupacional e regressão salarial com IA Generativa (`Gemini API`) para orientação de carreira.
    """)