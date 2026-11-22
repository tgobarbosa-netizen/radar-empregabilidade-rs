import os
from typing import Dict, List, Any


def prever_perfil(dados_usuario: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recebe os parâmetros do estudante e retorna as Top 5 ocupações (CBO),
    faixa salarial estimada, tendência da média móvel (3m) e recomendação de habilidades.
    """
    idade = dados_usuario.get("idade", 22)
    escolaridade = dados_usuario.get("escolaridade", "Superior Incompleto")
    municipio = dados_usuario.get("municipio", "Porto Alegre")
    modo_neutro = dados_usuario.get("modo_neutro", False)

    fator_escolaridade = 1.35 if "Completo" in escolaridade or "Pós" in escolaridade else 1.0
    salario_base = round(2400 * fator_escolaridade + (idade - 18) * 45, 2)

    ocupacoes_mock = [
        {
            "cbo_codigo": "2124",
            "ocupacao": "Analista de Desenvolvimento de Sistemas / Dados",
            "probabilidade": 0.42,
            "salario_estimado": round(salario_base * 1.25, 2),
            "tendencia_salario_pct": 6.4,
            "saldo_vagas_12m": 1420,
        },
        {
            "cbo_codigo": "3171",
            "ocupacao": "Técnico de Desenvolvimento de Sistemas e Aplicações",
            "probabilidade": 0.26,
            "salario_estimado": round(salario_base * 0.95, 2),
            "tendencia_salario_pct": 4.1,
            "saldo_vagas_12m": 890,
        },
        {
            "cbo_codigo": "2521",
            "ocupacao": "Analista de Planejamento e Gestão",
            "probabilidade": 0.15,
            "salario_estimado": round(salario_base * 1.10, 2),
            "tendencia_salario_pct": 2.8,
            "saldo_vagas_12m": 640,
        },
        {
            "cbo_codigo": "4110",
            "ocupacao": "Assistente Administrativo / Operações",
            "probabilidade": 0.11,
            "salario_estimado": round(salario_base * 0.78, 2),
            "tendencia_salario_pct": -1.2,
            "saldo_vagas_12m": 2150,
        },
        {
            "cbo_codigo": "3172",
            "ocupacao": "Técnico em Operação e Monitoramento de Computadores",
            "probabilidade": 0.06,
            "salario_estimado": round(salario_base * 0.85, 2),
            "tendencia_salario_pct": 1.9,
            "saldo_vagas_12m": 410,
        },
    ]

    recomendacao_llm = gerar_trilha_habilidades(
        ocupacao_principal=ocupacoes_mock[0]["ocupacao"],
        escolaridade=escolaridade,
        municipio=municipio,
    )

    return {
        "status": "mock_mvp",
        "modo_neutro_aplicado": modo_neutro,
        "top_ocupacoes": ocupacoes_mock,
        "trilha_recomendada": recomendacao_llm,
    }


def buscar_demanda_reversa(area_cbo: str, filtro_regiao: str = "Todo o RS") -> List[Dict[str, Any]]:
    """
    Engenharia reversa: identifica os municípios do RS com maior Índice de Aquecimento
    (saldo líquido de admissões + variação salarial positiva) e coordenadas geográficas.
    """
    return [
        {"municipio": "Porto Alegre", "lat": -30.0346, "lon": -51.2177, "saldo_liquido": 3450, "variacao_salarial_pct": 6.8, "indice_aquecimento": 94.2},
        {"municipio": "Caxias do Sul", "lat": -29.1678, "lon": -51.1794, "saldo_liquido": 1890, "variacao_salarial_pct": 7.4, "indice_aquecimento": 91.5},
        {"municipio": "Canoas", "lat": -29.9178, "lon": -51.1836, "saldo_liquido": 1120, "variacao_salarial_pct": 5.9, "indice_aquecimento": 86.0},
        {"municipio": "Novo Hamburgo", "lat": -29.6875, "lon": -51.1328, "saldo_liquido": 870, "variacao_salarial_pct": 6.1, "indice_aquecimento": 83.4},
        {"municipio": "Passo Fundo", "lat": -28.2628, "lon": -52.4067, "saldo_liquido": 740, "variacao_salarial_pct": 7.9, "indice_aquecimento": 82.1},
        {"municipio": "Pelotas", "lat": -31.7654, "lon": -52.3376, "saldo_liquido": 620, "variacao_salarial_pct": 5.2, "indice_aquecimento": 78.5},
        {"municipio": "Santa Maria", "lat": -29.6842, "lon": -53.8069, "saldo_liquido": 580, "variacao_salarial_pct": 5.5, "indice_aquecimento": 76.8},
    ]


def gerar_trilha_habilidades(ocupacao_principal: str, escolaridade: str, municipio: str) -> str:
    """
    Conecta com a API do Gemini (se configurada) ou aciona o fallback local.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = (
                f"Atue como um orientador de carreira focado no mercado do Rio Grande do Sul (ODS 8). "
                f"Para um candidato com escolaridade '{escolaridade}' em '{municipio}' mirando a ocupação "
                f"'{ocupacao_principal}', liste em 3 tópicos curtos: 1) Competências técnicas essenciais, "
                f"2) Ferramentas mais pedidas na região e 3) Um passo prático imediato."
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            return response.text
        except Exception:
            pass

    return (
        f"**Plano de Ação Sugerido para {ocupacao_principal} ({municipio}):**\n"
        "- **Competências Técnicas:** Domínio de SQL, análise exploratória em Python (Pandas) e lógica de indicadores de negócio.\n"
        "- **Ferramentas em Alta no RS:** Power BI, Excel Avançado, Git e bancos relacionais.\n"
        "- **Próximo Passo Prático:** Construir um portfólio no GitHub resolvendo um problema real com dados públicos locais."
    )