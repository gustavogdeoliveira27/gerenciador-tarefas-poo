from datetime import datetime


class Tarefa:
    def __init__(self, titulo, descricao):
        self.titulo = titulo
        self.descricao = descricao
        self.status = "Pendente"
        self.data_criacao = datetime.now()

    def concluir(self):
        self.status = "Concluída"

    def atualizar(self, novo_titulo=None, nova_descricao=None):
        if novo_titulo:
            self.titulo = novo_titulo
        if nova_descricao:
            self.descricao = nova_descricao

    def __str__(self):
        return (f"Título: {self.titulo}\n"
                f"Descrição: {self.descricao}\n"
                f"Status: {self.status}\n"
                f"Criada em: {self.data_criacao.strftime('%d/%m/%Y %H:%M:%S')}\n")


class GerenciadorTarefas:
    def __init__(self):
        self.tarefas = []

    # CREATE
    def criar_tarefa(self, titulo, descricao):
        tarefa = Tarefa(titulo, descricao)
        self.tarefas.append(tarefa)
        print("Tarefa criada com sucesso!")

    # READ
    def listar_tarefas(self):
        if not self.tarefas:
            print("Nenhuma tarefa cadastrada.")
            return

        for i, tarefa in enumerate(self.tarefas):
            print(f"ID: {i}")
            print(tarefa)
            print("-" * 30)

    # UPDATE
    def atualizar_tarefa(self, id_tarefa, titulo=None, descricao=None):
        try:
            self.tarefas[id_tarefa].atualizar(titulo, descricao)
            print("Tarefa atualizada com sucesso!")
        except IndexError:
            print("ID inválido.")

    # DELETE
    def excluir_tarefa(self, id_tarefa):
        try:
            self.tarefas.pop(id_tarefa)
            print("Tarefa excluída com sucesso!")
        except IndexError:
            print("ID inválido.")

    # CONCLUIR
    def concluir_tarefa(self, id_tarefa):
        try:
            self.tarefas[id_tarefa].concluir()
            print("Tarefa marcada como concluída!")
        except IndexError:
            print("ID inválido.")


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

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            titulo = input("Título: ")
            descricao = input("Descrição: ")
            sistema.criar_tarefa(titulo, descricao)

        elif opcao == "2":
            sistema.listar_tarefas()

        elif opcao == "3":
            id_tarefa = int(input("ID da tarefa: "))
            titulo = input("Novo título (enter para manter): ")
            descricao = input("Nova descrição (enter para manter): ")
            sistema.atualizar_tarefa(
                id_tarefa,
                titulo if titulo else None,
                descricao if descricao else None
            )

        elif opcao == "4":
            id_tarefa = int(input("ID da tarefa: "))
            sistema.excluir_tarefa(id_tarefa)

        elif opcao == "5":
            id_tarefa = int(input("ID da tarefa: "))
            sistema.concluir_tarefa(id_tarefa)

        elif opcao == "0":
            print("Encerrando sistema...")
            break

        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu()