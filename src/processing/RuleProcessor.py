import re
from pathlib import Path
from typing import Dict, List, Tuple
import os
import subprocess
import tempfile
from src.processing.ASPRuleParser import ASPRuleParser
from src.processing.FileManager import FileManager


class RuleProcessor:
    """Processes LLM-generated ASP rules and adds fired() tracking."""
    
    def __init__(self, guideline_path: str):
        self.file_manager = FileManager()
        self.parser = ASPRuleParser()
        self.rule_registry: Dict[str, str] = {}  # Maps rule_id to rule text
        self.guideline_text = self._build_guideline_lookup(guideline_path) if guideline_path else {}
        self.constraint_rules = {}  # Maps constraint rule_id to body
    
    def _build_guideline_lookup(self, guideline_path: str) -> dict[str, str]:

        text = self.file_manager.load_file(guideline_path)
        lookup: Dict[str, str] = {}
        current_rule_id = None
        current_rule_lines: List[str] = []
        section_context: List[str] = []  # active context block for the section
        context_active = False  # whether we're currently collecting a context block

        def flush_rule():
            nonlocal current_rule_id, current_rule_lines, lookup
            if current_rule_id and current_rule_lines:
                ctx_len = 0
                # match prefix of rule lines with section_context
                for i in range(min(len(section_context), len(current_rule_lines))):
                    if current_rule_lines[i] == section_context[i]:
                        ctx_len += 1
                    else:
                        break

                context_block = current_rule_lines[:ctx_len]
                rule_block = current_rule_lines[ctx_len:]

                # Format output: context on its own lines, blank line, then rule text.
                formatted = ""
                if context_block:
                    formatted += "\n".join(context_block)
                    # Add a newline separator between context and rule if both exist
                    if rule_block:
                        formatted += "\n\n"
                
                formatted += "\n".join(rule_block)

                lookup[current_rule_id] = formatted.strip()

            current_rule_id = None
            current_rule_lines = []

        lines = text.splitlines()
        for raw in lines:
            line = raw.rstrip()
            stripped = line.strip()

            # detect numbered token at start
            m = re.match(r'^(\d+(?:\.\d+)*)\b', stripped)
            if m:
                num = m.group(1)
                dot_count = num.count(".")
                # treat as a rule only if dot_count >= 2 (e.g., 1.1.1)
                if dot_count >= 2:
                    # start a new rule: flush previous
                    flush_rule()
                    current_rule_id = num
                    # build content: start with a COPY of active context if any
                    current_rule_lines = section_context.copy() if section_context else []
                    # attach the rest of the line after the number
                    rest = stripped[len(num):].strip(" .-")
                    if rest:
                        current_rule_lines.append(rest)
                    # now collect rule continuation lines or bullets until next rule/blank/header
                    continue
                else:
                    # section header like "1.1 Diagnosis" -> reset context
                    flush_rule()
                    section_context = []
                    context_active = False
                    continue

            # bullet lines - attach to current rule if exists, otherwise treat as context line
            if stripped.startswith("•") or stripped.startswith("-"):
                if current_rule_id:
                    current_rule_lines.append(stripped)
                else:
                    if not context_active:
                        section_context = [stripped]
                        context_active = True
                    else:
                        section_context.append(stripped)
                continue

            # blank line -> end current rule and mark context inactive so next text starts a new context
            if stripped == "":
                flush_rule()
                context_active = False
                continue

            # continuation of a rule
            if current_rule_id:
                current_rule_lines.append(stripped)
                continue

            # otherwise it's context text before rules in the section
            if not context_active:
                # start a new context block (replace previous)
                section_context = [stripped]
                context_active = True
            else:
                # append to existing context block
                section_context.append(stripped)

        # final flush
        flush_rule()
        return lookup
    
    def _constraint_to_rule(self, body: str) -> str:
        literals = [lit.strip() for lit in body.split(',') if lit.strip()]
        if not literals:
            return "Not (condition)."
        head = literals[0]
        tail = ', '.join(literals[1:]) if len(literals) > 1 else ""
        neg_head = head[4:].strip() if head.startswith('not ') else f'Not {head}'
        if tail:
            return f"{neg_head} if {tail}."
        return f"{neg_head}."
    
    
    def append_fired_rules(self, input_path: str, output_path: str) -> None:
        """
        Process rulegen_response.txt and add fired() tracking rules.
        
        Args:
            input_path: Path to rulegen_response.txt
            output_path: Path to output .lp file
        """
        content = self.file_manager.load_file(input_path)
        lines = content.split('\n')
        
        output_lines = []
        current_rule_number = None
        rule_counter = {}  # Track how many rules per rule number
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Check for rule number marker [X.X.X]
            rule_match = re.match(r'\[([\d.]+)\]', line)
            if rule_match:
                current_rule_number = rule_match.group(1)
                # Reset counter for this rule number
                rule_counter[current_rule_number] = 0
                # Comment out the rule number line
                output_lines.append(f"% {line}")
                i += 1
                continue
            
            # Check if this is a rule line (contains :- or starts with :-)
            if line and (':-' in line or line.startswith(':-')):
                # Determine rule ID
                if current_rule_number:
                    # Check if we've seen this rule number before
                    if current_rule_number not in rule_counter:
                        rule_counter[current_rule_number] = 0
                    
                    rule_counter[current_rule_number] += 1
                    count = rule_counter[current_rule_number]
                    
                    # Create rule ID with suffix if multiple rules
                    if count == 1:
                        rule_id = current_rule_number
                    else:
                        # Convert count to letter (A, B, C, etc.)
                        suffix = chr(ord('B') + count - 2)
                        rule_id = f"{current_rule_number}_{suffix}"
                else:
                    # No rule number, use a generic ID
                    rule_id = f"unnamed_{len(self.rule_registry) + 1}"
                
                # Store the rule in registry
                self.rule_registry[rule_id] = line.rstrip('.')
                
                # Add original rule
                output_lines.append(line)
                
                # Extract body for fired() rule
                body = self._extract_body(line)

                if line.startswith(':-'):
                    output_lines.append(f'fired("{rule_id}").') 
                    support_atom = f'constraint_ok("{rule_id}")'
                    output_lines.append(f'{support_atom}.')
                    
                    self.constraint_rules[rule_id] = body   
                else:
                    if body:
                        output_lines.append(f'fired("{rule_id}") :- {body}.')
                    else:
                        output_lines.append(f'fired("{rule_id}").')
                
                
                i += 1
            else:
                # Empty line or non-rule line, preserve as-is
                if not line and i < len(lines) - 1:
                    # Only add empty line if not at the end
                    output_lines.append("")
                elif line:
                    output_lines.append(line)
                i += 1
        
        # Add #show directive at the end
        output_lines.append("")
        output_lines.append("#show fired/1.")
        output_lines.append("#show constraint_ok/1.")
        
        # Write output
        output_content = '\n'.join(output_lines)
        self.file_manager.save_file(output_content, output_path)
        
        print(f"Processed {len(self.rule_registry)} rules")
        print(f"Output written to {output_path}")
    
    def _extract_body(self, rule_line: str) -> str:
        """
        Extract the body part of a rule (everything after :-).
        
        Args:
            rule_line: The ASP rule line
            
        Returns:
            The body part, or empty string for facts
        """
        rule_line = rule_line.strip()
        
        # Handle constraint rules (start with :-)
        if rule_line.startswith(':-'):
            body = rule_line[2:].strip().rstrip('.')
            return body
        
        # Regular rule with head and body
        if ':-' in rule_line:
            parts = rule_line.split(':-', 1)
            body = parts[1].strip().rstrip('.')
            return body
        
        # Fact rule (no body) - return empty body
        return ""
    
    def explain_fired_rules(self, lp_file_path: str, clingo_output_path: str, explanation_path: str) -> None:
        """
        Parse clingo output and generate natural language explanations for each patient.
        
        Args:
            lp_file_path: Path to the .lp file with fired rules
            clingo_output_path: Path to clingo output file
            explanation_path: Path to write explanations
        """
        # Load the .lp file and build a rule registry
        lp_content = self.file_manager.load_file(lp_file_path)
        rule_map = self._build_rule_map_from_lp(lp_content)
        
        # Load clingo output
        clingo_output = self.file_manager.load_file(clingo_output_path)
        
        # Split by patient sections
        patient_sections = re.split(r'=== Patient (\d+) ===', clingo_output)[1:]
        
        if not patient_sections:
            explanation = "No patient results found.\n"
            self.file_manager.save_file(explanation, explanation_path)
            print("No patient results found in clingo output")
            return
        
        # Group patient IDs with their outputs (they alternate in the split result)
        patient_data = [(patient_sections[i], patient_sections[i+1]) for i in range(0, len(patient_sections), 2)]
        
        # Generate explanations
        explanations = []
        explanations.append("=" * 80 + "\n")
        explanations.append("FIRED RULES EXPLANATIONS BY PATIENT\n")
        explanations.append("=" * 80 + "\n\n")
        
        for patient_id, output in patient_data:
            explanations.append(f"{'='*80}\n")
            explanations.append(f"PATIENT {patient_id}\n")
            explanations.append(f"{'='*80}\n\n")
            
            # Extract all answer sets for this patient
            answer_sets = re.findall(r'Answer: (\d+)\n([^\n]+)', output)
            
            if not answer_sets:
                explanations.append("No rules fired for this patient.\n\n")
                continue
            
            # Process each answer set
            for answer_num, answer_line in answer_sets:
                # Extract fired rule IDs from this answer set
                fired_ids = re.findall(r'fired\("([^"]+)"\)', answer_line)
                
                explanations.append(f"Answer Set {answer_num}: ({len(fired_ids)} rules fired)\n")
                explanations.append("-" * 80 + "\n\n")
                
                # Explain each fired rule
                for rule_id in fired_ids:
                    if rule_id in rule_map:
                        rule_text = rule_map[rule_id]

                        constraint_body = self.constraint_rules.get(rule_id)
                        print(f"Constraint body: {constraint_body}")
                        if constraint_body:
                            explanations.append("NICE2ASP:\n")
                            explanations.append(f"Rule {rule_id}\n")
                            explanations.append("Constraint satisfied:\n")
                            explanations.append(f"{self._constraint_to_rule(constraint_body)}\n\n")

                            base_rule_id = rule_id.split('_')[0]
                            original_text = self.guideline_text.get(base_rule_id)
                            if original_text:
                                explanations.append(f"Guideline {base_rule_id} Natural Language:\n{original_text}\n\n")
                            continue  
                        explanation = self.parser.explain_rule(rule_text, rule_id)

                        explanations.append(f"{explanation}\n")

                        # Add the original guideline text for the rule
                        base_rule_id = rule_id.split('_')[0]
                        original_text = self.guideline_text.get(base_rule_id)
                        if original_text:
                            explanations.append(f"Guideline {base_rule_id} Natural Language: \n{original_text}\n\n")
                    else:
                        explanations.append(f"Rule {rule_id}: [Rule not found]\n\n")
                
                explanations.append("\n")
            
            explanations.append("\n")
        
        explanation_text = ''.join(explanations)
        self.file_manager.save_file(explanation_text, explanation_path)
        print(f"Explanations written to {explanation_path}")

    def _build_rule_map_from_lp(self, lp_content: str) -> dict:
        """
        Build a mapping of rule_id to rule_text from the .lp file.
        Looks for patterns where fired("rule_id") follows the actual rule.
        
        Args:
            lp_content: Content of the .lp file
            
        Returns:
            Dictionary mapping rule_id to rule text
        """
        rule_map = {}
        lines = lp_content.split('\n')
        
        for i in range(len(lines) - 1):
            line = lines[i].strip()
            next_line = lines[i + 1].strip()
            
            # Check if next line is a fired() rule
            fired_match = re.match(r'fired\("([^"]+)"\)', next_line)
            if fired_match and line and not line.startswith('%') and ':-' in line:
                rule_id = fired_match.group(1)
                rule_map[rule_id] = line.rstrip('.')
        
        return rule_map
    
    def run_clingo_for_patients(self, lp_file_path: str, atoms_file_path: str, output_file_path: str, debug_id: int = None) -> dict:
        """
        For each patient in the atoms file:
        1. Extract patient facts from the atoms file
        2. Append the facts to the .lp file (rulegen_response_fired.lp)
        3. Run clingo on the combined file
        4. Record the output
        
        Args:
            lp_file_path (str): Path to the ASP logic program (.lp file with fired rules)
            atoms_file_path (str): Path to the atoms file with patient facts
            output_file_path (str, optional): Path to save the results. If None, results are only printed.
        
        Returns:
            dict: Dictionary mapping patient IDs to clingo outputs
        """
        
        # Read the original .lp file content
        with open(lp_file_path, 'r', encoding='utf-8') as f:
            lp_content = f.read()
        
        # Read the atoms file
        with open(atoms_file_path, 'r', encoding='utf-8') as f:
            atoms_content = f.read()
        
        # Dictionary to store results
        results = {}
        
        # Split the content into patient sections using **Patient N:**
        patient_sections = re.split(r'(?:\*\*)?Patient\s+(\d+):?(?:\*\*)?', atoms_content)[1:]
        
        # Group patient IDs with their sections (they alternate in the split result)
        patient_data = [(patient_sections[i], patient_sections[i+1]) for i in range(0, len(patient_sections), 2)]
        
        # Process each patient
        for patient_id, section in patient_data:
            print(f"Processing Patient {patient_id}...")
            
            # Extract facts from the section
            facts = []
            for line in section.strip().split('\n'):
                line = line.strip()
                # Skip empty lines, comments, and lines that don't look like facts
                if line and not line.startswith('%') and not line.startswith('**') and '(' in line:
                    facts.append(line)
            
            # Create a temporary file with the combined content
            with tempfile.NamedTemporaryFile(mode='w', suffix='.lp', delete=False, encoding='utf-8') as temp_file:
                temp_file_path = temp_file.name
                # Write original .lp content
                temp_file.write(lp_content)
                # Add a newline if needed
                if not lp_content.endswith('\n'):
                    temp_file.write('\n')
                # Add a comment for patient
                temp_file.write(f'\n% Patient {patient_id} facts\n')
                # Write patient facts
                temp_file.write('\n'.join(facts) + '\n')
            
            if int(patient_id) == debug_id:
                
                debug_file_path = os.path.join(os.path.dirname(lp_file_path), f'debug_patient_{patient_id}.lp')
                with open(temp_file_path, 'r', encoding='utf-8') as src:
                    debug_content = src.read()
                with open(debug_file_path, 'w', encoding='utf-8') as dst:
                    dst.write(debug_content)
                print(f"  *** DEBUG: Saved combined file to {debug_file_path} ***")
            
            try:
                # Run clingo on the temporary file
                result = subprocess.run(
                    ['clingo', '--warn=no-atom-undefined', temp_file_path, '0'],
                    capture_output=True, 
                    text=True,
                    check=False
                )
                
                # Store the output
                results[patient_id] = result.stdout
                
                # Print summary
                fired_count = result.stdout.count('fired(')
                print(f"Patient {patient_id}: {fired_count} rules fired")
                
            except Exception as e:
                # Handle errors
                results[patient_id] = f"ERROR: {str(e)}"
                print(f"Error running clingo for Patient {patient_id}: {str(e)}")
            finally:
                # Clean up the temporary file
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
        
        # Save results to file if requested
        if output_file_path:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                for patient_id in sorted(results.keys(), key=int):
                    f.write(f"=== Patient {patient_id} ===\n")
                    f.write(results[patient_id])
                    f.write("\n" + "=" * 80 + "\n\n")
            print(f"\nResults saved to {output_file_path}")
        
        return results

