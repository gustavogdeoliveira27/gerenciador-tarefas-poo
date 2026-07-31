import json
import os
from datetime import datetime

ARQUIVO_DADOS = "tarefas.json"


class Tarefa:
    def __init__(self, titulo, descricao, status="Pendente", data_criacao=None):
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.data_criacao = data_criacao or datetime.now()

    def concluir(self):
        self.status = "Concluída"

    def atualizar(self, novo_titulo=None, nova_descricao=None):
        if novo_titulo:
            self.titulo = novo_titulo
        if nova_descricao:
            self.descricao = nova_descricao

    def para_dicionario(self):
        """Converte a tarefa em dicionário para salvar no JSON."""
        return {
            "titulo": self.titulo,
            "descricao": self.descricao,
            "status": self.status,
            "data_criacao": self.data_criacao.isoformat()
        }

    @classmethod
    def de_dicionario(cls, dados):
        """Recria uma tarefa a partir dos dados lidos do JSON."""
        return cls(
            titulo=dados["titulo"],
            descricao=dados["descricao"],
            status=dados["status"],
            data_criacao=datetime.fromisoformat(dados["data_criacao"])
        )

    def __str__(self):
        return (f"Título: {self.titulo}\n"
                f"Descrição: {self.descricao}\n"
                f"Status: {self.status}\n"
                f"Criada em: {self.data_criacao.strftime('%d/%m/%Y %H:%M:%S')}\n")


class GerenciadorTarefas:
    def __init__(self, arquivo=ARQUIVO_DADOS):
        self.arquivo = arquivo
        self.tarefas = []
        self.carregar()

    # ---------- PERSISTÊNCIA ----------
    def salvar(self):
        """Grava todas as tarefas no arquivo JSON."""
        try:
            with open(self.arquivo, "w", encoding="utf-8") as f:
                json.dump(
                    [t.para_dicionario() for t in self.tarefas],
                    f,
                    ensure_ascii=False,
                    indent=2
                )
        except OSError as erro:
            print(f"Não foi possível salvar as tarefas: {erro}")

    def carregar(self):
        """Lê as tarefas do arquivo JSON, se ele existir."""
        if not os.path.exists(self.arquivo):
            return

        try:
            with open(self.arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
            self.tarefas = [Tarefa.de_dicionario(d) for d in dados]
        except (OSError, json.JSONDecodeError, KeyError, ValueError):
            print("Arquivo de tarefas corrompido ou ilegível. Iniciando lista vazia.")
            self.tarefas = []

    # ---------- VALIDAÇÃO ----------
    def id_valido(self, id_tarefa):
        """Garante que o ID existe na lista (bloqueia negativos e fora do intervalo)."""
        return 0 <= id_tarefa < len(self.tarefas)

    # ---------- CREATE ----------
    def criar_tarefa(self, titulo, descricao):
        if not titulo.strip():
            print("O título não pode ficar vazio.")
            return

        self.tarefas.append(Tarefa(titulo, descricao))
        self.salvar()
        print("Tarefa criada com sucesso!")

    # ---------- READ ----------
    def listar_tarefas(self):
        if not self.tarefas:
            print("Nenhuma tarefa cadastrada.")
            return

        for i, tarefa in enumerate(self.tarefas):
            print(f"ID: {i}")
            print(tarefa)
            print("-" * 30)

    # ---------- UPDATE ----------
    def atualizar_tarefa(self, id_tarefa, titulo=None, descricao=None):
        if not self.id_valido(id_tarefa):
            print("ID inválido.")
            return

        self.tarefas[id_tarefa].atualizar(titulo, descricao)
        self.salvar()
        print("Tarefa atualizada com sucesso!")

    # ---------- DELETE ----------
    def excluir_tarefa(self, id_tarefa):
        if not self.id_valido(id_tarefa):
            print("ID inválido.")
            return

        self.tarefas.pop(id_tarefa)
        self.salvar()
        print("Tarefa excluída com sucesso!")

    # ---------- CONCLUIR ----------
    def concluir_tarefa(self, id_tarefa):
        if not self.id_valido(id_tarefa):
            print("ID inválido.")
            return

        self.tarefas[id_tarefa].concluir()
        self.salvar()
        print("Tarefa marcada como concluída!")


def ler_id(sistema):
    """Lê um ID do usuário, tratando texto inválido e IDs inexistentes."""
    if not sistema.tarefas:
        print("Nenhuma tarefa cadastrada.")
        return None

    entrada = input("ID da tarefa: ").strip()

    try:
        id_tarefa = int(entrada)
    except ValueError:
        print("Digite um número inteiro válido.")
        return None

    if not sistema.id_valido(id_tarefa):
        print(f"ID inválido. Use um valor entre 0 e {len(sistema.tarefas) - 1}.")
        return None

    return id_tarefa


def menu():
    sistema = GerenciadorTarefas()

    while True:
        print("\n===== GERENCIADOR DE TAREFAS =====")
        print("1 - Criar tarefa")
        print("2 - Listar tarefas")
        print("3 - Atualizar tarefa")
        print("4 - Excluir tarefa")
        print("5 - Concluir tarefa")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            titulo = input("Título: ")
            descricao = input("Descrição: ")
            sistema.criar_tarefa(titulo, descricao)

        elif opcao == "2":
            sistema.listar_tarefas()

        elif opcao == "3":
            id_tarefa = ler_id(sistema)
            if id_tarefa is None:
                continue

            titulo = input("Novo título (enter para manter): ")
            descricao = input("Nova descrição (enter para manter): ")
            sistema.atualizar_tarefa(
                id_tarefa,
                titulo if titulo else None,
                descricao if descricao else None
            )

        elif opcao == "4":
            id_tarefa = ler_id(sistema)
            if id_tarefa is None:
                continue
            sistema.excluir_tarefa(id_tarefa)

        elif opcao == "5":
            id_tarefa = ler_id(sistema)
            if id_tarefa is None:
                continue
            sistema.concluir_tarefa(id_tarefa)

        elif opcao == "0":
            print("Encerrando sistema...")
            break

        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu()
