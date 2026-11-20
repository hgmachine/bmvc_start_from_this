from abc import ABC, abstractmethod


class Pessoa(ABC):
    """Classe base abstrata que representa uma pessoa no sistema."""

    def __init__(self, nome: str):
        nome_limpo = nome.strip()
        if not nome_limpo:
            raise ValueError("O nome não pode ficar vazio.")
        self.nome = nome_limpo

    @abstractmethod
    def exibir_identificacao(self) -> str:
        """Retorna uma representação formatada da pessoa (polimorfismo)."""
        raise NotImplementedError
