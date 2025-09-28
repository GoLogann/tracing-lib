# 📊 tracing-lib

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Poetry](https://img.shields.io/badge/poetry-dependency%20management-blue.svg)
![Langfuse](https://img.shields.io/badge/langfuse-observability-green.svg)

> Uma biblioteca wrapper para o [Langfuse](https://langfuse.com/) focada em **observabilidade para aplicações de LLM**, centralizando tracing, métricas de performance e feedback de usuários.

-----

## 🚀 Instalação

A biblioteca pode ser adicionada ao seu projeto via Poetry.

### Opção 1 — Via Repositório Git (Recomendado)

Para instalar diretamente do GitHub, execute:

```bash
poetry add git+https://github.com/GoLogann/tracing-lib.git
```

Para fixar uma versão ou tag específica (ex: `v0.1.0`):

```bash
poetry add git+https://github.com/GoLogann/tracing-lib.git#v0.1.0
```

### Opção 2 — Via Diretório Local (Para Desenvolvimento)

Se você clonou o repositório para sua máquina local, pode instalá-lo da seguinte forma:

```bash
# O caminho deve ser relativo ao diretório do seu projeto
poetry add ../tracing-lib
```

## ⚙️ Configuração

Para inicializar o serviço de tracing, você pode definir as seguintes variáveis de ambiente (em um arquivo `.env`, por exemplo):

- `LANGFUSE_HOST`
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`

Ou, se preferir, pode instanciar as configurações via Pydantic e passar para o serviço:

```python
from tracing_lib.config import TracerSettings
from tracing_lib.tracer_service import TracerService

# Inicialização via Pydantic
settings = TracerSettings(
    LANGFUSE_HOST="https://cloud.langfuse.com",
    LANGFUSE_PUBLIC_KEY="pk-xxx",
    LANGFUSE_SECRET_KEY="sk-xxx",
)

tracer = TracerService(settings)
```

## 🛠️ Como Usar

### 1. Criando Traces e Gerações (Context Manager)

O `TracerService` utiliza gerenciadores de contexto (`with`) para garantir que os traces e observações sejam corretamente abertos e fechados.

```python
# Inicia um trace principal para uma requisição
with tracer.start_trace(name="bedrock-generate", metadata={"model": "claude-3-sonnet"}) as trace:
    
    # Dentro do trace, inicia uma "geração" (chamada de LLM)
    with tracer.start_generation(
        name="qa-generate",
        model="claude-3-sonnet",
        input="Pergunta: Qual o número do processo?"
    ) as gen:
        
        # Simula a chamada real ao seu modelo
        answer = "0801234-56.2023.8.01.0001"
        
        # Atualiza a geração com o resultado
        gen.update(output=answer)

    # Adiciona um score customizado ao trace principal
    tracer.add_score(trace=trace, name="groundedness", value=1, comment="Resposta baseada em corpus")
```

### 2. Usando Decorators

Para instrumentar funções inteiras de forma simples, utilize o decorator `@tracer.observe`:

```python
@tracer.observe(as_type="retriever", name="get-graph-facts")
def fetch_facts_from_database(pasta_id: str):
    # Lógica para buscar dados no banco
    # O decorator irá capturar automaticamente o input, output e a duração.
    return {"docs_found": 50}

# Ao chamar a função, um span será criado no Langfuse
fetch_facts_from_database(pasta_id="12345")
```

## 📊 Métricas Coletadas

Ao usar esta biblioteca, você terá acesso imediato no dashboard do Langfuse a:

- **Traces**: Requisições completas (ex: uma chamada de API `ask` ou `extract`).
- **Observations**: Chamadas internas detalhadas (ex: `retriever`, `generation`, `embedding`).
- **Scores**: Métricas de qualidade customizadas (ex: `latência`, `groundedness`, `validade de JSON`).
- **Custos e Uso**: Tokens de entrada/saída e custos inferidos pelo Langfuse.

-----

## 👨‍💻 Autor

**Logan Cardoso**  
*AI/ML Engineer • AWS • LangChain • LangGraph • Python*

📧 **Email:** logan.cc@outlook.com  
💼 **LinkedIn:** [logan-cardoso](https://www.linkedin.com/in/logan-cardoso/)  
🌐 **GitHub:** [GoLogann](https://github.com/GoLogann)

## 📜 Licença

MIT License

Copyright (c) 2024 Logan Cardoso

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.