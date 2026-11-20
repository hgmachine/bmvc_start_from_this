from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from classes.aluno import Aluno

if TYPE_CHECKING:
    from classes.professor import Professor


class Aula(ABC):
    """Classe base abstrata para aulas ministradas no reforço escolar."""

    def __init__(self, aluno: Aluno, data_aula: str, professor: "Professor | None" = None):
        data_limpa = data_aula.strip()
        if not data_limpa:
            raise ValueError("A data da aula não pode ficar vazia.")
        self.aluno = aluno
        self.data_aula = data_limpa
        self.professor = professor

    @property
    def id_professor(self) -> int | None:
        return self.professor.id if self.professor is not None else None

    @property
    @abstractmethod
    def tipo_aula(self) -> str:
        """Nome descritivo da modalidade da aula."""
        raise NotImplementedError

    @abstractmethod
    def calcular_valor(self) -> float:
        """Calcula o valor da aula de forma polimórfica."""
        raise NotImplementedError

    def descrever(self) -> str:
        return (
            f"Aluno: {self.aluno.nome} | "
            f"Data: {self.data_aula} | "
            f"Tipo: {self.tipo_aula} | "
            f"Valor: R$ {self.calcular_valor():.2f}"
        )

    def to_dict(self) -> dict:
        return {
            "nome": self.aluno.nome,
            "data_aula": self.data_aula,
            "id_professor": self.id_professor,
            "tipo_de_aula": self.tipo_aula,
            "valor": self.calcular_valor(),
        }


class AulaFundamentalColetivo(Aula):
    @property
    def tipo_aula(self) -> str:
        return "Fundamental Coletivo"

    def calcular_valor(self) -> float:
        return 9.92


class AulaFundamentalIndividual(Aula):
    @property
    def tipo_aula(self) -> str:
        return "Fundamental Individual"

    def calcular_valor(self) -> float:
        return 16.54


class AulaMedioColetivo(Aula):
    @property
    def tipo_aula(self) -> str:
        return "Médio Coletivo"

    def calcular_valor(self) -> float:
        return 16.54


class AulaMedioIndividual(Aula):
    @property
    def tipo_aula(self) -> str:
        return "Médio Individual"

    def calcular_valor(self) -> float:
        return 19.85


class AulaFimDeSemana(Aula):
    @property
    def tipo_aula(self) -> str:
        return "Fim de Semana"

    def calcular_valor(self) -> float:
        return 37.50


class FabricaAula:
    """Fábrica responsável por instanciar a subclasse correta de Aula (Dependência)."""

    OPCOES = {
        "1": AulaFundamentalColetivo,
        "2": AulaFundamentalIndividual,
        "3": AulaMedioColetivo,
        "4": AulaMedioIndividual,
        "5": AulaFimDeSemana,
    }

    POR_TIPO = {
        "Fundamental Coletivo": AulaFundamentalColetivo,
        "Fundamental Individual": AulaFundamentalIndividual,
        "Médio Coletivo": AulaMedioColetivo,
        "Médio Individual": AulaMedioIndividual,
        "Fim de Semana": AulaFimDeSemana,
    }

    @classmethod
    def listar_opcoes(cls) -> list[tuple[str, str]]:
        return [
            (codigo, subclasse(Aluno("Exemplo"), "01/01/00").tipo_aula)
            for codigo, subclasse in cls.OPCOES.items()
        ]

    @classmethod
    def criar_por_opcao(
        cls,
        opcao: str,
        aluno: Aluno,
        data_aula: str,
        professor: "Professor | None" = None,
    ) -> Aula:
        classe_aula = cls.OPCOES.get(opcao.strip())
        if classe_aula is None:
            raise ValueError(f"Opção de aula inválida: {opcao!r}")
        return classe_aula(aluno=aluno, data_aula=data_aula, professor=professor)

    @classmethod
    def criar_por_tipo(
        cls,
        tipo_aula: str,
        aluno: Aluno,
        data_aula: str,
        professor: "Professor | None" = None,
    ) -> Aula:
        classe_aula = cls.POR_TIPO.get(tipo_aula)
        if classe_aula is None:
            raise ValueError(f"Tipo de aula desconhecido: {tipo_aula!r}")
        return classe_aula(aluno=aluno, data_aula=data_aula, professor=professor)

    @classmethod
    def from_dict(cls, dados: dict, professor: "Professor | None" = None) -> Aula:
        aluno = Aluno(dados["nome"])
        tipo = dados.get("tipo_de_aula", "")
        return cls.criar_por_tipo(
            tipo_aula=tipo,
            aluno=aluno,
            data_aula=dados["data_aula"],
            professor=professor,
        )
