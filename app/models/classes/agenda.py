from datetime import datetime

from classes.aula import Aula


def chave_ordenacao_data(data_str: str) -> tuple[int, str]:
    """Ordena datas no formato dd/mm/aa ou dd/mm/aaaa cronologicamente."""
    texto = data_str.strip()
    for fmt in ("%d/%m/%y", "%d/%m/%Y"):
        try:
            dt = datetime.strptime(texto, fmt)
            return (0, dt.strftime("%Y-%m-%d"))
        except ValueError:
            continue
    return (1, texto)


class AgendaMensal:
    """Gerencia a coleção de aulas de um professor (Composição com Professor)."""

    def __init__(self):
        self._aulas: list[Aula] = []

    @property
    def aulas(self) -> list[Aula]:
        return list(self._aulas)

    def esta_vazia(self) -> bool:
        return len(self._aulas) == 0

    def ordenar(self) -> None:
        self._aulas.sort(key=lambda aula: chave_ordenacao_data(aula.data_aula))

    def adicionar(self, aula: Aula) -> None:
        self._aulas.append(aula)
        self.ordenar()

    def substituir(self, indice: int, nova_aula: Aula) -> None:
        if indice < 0 or indice >= len(self._aulas):
            raise IndexError("Índice de aula inválido.")
        self._aulas[indice] = nova_aula
        self.ordenar()

    def obter(self, indice: int) -> Aula:
        if indice < 0 or indice >= len(self._aulas):
            raise IndexError("Índice de aula inválido.")
        return self._aulas[indice]

    def limpar(self) -> None:
        self._aulas.clear()

    def dias_trabalhados(self) -> set[str]:
        return {aula.data_aula for aula in self._aulas}
