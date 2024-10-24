from datetime import datetime
import pytz
from random import randint

class ContaCorrente:
    def __init__(self, nome, cpf, agencia, num_conta):
        self._nome = nome
        self._cpf = cpf
        self._saldo = 0
        self._limite = -1000
        self._agencia = agencia
        self._num_conta = num_conta
        self._transacoes = []
        self._cartoes = []

    def consultar_saldo(self):
        print('Seu saldo atual é de R${:.2f}'.format(self._saldo))

    def depositar_dinheiro(self, valor):
        self._saldo += valor
        self._transacoes.append((valor, self._saldo, self.data_hora()))

    def sacar_dinheiro(self, valor):
        if self._saldo - valor < self._limite:
            print("Você não tem saldo suficiente para sacar esse valor")
            self.consultar_saldo()
        else:
            self._saldo -= valor
            self._transacoes.append((-valor, self._saldo, self.data_hora()))

    @staticmethod
    def data_hora():
        return datetime.now(pytz.timezone("Brazil/East"))

    def consultar_historico_transacoes(self):
        print('Histórico de Transações:')
        for transacao in self._transacoes:
            print(transacao)

    def criar_cartao_credito(self):
        cartao = CartaoCredito(self._nome, self)
        self._cartoes.append(cartao)
        return cartao

class CartaoCredito:
    def __init__(self, titular, conta_corrente):
        self.numero = randint(1000000000000000, 9999999999999999)
        self.titular = titular
        self.validade = f"{CartaoCredito._data_hora().month}/{CartaoCredito._data_hora().year + 4}"
        self.cod_seguranca = f"{randint(100, 999)}"
        self.limite = 1000
        self.conta_corrente = conta_corrente

    @staticmethod
    def _data_hora():
        fuso_BR = pytz.timezone("Brazil/East")
        horario_BR = datetime.now(fuso_BR)
        return horario_BR

conta_lira = ContaCorrente("Lira", "111.222.333-45", "1234", "56789")
conta_lira.consultar_saldo()
conta_lira.depositar_dinheiro(10000)
conta_lira.consultar_saldo()
conta_lira.sacar_dinheiro(1000)
conta_lira.consultar_saldo()
print('Saldo Final:')
conta_lira.consultar_saldo()

conta_lira.consultar_historico_transacoes()

cartao_lira = conta_lira.criar_cartao_credito()
print(f"Número do Cartão: {cartao_lira.numero}")
print(f"Titular: {cartao_lira.titular}")
print(f"Validade: {cartao_lira.validade}")
print(f"Código de Segurança: {cartao_lira.cod_seguranca}")
print(f"Limite: R${cartao_lira.limite}")

print("Tentativa de acessar saldo diretamente (deveria falhar):")
try:
    print(conta_lira._saldo)
except AttributeError as e:
    print(e)

try:
    conta_lira._saldo = 8000
except AttributeError as e:
    print(e)

conta_lira.consultar_saldo()

print(f"Cartões associados à conta: {conta_lira._cartoes}")
