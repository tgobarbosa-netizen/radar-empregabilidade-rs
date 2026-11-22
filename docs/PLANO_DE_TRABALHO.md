# Plano de Trabalho & Arquitetura por Sprints — Radar de Empregabilidade RS

* **Disciplina:** Inteligência Artificial
* **Composição da Equipe (5 Integrantes):** 
  * 2 alunos do **3º Semestre de Ciência de Dados e IA**
  * 2 alunos do **5º Semestre de Análise e Desenvolvimento de Sistemas (ADS)**
  * 1 vaga aberta (5º integrante a formalizar no encontro presencial de quarta-feira, 25/11)
* **Alinhamento Estratégico:** ODS 8 — Trabalho Decente e Crescimento Econômico (Meta 8.6)
* **Ambiente em Produção (MVP):** [https://radar-empregabilidade-rs.streamlit.app](https://radar-empregabilidade-rs.streamlit.app)
* **Meta Interna de Conclusão:** 09/12/2026 (1 semana de margem antes da entrega oficial em 16/12/2026)

---

## 1. Divisão Técnica por Perfil e Maturidade Acadêmica

A organização do projeto explora a complementaridade direta entre a base analítica/estatística (3º sem. Ciência de Dados e IA) e a maturidade de engenharia de software e arquitetura de sistemas (5º sem. ADS):

| Frente de Atuação | Perfil & Semestre | Escopo Técnico e Responsabilidades |
| :--- | :--- | :--- |
| **1. Engenharia de Dados & ETL (Novo CAGED)** | **Ciência de Dados e IA (3º Sem.)** | Extração, sanitização e agregação dos microdados dos últimos 12 meses do Novo CAGED (RS); tratamento de *outliers* salariais, agrupamento de subgrupos CBO e exportação em formato colunar otimizado (`.parquet`) em `/data`. |
| **2. Modelagem Preditiva & Avaliação Estatística** | **Ciência de Dados e IA (3º Sem.)** | Engenharia de *features*, treinamento e validação cruzada de modelos supervisionados (`LightGBM` / `Scikit-Learn`) para classificação multiclasse (Top 5 CBOs) e regressão salarial; serialização dos artefatos (`.joblib`) em `/models` e extração de métricas (F1-Score, Acurácia Top-K e MAE). |
| **3. Arquitetura Backend, APIs & CI/CD** | **ADS (5º Sem.)** | Manutenção da arquitetura modular (`src/inference.py`), gerenciamento de *branches*/PRs no GitHub, pipeline de deploy contínuo no Streamlit Cloud, integração da **Gemini API** (com *fallback* resiliente) e carregamento otimizado (`@st.cache_resource`) dos modelos `.joblib`. |
| **4. Front-end, UX & Visualização Analítica** | **ADS (5º Sem.)** | Evolução da interface em **Streamlit** (`app.py`), visualização interativa em **Plotly**, lógica do **Radar Reverso**, implementação funcional do **Modo Neutro** (mitigação de viés) e responsividade. |
| **5. Domínio de Negócio (CBO/ODS 8), QA & Pitch** | **5º Integrante (A definir na Quarta, 25/11)** | Construção da tabela de domínio (códigos CBO $\rightarrow$ nomenclatura amigável), validação de regras de negócio da ODS 8, execução de roteiro de testes de estresse (QA) e estruturação da apresentação executiva (6 slides). |

---

## 2. Roadmap de Execução (Sprints 1 a 4)

| Sprint | Período | Status / Objetivo | Entregáveis Técnicos |
| :--- | :--- | :--- | :--- |
| **Sprint 1** | **Até 25/11 (Quarta)** | ✅ **Concluída** (Setup, Arquitetura & MVP em Produção) | Repositório GitHub estruturado, deploy contínuo ativo no Streamlit Cloud, contrato de interface desacoplado (`app.py` $\leftrightarrow$ `src/inference.py`), indicador de média móvel salarial (3m) e tradução prática para o estudante. *(Marco presencial de quarta-feira: validação do desenho com o grupo e entrada do 5º integrante).* |
| **Sprint 2** | **26/11 a 30/11** (5 dias) | 🔄 **Próxima** (Pipeline ETL & Base Real do Novo CAGED RS) | **Dados (3º sem.):** Script/notebook de ETL processando os últimos 12 meses do RS, calculando o *Índice de Aquecimento* e a *Média Móvel Salarial (3m)* e gerando `/data/radar_agregado_rs.parquet` e `/data/dataset_treino_rs.parquet`.<br>**ADS (5º sem.) + 5º Integrante:** Dicionário oficial CBO e conexão da **Aba 2 (Radar Reverso)** aos dados reais. |
| **Sprint 3** | **01/12 a 05/12** (5 dias) | ⏳ **Planejada** (Treinamento ML, Serialização & Gemini API) | **Dados (3º sem.):** Treinamento e validação do Classificador (Top 5 CBOs) e Regressor Salarial, exportando `.joblib` para `/models`.<br>**ADS (5º sem.):** Substituição do *mock* em `src/inference.py` pela inferência real dos modelos `.joblib` e ativação da **Gemini API** via *Secrets* do Streamlit Cloud. |
| **Sprint 4** | **06/12 a 09/12** (4 dias) | ⏳ **Planejada** (Viés Algorítmico, QA & Defesa Técnica) | **ADS + Dados:** Validação do **"Modo Neutro"** (inferência sem variável de gênero para mitigar viés histórico) e auditoria de performance/cache.<br>**5º Integrante + Equipe:** Bateria de 10 cenários extremos (QA), atualização do `README.md` com métricas finais (F1-Score/MAE) e finalização dos 6 slides do Pitch. |
| **Margem & Banca** | **10/12 a 16/12** | 🏁 **Revisão Final e Apresentação ao Vivo** | Ensaio de 5 minutos dividindo a fala técnica entre Engenharia de Dados, Modelagem ML e Arquitetura de Software para a entrega oficial em **16/12/2026**. |

---

## 3. Pauta do Encontro Presencial (Quarta-feira, 25/11)

1. **Demonstração do MVP no Ar:** Validar juntos a interface publicada (`radar-empregabilidade-rs.streamlit.app`) e fechar o escopo definitivo.
2. **Onboarding da Equipe:** Formalizar o 5º integrante na Frente 5, adicionar todos como colaboradores no GitHub e validar o ambiente local (`git clone` + `streamlit run app.py`).
3. **Alinhamento de Contrato de Dados:** Confirmar os nomes exatos das colunas do `.parquet` que a equipe de Dados (3º sem.) vai entregar até **30/11** para que o pessoal de ADS (5º sem.) já deixe a leitura pronta no código.

---

## 4. Checklist Final (Definition of Done)
* [x] Repositório GitHub modularizado e aplicação hospedada em nuvem fora de notebooks.
* [ ] Pipeline ETL reproduzível processando microdados reais do Novo CAGED (RS).
* [ ] Modelos supervisionados (Classificação + Regressão) serializados (`.joblib`) com métricas documentadas.
* [ ] IA Generativa (`Gemini API`) operando em tempo real com *fallback* seguro.
* [ ] Modo Neutro validado e apresentação final ensaiada pelos 5 integrantes.