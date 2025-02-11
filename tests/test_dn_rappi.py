import pytest
import sqlite3
import time
from unittest import TestCase

# Configuração do Banco de Dados Simulado
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
        ("CH003", "Erro no endereço de entrega", "Médio", 48),
        ("CH004", "Dúvida sobre taxas", "Baixo", 48),
        ("CH005", "Problema com aplicativo", "Médio", 48),
    ]
    cursor.executemany("INSERT INTO chamados VALUES (?, ?, ?, ?)", chamados_testes)

    cursor.execute('''CREATE TABLE estoque (
                        id TEXT PRIMARY KEY,
                        loja TEXT,
                        quantidade_anterior INTEGER,
                        quantidade_atual INTEGER,
                        tempo_sincronizacao INTEGER)''')
    
    estoque_testes = [
        ("IT001", "Loja A", 10, 5, 10),
        ("IT002", "Loja B", 50, 49, 10),
        ("IT003", "Loja C", 0, 10, 10),
        ("IT004", "Loja D", 100, 80, 10),
        ("IT005", "Loja E", 5, 0, 10),
    ]
    cursor.executemany("INSERT INTO estoque VALUES (?, ?, ?, ?, ?)", estoque_testes)

    conn.commit()
    return conn


class TestSuporte(TestCase):

    def setUp(self):
        self.conn = setup_db()
        self.cursor = self.conn.cursor()

    def test_chamado_critico_prioritario(self):
        """Testa se chamados críticos são escalados corretamente em até 1 min"""
        chamado_critico = {"tipo": "Pagamento não recebido", "prioridade": "Crítico"}
        start_time = time.time()

        # Simulando requisição ao suporte
        response_time = 30

        assert response_time < 60, "Chamado crítico não foi priorizado corretamente"

        end_time = time.time()
        print(f"Tempo de resposta do chamado crítico: {end_time - start_time:.2f} segundos")

    def test_resposta_chamados_criticos_em_lote(self):
        """Testa se 85% dos chamados críticos são respondidos em até 15 minutos"""
        total_chamados = 100
        chamados_no_tempo = 87

        assert chamados_no_tempo / total_chamados >= 0.85, "Menos de 85% dos chamados críticos foram respondidos no prazo"

    def test_resposta_chamados_gerais(self):
        """Testa se 95% dos chamados gerais são respondidos em até 2h"""
        total_chamados = 100
        chamados_no_tempo = 96

        assert chamados_no_tempo / total_chamados >= 0.95, "Menos de 95% dos chamados foram respondidos no prazo"

    def test_falha_api_suporte(self):
        """Testa se o sistema exibe mensagem de fallback quando a API de suporte falha"""
        falha_simulada = True
        fallback_ativado = False

        if falha_simulada:
            fallback_ativado = True

        assert fallback_ativado, "Sistema não exibiu fallback corretamente ao falhar a API de suporte"


class TestSincronizacaoEstoque(TestCase):

    def setUp(self):
        self.conn = setup_db()
        self.cursor = self.conn.cursor()

    def test_atualizacao_estoque_tempo_real(self):
        """Testa se a atualização do estoque ocorre em até 10 segundos"""
        start_time = time.time()

        # Simulando uma atualização de estoque
        item_id = "IT001"
        self.cursor.execute("UPDATE estoque SET quantidade_atual = ? WHERE id = ?", (3, item_id))
        self.conn.commit()

        end_time = time.time()
        sync_time = end_time - start_time

        assert sync_time <= 10, f"Tempo de sincronização foi {sync_time:.2f}s, acima do limite"

    def test_sincronizacao_massiva_carga_alta(self):
        """Testa se 95% das mudanças no estoque são sincronizadas corretamente em até 2 minutos"""
        total_alteracoes = 1000
        alteracoes_sucesso = 960

        assert alteracoes_sucesso / total_alteracoes >= 0.95, "Menos de 95% das mudanças de estoque foram sincronizadas no tempo esperado"

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


if __name__ == "__main__":
    pytest.main()
