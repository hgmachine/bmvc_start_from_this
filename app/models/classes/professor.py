from classes.agenda import AgendaMensal
from classes.aula import Aula
from classes.pessoa import Pessoa


class Professor(Pessoa):
    """Representa um professor do reforço escolar e compõe sua AgendaMensal."""

    def __init__(
        self,
        nome: str,
        email: str,
        login: str,
        senha: str,
        id: int | None = None,
    ):
        super().__init__(nome)
        self.id = id
        self.email = email.strip()
        self.login = login.strip()
        self.senha = senha.strip()
        # Composição: a AgendaMensal nasce com o Professor e pertence a ele
        self.agenda = AgendaMensal()

    def exibir_identificacao(self) -> str:
        return f"Professor(a): {self.nome} | Email: {self.email}"

    def adicionar_aula(self, aula: Aula) -> None:
        aula.professor = self
        self.agenda.adicionar(aula)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "login": self.login,
            "senha": self.senha,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Professor":
        return cls(
            nome=dados["nome"],
            email=dados["email"],
            login=dados["login"],
            senha=dados["senha"],
            id=dados.get("id"),
        )
