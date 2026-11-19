from classes.pessoa import Pessoa


class Aluno(Pessoa):
    """Representa um aluno atendido no reforço escolar."""

    def __init__(self, nome: str):
        super().__init__(nome)

    def exibir_identificacao(self) -> str:
        return f"Aluno: {self.nome}"
