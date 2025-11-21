import re
from typing import List, Tuple, Optional


class ASPRuleParser:
    """Parser for ASP rules to generate natural language explanations."""
    
    def __init__(self):
        pass
    
    def parse_rule(self, rule_text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Parse an ASP rule into head and body components.
        
        Args:
            rule_text: The ASP rule as a string
            
        Returns:
            Tuple of (head, body) or (None, body) for constraints
        """
        rule_text = rule_text.strip()
        
        # Handle constraint rules (start with :-)
        if rule_text.startswith(':-'):
            body = rule_text[2:].strip().rstrip('.')
            return (None, body)
        
        # Split on :- to separate head and body
        if ':-' in rule_text:
            parts = rule_text.split(':-', 1)
            head = parts[0].strip()
            body = parts[1].strip().rstrip('.')
            return (head, body)
        else:
            # Fact rule (no body)
            return (rule_text.rstrip('.'), None)
    
    def parse_choice_expression(self, text: str) -> Optional[Tuple[int, int, List[str]]]:
        """
        Parse choice expression like 1{offer("A"); offer("B")}2
        
        Returns:
            Tuple of (min, max, list_of_options) or None if not a choice
        """
        pattern = r'(\d+)\{([^}]+)\}(\d+)'
        match = re.search(pattern, text)
        if match:
            min_val = int(match.group(1))
            options_str = match.group(2)
            max_val = int(match.group(3))
            # Split options by semicolon
            options = [opt.strip() for opt in options_str.split(';')]
            return (min_val, max_val, options)
        return None
    
    def parse_body_conditions(self, body: str) -> List[str]:
        """
        Parse body conditions, handling commas, not, and choice expressions.
        
        Returns:
            List of condition strings
        """
        if not body:
            return []
        
        conditions = []
        # Split by comma, but be careful with nested structures
        # Simple approach: split by comma that's not inside quotes or parentheses
        parts = []
        current = ""
        paren_depth = 0
        quote_char = None
        
        for char in body:
            if char in ['"', "'"] and (not quote_char or quote_char == char):
                if quote_char == char:
                    quote_char = None
                else:
                    quote_char = char
                current += char
            elif quote_char:
                current += char
            elif char == '(':
                paren_depth += 1
                current += char
            elif char == ')':
                paren_depth -= 1
                current += char
            elif char == ',' and paren_depth == 0:
                if current.strip():
                    parts.append(current.strip())
                current = ""
            else:
                current += char
        
        if current.strip():
            parts.append(current.strip())
        
        return parts
    
    def explain_condition(self, condition: str) -> str:
        """
        Convert a single condition to natural language.
        """
        condition = condition.strip()
        
        # Handle not
        if condition.startswith('not '):
            inner = condition[4:].strip()
            return f"not {self.explain_condition(inner)}"
        
        # Handle choice expressions in body
        choice = self.parse_choice_expression(condition)
        if choice:
            min_val, max_val, options = choice
            explained_options = [self.explain_condition(opt) for opt in options]
            if min_val == max_val:
                return f"exactly {min_val} of: {', '.join(explained_options)}"
            else:
                return f"at least {min_val} and at most {max_val} of: {', '.join(explained_options)}"
        
        return condition
    
    def explain_head(self, head: str) -> str:
        """
        Convert rule head to natural language.
        """
        if not head:
            return ""
        
        head = head.strip()
        
        # Handle choice expressions in head
        choice = self.parse_choice_expression(head)
        if choice:
            min_val, max_val, options = choice
            explained_options = [self.explain_condition(opt) for opt in options]
            if min_val == max_val:
                return f"choose exactly {min_val} of: {', '.join(explained_options)}"
            else:
                return f"choose at least {min_val} and at most {max_val} of: {', '.join(explained_options)}"
        
        # Default: return as-is
        return head
    
    def explain_rule(self, rule_text: str, rule_id: str = "") -> str:
        """
        Generate natural language explanation of an ASP rule.
        
        Args:
            rule_text: The ASP rule as a string
            rule_id: The rule identifier (e.g., "1.1.14_A")
            
        Returns:
            Natural language explanation
        """
        head, body = self.parse_rule(rule_text)

        conditions = self.parse_body_conditions(body)

        explained_conditions = []
        i = 0
        while i < len(conditions):
            current = conditions[i]
            next_condition = conditions[i + 1] if i + 1 < len(conditions) else None

            if next_condition:
                var_match = re.match(r'(\w+)\(([^)]+)\)', current)
                comp_match = re.match(r'(\w+)(>=|<=|>|<|==|!=)(\d+)', next_condition)

                if var_match and comp_match and var_match.group(2) == comp_match.group(1):
                    var_name = var_match.group(1)
                    comp_op = comp_match.group(2)
                    comp_val = comp_match.group(3)

                    if var_name.lower() == "age":
                        explained_conditions.append(f"age {comp_op} {comp_val}")
                        i += 2
                        continue

            explained_conditions.append(self.explain_condition(current))
            i += 1
        
        # Handle constraints
        if head is None:
            conditions_str = " and ".join(explained_conditions)
            prefix = f"{'.' * 80}\nNICE2ASP:\nRule {rule_id}: " if rule_id else "Constraint: "
            return f"{prefix}\nCurrent Patient Features: {conditions_str},\nConstraint: The following conditions cannot all be true."
        
        # Handle facts (no body)
        if body is None:
            explained_head = self.explain_head(head)
            prefix = f"{'.' * 80}\nNICE2ASP:\nRule {rule_id}: " if rule_id else "Fact: "
            return f"{prefix}\nCurrent Patient Features: \n{conditions_str},\nAction: \n{explained_head}.\n"
        
        # Regular rule
        conditions_str = " and ".join(explained_conditions)
        explained_head = self.explain_head(head)
        
        prefix = f"{'.' * 80}\nNICE2ASP:\nRule {rule_id}: " if rule_id else "Rule: "
        return f"{prefix}\nCurrent Patient Features: \n{conditions_str},\nAction: \n{explained_head}.\n"

