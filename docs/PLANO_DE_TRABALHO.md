---

### 2. `docs/PLANO_DE_TRABALHO.md`

```markdown
# Método de Trabalho e Plano de Sprints (20/11 a 09/12)

Para garantir que o sistema esteja 100% pronto e validado no dia **09/12** (uma semana antes do prazo limite de 16/12), o fluxo de trabalho é dividido em **3 Sprints Curtas**, usando os dias de aula presencial (**25/11**, **02/12** e **09/12**) como marcos obrigatórios de integração e validação.

## 1. Regras de Organização do Time (Fluxo Ágil)
* **Repositório Único (GitHub):** Estrutura padronizada (`/data`, `/notebooks`, `/models`, `/src`, `/docs`, `app.py`, `requirements.txt`).
* **Contrato de Interface (Desenvolvimento Paralelo):** Front-end e Modelagem não se bloqueiam. As funções `prever_perfil(dados_usuario)` e `buscar_demanda_reversa(area_cbo)` possuem entradas e saídas padronizadas antes mesmo do modelo final estar treinado.
* **Rituais Rápidos:** Check-in assíncrono de 5 minutos às sextas-feiras e alinhamento presencial nos dias de aula.

---

## 2. Cronograma por Sprints e Marcos de Aula

### Sprint 1: Dados, Baseline e Esqueleto Visual (20/11 a 25/11)
*Foco: Limpar os dados do Novo CAGED (RS) e ter um protótipo navegável.*
* **Engenharia de Dados:** Baixar os últimos 12 meses do Novo CAGED (RS), filtrar colunas relevantes (`município`, `idade`, `sexo`, `grau_instrucao`, `cbo2002`, `saldomovimentacao`, `salario`), agrupar CBOs em Subgrupos (2–3 dígitos) e salvar `caged_rs_limpo.parquet`.
* **Ciência de Dados:** Análise exploratória rápida e criação da feature sintética **Índice de Aquecimento** (para a aba de engenharia reversa).
* **Front-end (Streamlit):** Criar a estrutura com as 2 abas (*Modo Estudante* e *Radar Reverso de Demanda*) usando dados fictícios (mock) para validar layout e filtros.
* **Requisitos/Docs:** Subir o `README.md` inicial no GitHub com a especificação de requisitos e ODS 8.
* **Marco na Aula de 25/11:** Apresentar ao professor a arquitetura fechada, os requisitos e a base limpa; alinhar dúvidas técnicas com o time em sala.

### Sprint 2: Modelagem Preditiva e Integração Ponta a Ponta (26/11 a 02/12)
*Foco: Substituir dados fictícios pelos modelos reais treinados e conectar a LLM.*
* **Ciência de Dados:** Treinar o classificador (Top 5 CBOs prováveis) e o regressor salarial (`LightGBM` ou `RandomForest`), avaliar métricas (F1-Score / MAE) e exportar os arquivos `.joblib` para a pasta `/models`.
* **Backend & IA Generativa:** Implementar o script `inference.py` que carrega os modelos `.joblib`, conecta com a API do Gemini para gerar a trilha de habilidades e implementa o dicionário de *fallback* offline.
* **Front-end (Streamlit):** Conectar os botões e filtros da interface diretamente às funções reais do `inference.py` e renderizar os gráficos comparativos com `Plotly`.
* **Marco na Aula de 02/12:** Sistema rodando **ponta a ponta** localmente no notebook do grupo. Validar interface e justificativa da ODS com o professor.

### Sprint 3: Refino, Deploy em Nuvem e Ensaio do Pitch (03/12 a 09/12)
*Foco: Estabilidade, mitigação de viés, deploy público e preparação da apresentação.*
* **Engenharia & Front-end:** Subir a aplicação no **Streamlit Community Cloud** e validar o botão de "Modo Neutro" (sem filtro de gênero) para atender ao RNF03.
* **Todos os Integrantes (QA):** Testar pelo menos 10 cenários extremos (cidades do interior vs. capital, ensino técnico vs. pós-graduação) para garantir estabilidade ao vivo.
* **Documentação & Pitch:** Atualizar o `README.md` com prints da tela funcionando, métricas finais do modelo e link do deploy. Montar apresentação de 6 slides.
* **Marco na Aula de 09/12:** **Sistema 100% concluído** e pronto para apresentação antecipada ou revisão final.

---

## 3. Checklist de Controle (Definition of Done)
* [ ] Justificativa clara ligando o problema à **ODS 8 (Meta 8.6)** e explicando por que usar IA.
* [ ] Interface funcional rodando fora de notebooks (Streamlit online/local).
* [ ] Fluxo completo funcionando: entrada do usuário -> processamento da IA -> resultado na tela.
* [ ] Repositório no GitHub público com código limpo, `requirements.txt` e `README.md` completo.
* [ ] Todos os integrantes dominando a parte que vão explicar e demonstrar ao vivo.