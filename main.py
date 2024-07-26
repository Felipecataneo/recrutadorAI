from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class RecruitmentCrew:
    def __init__(self, pdf_tool=None):
        self.pdf_tool = pdf_tool
        print("crew iniciado")
        self.agents_config = 'config/agents.yaml'
        self.tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[self.pdf_tool] if self.pdf_tool else [],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def matcher(self) -> Agent:
        return Agent(
            config=self.agents_config['matcher'],
            tools=[self.pdf_tool] if self.pdf_tool else [],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def communicator(self) -> Agent:
        return Agent(
            config=self.agents_config['communicator'],
            tools=[self.pdf_tool] if self.pdf_tool else [],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def reporter(self) -> Agent:
        return Agent(
            config=self.agents_config['reporter'],
            allow_delegation=False,
            verbose=True,
        )

    @task
    def research_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_candidates_task'],
            agent=self.researcher(),
        )

    @task
    def match_and_score_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config['match_and_score_candidates_task'],
            agent=self.matcher()
        )

    @task
    def report_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_candidates_task'],
            agent=self.reporter(),
            context=[self.research_candidates_task(), self.match_and_score_candidates_task()],
        )

    @crew
    def crew(self) -> Crew:
        """Criar o time de recrutadores"""
        agents = [self.researcher(), self.matcher(), self.communicator(), self.reporter()]
        tasks = [self.research_candidates_task(), self.match_and_score_candidates_task(), self.report_candidates_task()]
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=2,
        )
