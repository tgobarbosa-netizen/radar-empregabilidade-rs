# Radar de Empregabilidade & Demanda Ocupacional (RS)

Sistema inteligente de apoio à decisão profissional e análise de absorção do mercado de trabalho no Rio Grande do Sul, desenvolvido como Projeto Final da disciplina de Inteligência Artificial (3º Semestre — Ciência de Dados e IA).

## Integrantes do Grupo (Máx. 5)
* [Nome Completo 1] — Engenharia de Dados & ETL
* [Nome Completo 2] — Modelagem Preditiva (Machine Learning)
* [Nome Completo 3] — Integração IA Generativa & Backend
* [Nome Completo 4] — Front-end & UX (Streamlit)
* [Nome Completo 5] — Engenharia de Requisitos, Negócio (ODS) & Documentação

---

## 1. Alinhamento com os Objetivos de Desenvolvimento Sustentável (ODS)

### 1.1 ODS Escolhida e Meta Relacionada
* **ODS 8:** Trabalho Decente e Crescimento Econômico.
* **Meta 8.6:** Reduzir substancialmente a proporção de jovens sem emprego, educação ou formação, promovendo a inserção qualificada no mercado de trabalho.

### 1.2 O Problema e Público Afetado
Estudantes do ensino técnico, superior e jovens em busca de inserção ou recolocação profissional no Rio Grande do Sul enfrentam forte assimetria de informação: desconhecem quais ocupações realmente absorvem seu perfil demográfico e educacional, qual a remuneração realista de entrada e quais municípios apresentam demanda reprimida (escassez de mão de obra). Isso gera escolhas de carreira desalinhadas com o mercado regional e aumento do tempo de desocupação.

### 1.3 Como a Solução Enfrenta o Problema
A aplicação atua em duas frentes complementares:
1. **Inferência de Perfil (Modo Estudante):** Estima as ocupações (CBO) com maior probabilidade de contratação e faixa salarial esperada a partir do perfil do usuário.
2. **Engenharia Reversa de Demanda (Radar Regional):** Identifica municípios e áreas profissionais com alto Índice de Aquecimento (saldo líquido positivo de admissões + crescimento salarial), revelando onde há maior absorção de vagas.

### 1.4 Justificativa para o Uso de Inteligência Artificial
Consultas estáticas em planilhas governamentais mostram apenas médias passadas isoladas. O uso de **Machine Learning (Classificação e Regressão)** permite capturar interações não lineares entre múltiplas variáveis simultâneas (idade, sexo, grau de instrução, município e grande área CBO) para calcular probabilidades personalizadas de absorção. Adicionalmente, a integração com um **Modelo de Linguagem (LLM)** traduz os indicadores numéricos em planos de ação práticos de capacitação para o usuário final.

---

## 2. Especificação de Requisitos

### 2.1 Histórias de Usuário (User Stories)
* **US01 (Estudante):** *Como estudante ou candidato, quero informar minha idade, gênero, escolaridade, município e área de interesse para visualizar minhas Top 5 ocupações mais prováveis e a faixa salarial estimada.*
* **US02 (Análise Reversa):** *Como estudante ou orientador educacional, quero selecionar uma área de atuação (ou município) para descobrir quais cidades ou setores do RS estão com maior aquecimento de contratações e escassez relativa de profissionais.*
* **US03 (Plano de Ação):** *Como usuário do sistema, quero receber recomendações personalizadas de habilidades técnicas e comportamentais exigidas para a ocupação prevista.*

### 2.2 Requisitos Funcionais (RF)
* **RF01 — Parametrização de Perfil:** O sistema deve permitir a entrada estruturada de idade, sexo, nível de escolaridade, município (RS) e grande grupo ocupacional.
* **RF02 — Inferência Preditiva de Ocupação:** O pipeline de ML deve processar os parâmetros de entrada e retornar as 5 ocupações (Subgrupos CBO) com maior probabilidade de contratação.
* **RF03 — Estimativa Salarial:** O sistema deve calcular a faixa salarial esperada de admissão com base no perfil e na CBO inferida.
* **RF04 — Radar Reverso de Demanda:** O sistema deve calcular e ranquear o *Índice de Aquecimento Ocupacional* (baseado no saldo líquido de admissões e variação salarial) por município ou área.
* **RF05 — Recomendação Generativa:** O sistema deve enviar o resultado estruturado da inferência a uma API de LLM para gerar orientações de qualificação (com *fallback* local caso a API esteja indisponível).
* **RF06 — Visualização Comparativa:** A interface deve exibir gráficos interativos comparando o perfil consultado com a média histórica do estado.

### 2.3 Requisitos Não Funcionais (RNF)
* **RNF01 — Privacidade e LGPD:** Nenhum dado pessoal identificável (nome, CPF, e-mail) será coletado ou persistido em banco de dados; todo o processamento ocorre em sessão.
* **RNF02 — Desempenho:** O tempo total entre o envio do formulário e a exibição completa dos resultados (ML + gráficos + LLM) deve ser inferior a 4 segundos.
* **RNF03 — Mitigação de Viés Algorítmico:** Como bases históricas refletem desigualdades salariais de gênero, o sistema deve permitir visualizar a projeção tanto com o filtro demográfico quanto em modo neutro (apenas escolaridade e região), documentando essa limitação na interface.
* **RNF04 — Disponibilidade:** A aplicação deve estar hospedada em nuvem (Streamlit Community Cloud) e ser executável localmente via ambiente virtual Python.

---

## 3. Arquitetura e Tecnologias Utilizadas

* **Fonte de Dados:** Microdados do Novo CAGED (Ministério do Trabalho e Emprego — últimos 12 meses, recorte Rio Grande do Sul) + Tabela Oficial CBO.
* **ETL & Manipulação:** Python 3.11, `pandas`, `numpy`, `pyarrow` (armazenamento otimizado em `.parquet`).
* **Machine Learning:** `scikit-learn`, `lightgbm` (Classificação multiclasse para probabilidade de CBO e Regressão para salário de admissão), `joblib`.
* **IA Generativa:** API Google Gemini (com dicionário local de fallback).
* **Interface & Visualização:** `streamlit`, `plotly`.
* **Gestão de Sprints:** Consulte o plano completo em [`docs/PLANO_DE_TRABALHO.md`](docs/PLANO_DE_TRABALHO.md).

---

## 4. Como Executar o Projeto Localmente

```bash
# 1. Clonar o repositório
git clone [https://github.com/tgobarbosa-netizen/radar-empregabilidade-rs.git](https://github.com/tgobarbosa-netizen/radar-empregabilidade-rs.git)
cd radar-empregabilidade-rs

# 2. Criar e ativar ambiente virtual
python -m venv venv
venv\Scripts\activate     # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variável de ambiente da LLM (opcional, possui fallback)
set GEMINI_API_KEY="sua_chave_aqui"

# 5. Executar a aplicação
streamlit run app.py