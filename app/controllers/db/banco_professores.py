import json
import os

from classes.professor import Professor

CAMINHO_DB = os.path.join(os.path.dirname(__file__), "dataBase_professor.json")


class BancoProfessores:
    """Repositório JSON responsável pela persistência de professores."""

    def __init__(self, caminho: str = CAMINHO_DB):
        self.caminho = caminho

    def carregar(self) -> list[Professor]:
        if not os.path.exists(self.caminho) or os.path.getsize(self.caminho) == 0:
            return []
        try:
            with open(self.caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
            return [Professor.from_dict(item) for item in dados]
        except json.JSONDecodeError:
            return []

    def salvar(self, lista_professores: list[Professor]) -> None:
        dados_pra_salvar = [prof.to_dict() for prof in lista_professores]
        os.makedirs(os.path.dirname(self.caminho), exist_ok=True)
        with open(self.caminho, "w", encoding="utf-8") as f:
            json.dump(dados_pra_salvar, f, indent=4, ensure_ascii=False)
