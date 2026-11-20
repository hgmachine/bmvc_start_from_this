from dataclasses import dataclass

from classes.professor import Professor


class ValeTransporte:
    """Representa o benefício de vale-transporte calculado por dia trabalhado."""

    def __init__(self, valor_diario: float):
        if valor_diario < 0:
            raise ValueError("O valor diário do vale-transporte não pode ser negativo.")
        self.valor_diario = float(valor_diario)

    def calcular_total(self, dias_trabalhados: int) -> float:
        return dias_trabalhados * self.valor_diario


@dataclass(frozen=True)
class ResumoSalario:
    total_aulas: float
    dias_trabalhados: int
    total_vale_transporte: float
    total_geral: float


class CalculadoraSalario:
    """Calcula o salário mensal de um professor (Dependência com Professor e ValeTransporte)."""

    @staticmethod
    def calcular(
        professor: Professor,
        vale_transporte: ValeTransporte | None = None,
    ) -> ResumoSalario:
        aulas = professor.agenda.aulas
        # Uso polimórfico: cada subclasse de Aula resolve seu próprio calcular_valor()
        total_aulas = sum(aula.calcular_valor() for aula in aulas)
        dias = len(professor.agenda.dias_trabalhados())
        total_vt = vale_transporte.calcular_total(dias) if vale_transporte else 0.0
        return ResumoSalario(
            total_aulas=round(total_aulas, 2),
            dias_trabalhados=dias,
            total_vale_transporte=round(total_vt, 2),
            total_geral=round(total_aulas + total_vt, 2),
        )
