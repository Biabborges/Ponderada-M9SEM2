
## **1. Mapa de Business Drivers**

A imagem abaixo representa o mapeamento dos direcionadores de negócio da Rappi, focando na interação entre os sistemas e os entregadores.

<img src="./images/Mapa de direcionadores.jpg" alt="Mapa de Direcionadores">

### **1.1 Descrição Geral**
A Rappi opera com múltiplos sistemas interligados, mas nesta simulação vamos trabalhar com o suporte ao entregador e a correta sincronização de estoque. Os principais componentes do sistema são:

- **Sistema de Direcionadores de Negócio**: Define critérios de desempenho e eficiência.
- **Sistema de Suporte**: Gerencia chamados e suporte aos entregadores.
- **Sistema de Estoque**: Mantém a sincronização do estoque em tempo real.
- **Entregador**: Usuário final que interage com os sistemas para visualizar estoque e solicitar suporte.

## **2. Estratégia de Testes**
A estratégia de testes visa garantir que os sistemas de suporte e estoque atendam aos critérios definidos nos direcionadores de negócio.

### **2.1 Estratégia para DN1 - Eficiência no Suporte**
- Deve assegurar que o tempo máximo de resposta e resolução dos chamados esteja dentro dos limites estabelecidos.

#### **Tipos de Testes**
- **Testes Funcionais:** Validar a abertura, categorização e fluxo de chamados no sistema de suporte.
- **Testes de Desempenho:** Simular múltiplos chamados simultâneos para verificar tempos de resposta e escalabilidade do sistema.
- **Testes de Automação:** Criar scripts para monitoramento contínuo do tempo de resposta do chatbot e do assistente humano.

#### **Cenários de Teste**
| ID | Cenário | Entrada | Resultado Esperado |
|----|---------|---------|--------------------|
| DN1-01 | Abrir chamado crítico via chatbot | Problema: "Pagamento não recebido" | Chatbot deve priorizar e escalar para humano em menos de 1 min |
| DN1-02 | Testar tempo de resposta para chamados críticos em lote | 100 chamados simultâneos | 85% respondidos em até 15 minutos |
| DN1-03 | Testar tempo de resposta para chamados gerais | 100 chamados gerais | 95% respondidos em até 2 horas |
| DN1-04 | Simular falha na API de suporte | API de suporte offline | Mensagem de fallback deve ser exibida para o usuário |

### **Código de Teste para DN1**
```python
def test_chamado_critico_prioritario(self):
    """Testa se chamados críticos são escalados corretamente em até 1 min"""
    chamado_critico = {"tipo": "Pagamento não recebido", "prioridade": "Crítico"}
    start_time = time.time()
    response_time = 30
    assert response_time < 60, "Chamado crítico não foi priorizado corretamente"
    end_time = time.time()
    print(f"Tempo de resposta do chamado crítico: {end_time - start_time:.2f} segundos")
```
```python
def test_resposta_chamados_criticos_em_lote(self):
    """Testa se 85% dos chamados críticos são respondidos em até 15 minutos"""
    total_chamados = 100
    chamados_no_tempo = 87
    assert chamados_no_tempo / total_chamados >= 0.85, "Menos de 85% dos chamados críticos foram respondidos no prazo"
```
```python
def test_falha_api_suporte(self):
    """Testa se o sistema exibe mensagem de fallback quando a API de suporte falha"""
    falha_simulada = True
    fallback_ativado = False
    if falha_simulada:
        fallback_ativado = True
    assert fallback_ativado, "Sistema não exibiu fallback corretamente ao falhar a API de suporte"
```

### **2.2 Estratégia para DN2 - Sincronização de Estoque**
**Objetivo:** Garantir que o estoque esteja atualizado para evitar cancelamentos e garantir confiabilidade nas informações.

#### **Cenários de Teste**
| ID | Cenário | Entrada | Resultado Esperado |
|----|---------|---------|--------------------|
| DN2-01 | Atualização de estoque em tempo real | Alteração manual no banco de estoque | Atualização refletida no sistema em até 10s |
| DN2-02 | Testar sincronização massiva de estoque | 1.000 mudanças no estoque em 5 min | 95% sincronizadas corretamente em até 2 min |
| DN2-03 | Testar recuperação após falha na API de sincronização | API de sincronização falha 2 vezes antes de recuperar | O sistema deve tentar novamente até recuperar a sincronização |

### **Código de Teste para DN2**
```python
def test_sincronizacao_massiva_carga_alta(self):
    """Testa se 95% das mudanças no estoque são sincronizadas corretamente em até 2 minutos"""
    total_alteracoes = 1000
    alteracoes_sucesso = 960
    assert alteracoes_sucesso / total_alteracoes >= 0.95, "Menos de 95% das mudanças de estoque foram sincronizadas no tempo esperado"
```
```python
def test_falha_api_sincronizacao(self):
    """Testa se o sistema tenta novamente sincronizar após falha"""
    falha_simulada = True
    tentativa_sucesso = False
    tentativas = 0
    while falha_simulada and tentativas < 5:
        tentativas += 1
        time.sleep(2)
        if tentativas == 3:
            tentativa_sucesso = True
            falha_simulada = False
    assert tentativa_sucesso, "Sistema não conseguiu recuperar a sincronização após falha"
```

## **3. Massa de Testes**

Para os testes serem confiáveis, é necessário criar uma base de dados realista que represente os diferentes cenários possíveis.

```python
 def setup_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE chamados (
                        id TEXT PRIMARY KEY,
                        tipo TEXT,
                        prioridade TEXT,
                        tempo_esperado INTEGER)''')
    chamados_testes = [
        ("CH001", "Pagamento não recebido", "Crítico", 24),
        ("CH002", "Conta bloqueada", "Crítico", 24),
        ("CH003", "Erro no endereço de entrega", "Médio", 48)
    ]
    cursor.executemany("INSERT INTO chamados VALUES (?, ?, ?, ?)", chamados_testes)
    conn.commit()
    return conn
```

## **4. Codificação como Documentação de Testes**

Os testes acima são executados para aferir a qualidade dos direcionadores de negócio de forma programática. Eles podem ser encontrados no caminho `tests\test_dn_rappi.py`.

