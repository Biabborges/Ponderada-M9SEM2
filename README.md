# **Ponderada SEM 2 - Exercitando no Projeto**

## **Descrição**
Este projeto implementa testes para validar a eficiência do suporte e a sincronização de estoque na Rappi:

- **DN1** - Tempo máximo de resposta a chamados: 85% dos casos críticos respondidos em até 15 minutos; 95% dos chamados gerais em até 2 horas.
- **DN2** - Sincronização de estoque: 95% das lojas devem ter atualização a cada 2 minutos, com tempo máximo de atualização de itens em 10 segundos.  


## **Como Executar**
1. Clone o repositório.
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute os testes com `pytest`:
   ```bash
   pytest test_suporte.py
   pytest test_estoque.py
   ```

## **Tecnologias**
- Python
- Pytest
- SQLite

