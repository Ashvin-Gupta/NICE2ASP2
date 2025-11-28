from groq import Groq
from openai import OpenAI
from anthropic import Anthropic
from src.resources.API_KEYS import API_KEYS

class LLMInferencer:
    def __init__(self, model, temperature, family, seed=42) -> None:

        self.model = model
        self.temperature = temperature
        self.seed = seed
        self.family = family
        if self.family == "claude":
            self.client = Anthropic(api_key=API_KEYS['ANTHROPIC_API_KEY'])
        
        elif self.family == 'gpt':
            self.client = OpenAI(api_key=API_KEYS['OPENAI_API_KEY'])
        elif self.family == 'deepseek':
            self.client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=API_KEYS['OPENROUTER_API_KEY'])
        elif self.family == 'groq':
            self.client = Groq(api_key=API_KEYS['GROQ_API_KEY'])

    
    def _load_file(self, filename) -> str:
        # Read in the contexts of a file as plain text
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                file_text = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file '{filename}' not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while reading the prompt file: {e}")
        
        return file_text


    def run_constant_inference(self, prompt_template:str, problem_text:str, output_file:str) -> None:
        # Run the prompt and extract the constants
        
        print("Extracting the constants")
        prompt_template = self._load_file(prompt_template)
        problem_text = self._load_file(problem_text)
        prompt = prompt_template.format(problem_text=problem_text)

        self._callAPI(prompt, output_file)
        
    def run_predicate_inference(self, prompt_template:str, problem_text:str, processed_constants:str, output_file:str) -> None:
        # Run the prompt and extract the predicates
        # Relies on constants already being found
        
        print("Extracting the predicates")
        prompt_template = self._load_file(prompt_template)
        problem_text = self._load_file(problem_text)
        processed_constants = self._load_file(processed_constants)
        prompt = prompt_template.format(problem_text=problem_text, processed_constants=processed_constants)
        self._callAPI(prompt, output_file)
    
    def run_rulegen_inference(self, prompt_template:str, problem_text:str, processed_constants:str, processed_predicates:str, output_file:str) -> None:
        # Run the prompt and extract the rules
        # Relies on the predicates and constants already being found
        
        print("Extracting the rules part 1")
        prompt_template = self._load_file(prompt_template)
        problem_text = self._load_file(problem_text)
        processed_constants = self._load_file(processed_constants)
        processed_predicates = self._load_file(processed_predicates)
        prompt = prompt_template.format(problem_text=problem_text, constants=processed_constants, predicates=processed_predicates)
        self._callAPI(prompt, output_file)
    
    def extract_atoms(self, prompt_template:str, rules:str, descriptions:str, output_file:str) -> None:
        # Run the prompt and verify whether the constants/predicates are within the text
        prompt_template = self._load_file(prompt_template)
        rules = self._load_file(rules)
        descriptions = self._load_file(descriptions)
        prompt = prompt_template.format(rules=rules, descriptions=descriptions)

        self._callAPI(prompt, output_file)
    
    def run_llm_only(self, prompt_template:str, guidelines:str, vignettes:str, output_file:str) -> None:
        # Run the prompt and return the actions suggested by the guidelines
        prompt_template = self._load_file(prompt_template)
        guidelines = self._load_file(guidelines)
        vignettes = self._load_file(vignettes)
        prompt = prompt_template.format(guidelines=guidelines, vignettes=vignettes)
        self._callAPI(prompt, output_file)



    def _callAPI(self, prompt:str, output_file:str) -> None:
        # encoding = tiktoken.encoding_for_model(self.model)
        # num_tokens = len(encoding.encode(prompt))
        # print(f'Number of tokens: {num_tokens}')
        

        if self.family == "claude":
            chat_completion = self.client.messages.create(
                model = self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature = self.temperature,
                max_tokens = 20000 if self.model == 'claude-3-7-sonnet-20250219' else 4096
            )
            if hasattr(chat_completion, 'content') and isinstance(chat_completion.content, list):
        
                # Extract text from TextBlock objects
                full_response = ""
                for block in chat_completion.content:
                    if hasattr(block, 'text'):
                        full_response += block.text
                    else:
                        # Fallback if the block doesn't have a text attribute
                        full_response += str(block)
        else:
            chat_completion = self.client.chat.completions.create(
                model = self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                    
                ],
                temperature = self.temperature,
                seed = self.seed,
                
            )
            full_response = chat_completion.choices[0].message.content

        self._save_reply(full_response, output_file)

     
    
    def _save_reply(self, reply:str, output_file:str) -> None:
        # Appends the LLM's reply to the output file
        
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(reply)
          
          
        
    