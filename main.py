import os
import re
import yaml
import tempfile
from pathlib import Path
from src.processing.LLM_Inferencer import LLMInferencer
from src.processing.FileManager import FileManager
from src.processing.RuleProcessor import RuleProcessor
from src.processing.graph_analysis import GraphAnalyzer
from src.processing.graph_utils import ASPGraphCreator

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def setup_experiment_dir(config):
    # Create experiment output directory
    base_output_dir = Path(config['experiment']['output_dir'])
    cancer_type = config['experiment']['cancer_type']
    exp_dir = base_output_dir / cancer_type
    exp_dir.mkdir(parents=True, exist_ok=True)
    
    config_copy_path = exp_dir / 'config.yaml'
    with open('src/configs/config.yaml', 'r') as src, open(config_copy_path, 'w') as dst:
        lines = src.readlines()[:24]
        dst.writelines(lines)

    return exp_dir

def main():
    print('Running Data to Knowledge Pipeline!')
    
    # Load configuration
    config = load_config('src/configs/config.yaml')
    exp_dir = setup_experiment_dir(config)
    
    # Setup output file paths
    output_files = {
        'constant_response': exp_dir / 'constant_response.txt',
        # 'processed_constants': exp_dir / 'constant_processed.txt',
        'predicate_response': exp_dir / 'predicate_response.txt',
        # 'processed_predicates': exp_dir / 'predicate_processed.txt',
        'rulegen_response': exp_dir / 'rulegen_response.txt',

        'rulegen_response_fired': exp_dir / 'rulegen_response_fired.lp',
        'atoms': exp_dir / 'atoms.txt',
        'clingo_output': exp_dir / 'clingo_output.txt',
        'explanation': exp_dir / 'explanation.txt',

        # Baseline responses
        'llm_only_response': exp_dir / 'llm_only_response.txt',
        'in_context_response': exp_dir / 'in_context_response.txt',
        'zero_shot_response': exp_dir / 'zero_shot_response.txt',

        'graph_metrics': exp_dir / 'graph_metrics.csv',
    }

    llmExtractor = LLMInferencer(config['experiment']['model'], config['experiment']['temperature'], config['experiment']['family'])
    fileManager = FileManager()

    # ------------------------------------------------------------
    # D2K-Pipeline
    # ------------------------------------------------------------

    if config['experiment']['version'] == 'D2K-Pipeline':
        # Constant extraction
        llmExtractor.run_constant_inference(
            config['input_files']['constant_prompt'],
            config['input_files']['problem_text'],
            str(output_files['constant_response']),
        )

        # Extracting the predicates
        llmExtractor.run_predicate_inference(
            config['input_files']['predicate_prompt'],
            config['input_files']['problem_text'],
            str(output_files['constant_response']),
            str(output_files['predicate_response']),
        )

        # Rule generation
        llmExtractor.run_rulegen_inference(
            config['input_files']['rule_generation_prompt'],
            config['input_files']['problem_text'],
            str(output_files['constant_response']),
            str(output_files['predicate_response']),
            str(output_files['rulegen_response']),
        )

        graph_generated = ASPGraphCreator.create_program_graph(str(output_files['rulegen_response']))
        pass
    elif config['experiment']['version'] == 'In-Context':
        print("Running in context inference")
        llmExtractor.run_constant_inference(
            config['input_files']['in_context_prompt'],
            config['input_files']['problem_text'],
            str(output_files['in_context_response'])
        )
        graph_generated = ASPGraphCreator.create_program_graph(str(output_files['in_context_response']))
        pass
    elif config['experiment']['version'] == 'No-Pipeline':
        print("Running zero shot inference")
        llmExtractor.run_constant_inference(
            config['input_files']['zero_shot_prompt'],
            config['input_files']['problem_text'],
            str(output_files['zero_shot_response'])
        )
        graph_generated = ASPGraphCreator.create_program_graph(str(output_files['zero_shot_response']))
        pass
    else:
        print("Invalid experiment version")
        return

    # Graphical Analysis:
    graph_gt = ASPGraphCreator.create_program_graph(config['input_files']['ground_truth'])

    if config['experiment']['version'] == 'D2K-Pipeline':
        graph_file = str(output_files['rulegen_response'])
        graph_name = 'rulegen_response'
    elif config['experiment']['version'] == 'No-Pipeline':
        graph_file = str(output_files['zero_shot_response'])
        graph_name = 'zero_shot_response'
    elif config['experiment']['version'] == 'In-Context':
        graph_file = str(output_files['in_context_response'])
        graph_name = 'in_context_response'
    else:
        print(f"Unknown experiment version: {config['experiment']['version']}")
        return

    # ------------------------------------------------------------
    # Graphical Analysis
    # ------------------------------------------------------------
    graph_generated = ASPGraphCreator.create_program_graph(graph_file)
    graph_analyzer = GraphAnalyzer()
    graph_analyzer.calculate_graph_similarity(
        graph_gt, 
        [graph_generated], 
        str(output_files['graph_metrics']), 
        [graph_name],
        config=config
    )

    # ------------------------------------------------------------
    # K2P Analysis
    # ------------------------------------------------------------

    # Run the LLM only prompt BASELINE
    # llmExtractor.run_llm_only(config['input_files']['llm_only_prompt'], config['input_files']['problem_text'], config['input_files']['patient_vignettes'], str(output_files['llm_only_response']))
    
    # print("Starting K2P Analysis")
    # ruleProcessor = RuleProcessor(config['input_files']['problem_text'])

    # Add fired({rule number}) to the rules
    # ruleProcessor.append_fired_rules(str(output_files['rulegen_response']), str(output_files['rulegen_response_fired']))

    # Extract the atoms in patient vignettes from the rules generated by the program
    # llmExtractor.extract_atoms(
    #     prompt_template=config['input_files']['extract_atoms'], 
    #     rules=str(output_files['rulegen_response']), 
    #     descriptions=config['input_files']['patient_vignettes'], 
    #     output_file=str(output_files['atoms'])
    #     )

    # # Run clingo for each patient vignette
    # ruleProcessor.run_clingo_for_patients(str(output_files['rulegen_response_fired']), str(output_files['atoms']), str(output_files['clingo_output']), debug_id=1)

    # Explain the clingo output
    # ruleProcessor.explain_fired_rules(str(output_files['rulegen_response_fired']), str(output_files['clingo_output']), str(output_files['explanation']))


if __name__ == '__main__':
    main()