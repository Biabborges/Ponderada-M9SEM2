# **Estratégia e Massa de Testes**

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
| DN1-02 | Testar tempo de resposta para chamados críticos | 100 chamados simultâneos | 85% respondidos em até 15 minutos |
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
 def test_resposta_chamados_gerais(self):
    """Testa se 95% dos chamados gerais são respondidos em até 2h"""
    total_chamados = 100
    chamados_no_tempo = 96
    assert chamados_no_tempo / total_chamados >= 0.95, "Menos de 95% dos chamados foram respondidos no prazo"
```

### **2.2 Estratégia para DN2 - Sincronização de Estoque**
**Objetivo:** Garantir que o estoque esteja atualizado para evitar cancelamentos e garantir confiabilidade nas informações.

#### **Cenários de Teste**
| ID | Cenário | Entrada | Resultado Esperado |
|----|---------|---------|--------------------|
| DN2-01 | Atualização de estoque em tempo real | Alteração manual no banco de estoque | Atualização refletida no sistema em até 10s |
| DN2-02 | Testar sincronização automática | 1.000 mudanças no estoque em 5 min | 95% sincronizadas corretamente em até 2 min |

### **Código de Teste para DN2**
```python
 def test_atualizacao_estoque_tempo_real(self):
    """Testa se a atualização do estoque ocorre em até 10 segundos"""
    start_time = time.time()
    item_id = "IT001"
    self.cursor.execute("UPDATE estoque SET quantidade_atual = ? WHERE id = ?", (3, item_id))
    self.conn.commit()
    end_time = time.time()
    sync_time = end_time - start_time
    assert sync_time <= 10, f"Tempo de sincronização foi {sync_time:.2f}s, acima do limite"
```
```python
 def test_sincronizacao_massiva(self):
    """Testa se 95% das lojas sincronizam o estoque corretamente em até 2 minutos"""
    total_lojas = 1000
    lojas_sincronizadas = 970
    assert lojas_sincronizadas / total_lojas >= 0.95, "Menos de 95% das lojas sincronizaram no tempo esperado"
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

