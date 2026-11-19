import json
import os

from classes.aula import Aula, FabricaAula
from classes.professor import Professor

CAMINHO_DB_ALUNOS = os.path.join(os.path.dirname(__file__), "dataBase_alunos.json")


class BancoAulas:
    """Repositório JSON responsável pela persistência das aulas registradas."""

    def __init__(self, caminho: str = CAMINHO_DB_ALUNOS):
        self.caminho = caminho

    def carregar(
        self,
        professores_por_id: dict[int, Professor] | None = None,
    ) -> list[Aula]:
        if not os.path.exists(self.caminho) or os.path.getsize(self.caminho) == 0:
            return []
        try:
            with open(self.caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except json.JSONDecodeError:
            return []

        mapa_prof = professores_por_id or {}
        aulas: list[Aula] = []
        for item in dados:
            prof = mapa_prof.get(item.get("id_professor"))
            aula = FabricaAula.from_dict(item, professor=prof)
            aulas.append(aula)
            if prof is not None:
                prof.adicionar_aula(aula)
        return aulas

    def salvar(self, lista_aulas: list[Aula]) -> None:
        dados_pra_salvar = [aula.to_dict() for aula in lista_aulas]
        os.makedirs(os.path.dirname(self.caminho), exist_ok=True)
        with open(self.caminho, "w", encoding="utf-8") as f:
            json.dump(dados_pra_salvar, f, indent=4, ensure_ascii=False)
