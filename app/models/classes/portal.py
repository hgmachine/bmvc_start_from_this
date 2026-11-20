from classes.agenda import chave_ordenacao_data
from classes.aluno import Aluno
from classes.aula import Aula, FabricaAula
from classes.calculadora_salario import CalculadoraSalario, ResumoSalario, ValeTransporte
from classes.professor import Professor
from app.controllers.db.banco_alunos import BancoAulas, CAMINHO_DB_ALUNOS
from app.controllers.db.banco_professores import BancoProfessores, CAMINHO_DB


class PortalAlfabeta:
    """Controlador principal do sistema (Composição com repositórios e Associação com entidades)."""

    def __init__(
        self,
        caminho_professores: str = CAMINHO_DB,
        caminho_aulas: str = CAMINHO_DB_ALUNOS,
    ):
        # Composição: o portal cria e gerencia seus repositórios
        self.banco_professores = BancoProfessores(caminho_professores)
        self.banco_aulas = BancoAulas(caminho_aulas)
        self.professores: list[Professor] = []
        self.aulas: list[Aula] = []
        self.carregar_dados()

    def carregar_dados(self) -> None:
        self.professores = self.banco_professores.carregar()
        mapa_professores = {
            prof.id: prof for prof in self.professores if prof.id is not None
        }
        self.aulas = self.banco_aulas.carregar(mapa_professores)
        self._ordenar_aulas()

    def _ordenar_aulas(self) -> None:
        self.aulas.sort(key=lambda aula: chave_ordenacao_data(aula.data_aula))

    def registrar_professor(
        self,
        nome: str,
        email: str,
        login: str,
        senha: str,
    ) -> Professor:
        login_limpo = login.strip()
        email_limpo = email.strip()
        senha_limpa = senha.strip()
        if not email_limpo or not login_limpo or not senha_limpa:
            raise ValueError("Email, login e senha são obrigatórios.")
        if any(p.login == login_limpo for p in self.professores):
            raise ValueError(f"O login '{login_limpo}' já está em uso.")

        proximo_id = max((p.id for p in self.professores if p.id is not None), default=0) + 1
        novo_professor = Professor(
            nome=nome,
            email=email_limpo,
            login=login_limpo,
            senha=senha_limpa,
            id=proximo_id,
        )
        self.professores.append(novo_professor)
        self.professores.sort(key=lambda p: p.nome.lower())
        self.banco_professores.salvar(self.professores)
        return novo_professor

    def autenticar(self, login: str, senha: str) -> Professor | None:
        login_limpo = login.strip()
        senha_limpa = senha.strip()
        for professor in self.professores:
            if professor.login == login_limpo and professor.senha == senha_limpa:
                return professor
        return None

    def adicionar_aula(
        self,
        professor: Professor,
        nome_aluno: str,
        data_aula: str,
        opcao_tipo: str,
    ) -> Aula:
        aluno = Aluno(nome_aluno)
        nova_aula = FabricaAula.criar_por_opcao(
            opcao=opcao_tipo,
            aluno=aluno,
            data_aula=data_aula,
            professor=professor,
        )
        professor.adicionar_aula(nova_aula)
        self.aulas.append(nova_aula)
        self._ordenar_aulas()
        self.banco_aulas.salvar(self.aulas)
        return nova_aula

    def alterar_aula(
        self,
        professor: Professor,
        indice: int,
        novo_nome_aluno: str | None = None,
        nova_data_aula: str | None = None,
        nova_opcao_tipo: str | None = None,
    ) -> Aula:
        aula_atual = professor.agenda.obter(indice)

        nome_final = (
            novo_nome_aluno.strip()
            if novo_nome_aluno and novo_nome_aluno.strip()
            else aula_atual.aluno.nome
        )
        data_final = (
            nova_data_aula.strip()
            if nova_data_aula and nova_data_aula.strip()
            else aula_atual.data_aula
        )
        aluno_atualizado = Aluno(nome_final)

        if nova_opcao_tipo and nova_opcao_tipo.strip():
            aula_atualizada = FabricaAula.criar_por_opcao(
                opcao=nova_opcao_tipo,
                aluno=aluno_atualizado,
                data_aula=data_final,
                professor=professor,
            )
        else:
            aula_atualizada = FabricaAula.criar_por_tipo(
                tipo_aula=aula_atual.tipo_aula,
                aluno=aluno_atualizado,
                data_aula=data_final,
                professor=professor,
            )

        professor.agenda.substituir(indice, aula_atualizada)

        pos_global = self.aulas.index(aula_atual)
        self.aulas[pos_global] = aula_atualizada
        self._ordenar_aulas()
        self.banco_aulas.salvar(self.aulas)
        return aula_atualizada

    def listar_aulas(self, professor: Professor) -> list[Aula]:
        return professor.agenda.aulas

    def calcular_salario(
        self,
        professor: Professor,
        valor_vale_diario: float | None = None,
    ) -> ResumoSalario:
        vale = (
            ValeTransporte(valor_vale_diario)
            if valor_vale_diario is not None
            else None
        )
        return CalculadoraSalario.calcular(professor, vale)

    def finalizar_mes(self, professor: Professor) -> int:
        quantidade_removida = len(professor.agenda.aulas)
        if quantidade_removida == 0:
            return 0

        aulas_do_professor = set(professor.agenda.aulas)
        professor.agenda.limpar()
        self.aulas = [a for a in self.aulas if a not in aulas_do_professor]
        self.banco_aulas.salvar(self.aulas)
        return quantidade_removida
