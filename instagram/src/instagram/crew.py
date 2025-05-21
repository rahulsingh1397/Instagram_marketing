import os
import sys
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import List, Dict, Any
from pathlib import Path
import yaml

# Import OpenAI
from langchain_openai import ChatOpenAI

# Import tools
from instagram.tools.search import SearchTools

# Verify OpenAI API key is set
if not os.getenv('OPENAI_API_KEY'):
    print("[ERROR] OPENAI_API_KEY environment variable is not set")
    sys.exit(1)

@CrewBase
class InstagramCrew():
    """Instagram crew"""
    
    def __init__(self):
        super().__init__()
        self.agents_config = self.load_yaml_config('agents.yaml')
        try:
            self.tasks_config = self.load_yaml_config('tasks.yaml')
        except Exception as e:
            print(f"[ERROR] Failed to load tasks config: {e}")
            self.tasks_config = {}
        
        # Ensure OPENAI_API_KEY is set
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        # Get model configuration
        model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4-turbo-preview")
        organization = os.getenv("OPENAI_ORGANIZATION")
        project = os.getenv("OPENAI_PROJECT")
        
        print(f"[CREW_DEBUG] Initializing OpenAI model: {model_name}")
        print(f"[CREW_DEBUG] Organization: {organization}")
        print(f"[CREW_DEBUG] Project: {project}")
        
        try:
            # Initialize OpenAI with organization and project
            self.configured_llm = ChatOpenAI(
                model=model_name,
                temperature=0.7,
                api_key=openai_api_key,
                organization=organization,
                project=project
            )
            print(f"[CREW_DEBUG] Successfully initialized OpenAI model: {model_name}")
        except Exception as e:
            print(f"[CREW_ERROR] Failed to initialize OpenAI model: {e}")
            raise
            
        self.inputs = {}  # Initialize inputs dictionary
    
    def load_yaml_config(self, filename: str) -> Dict[str, Any]:
        """Load YAML configuration file."""
        config_path = Path(__file__).parent / 'config' / filename
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @agent
    def market_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['market_researcher'],
            tools=[
                SearchTools.search_internet,
                SearchTools.search_instagram,
                SearchTools.open_page
            ],
            llm=self.configured_llm  # Explicitly use Gemini
        )

    @agent
    def content_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['content_strategist'],
            llm=self.configured_llm
        )

    @agent
    def copy_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['copy_writer'],
            llm=self.configured_llm
        )

    @agent
    def visual_artist(self) -> Agent:
        return Agent(
            config=self.agents_config['visual_artist'],
            llm=self.configured_llm
        )

    def _create_task(self, task_name: str, context_tasks: list = None):
        """Helper method to create a task with the given name and context tasks."""
        task_config = dict(self.tasks_config[task_name])
        agent_name = task_config.pop('agent', None)
        context = task_config.pop('context', [])
        
        # If context_tasks is provided, use it; otherwise, use the context from the config
        final_context = context_tasks if context_tasks is not None else [getattr(self, t)() for t in context] if context else []
        
        agent_map = {
            'market_researcher': self.market_researcher(),
            'content_strategist': self.content_strategist(),
            'copy_writer': self.copy_writer(),
            'visual_artist': self.visual_artist()
        }
        
        # Get inputs passed to the crew
        inputs = getattr(self, 'inputs', {})
        
        # Replace placeholders in the task config
        from datetime import datetime
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_year = datetime.now().strftime("%Y")
        
        # Get topic and description from inputs or use defaults
        topic = inputs.get('topic_of_the_week', 'AI LLM and AI Art')
        instagram_description = inputs.get('instagram_description', 'AI LLM AI Art')
        
        replacements = {
            '{current date}': current_date,
            '{current year}': current_year,
            '{description}': instagram_description,  # Use the provided Instagram description
            '{instagram_description}': instagram_description,  # Use the provided Instagram description
            '{next_week_focus}': topic,  # Use the provided topic as the focus for next week
            '{topic}': topic,  # Use the provided topic
            '{topic_of_the_week}': topic  # Alias for topic
        }
        
        # Apply replacements to all string values in the task config
        for key, value in task_config.items():
            if isinstance(value, str):
                for placeholder, replacement in replacements.items():
                    value = value.replace(placeholder, str(replacement))
                task_config[key] = value
        
        # Remove any None values from task_config to avoid validation errors
        task_config = {k: v for k, v in task_config.items() if v is not None}
        
        return Task(
            config=task_config,
            agent=agent_map[agent_name],
            context=final_context if final_context else None  # Only pass context if it's not empty
        )

    def set_inputs(self, inputs):
        """Set the inputs for the crew."""
        self.inputs = inputs
        return self

    @task
    def market_research_task(self) -> Task:
        return self._create_task('market_research_task')

    @task
    def create_content_calendar_task(self) -> Task:
        return self._create_task('create_content_calendar_task', [self.market_research_task()])

    @task
    def copy_writing_task(self) -> Task:
        return self._create_task('copy_writing_task', [self.create_content_calendar_task()])

    @task
    def create_image_descriptions_task(self) -> Task:
        return self._create_task('create_image_descriptions_task', [self.copy_writing_task()])

    @task
    def compile_content_for_the_week_task(self) -> Task:
        return self._create_task('compile_content_for_the_week_task', [
            self.market_research_task(),
            self.create_content_calendar_task(),
            self.copy_writing_task(),
            self.create_image_descriptions_task()
        ])

    @crew
    def crew(self) -> Crew:
        """Creates the Instagram crew"""
        # Ensure all agents are using the Gemini LLM
        agents = [
            self.market_researcher(), 
            self.content_strategist(), 
            self.copy_writer(), 
            self.visual_artist()
        ]
        
        # Ensure all tasks are properly configured
        tasks = [
            self.market_research_task(), 
            self.create_content_calendar_task(), 
            self.copy_writing_task(), 
            self.create_image_descriptions_task(),
            self.compile_content_for_the_week_task()
        ]
        
        print("[CREW_DEBUG] Creating Crew with Gemini LLM")
        print(f"[CREW_DEBUG] Number of agents: {len(agents)}")
        print(f"[CREW_DEBUG] Number of tasks: {len(tasks)}")
        
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=2,
            memory=True,
            cache=True
        )