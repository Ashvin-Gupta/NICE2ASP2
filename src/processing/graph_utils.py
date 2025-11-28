import re
import networkx as nx
import matplotlib.pyplot as plt

class ASPGraphCreator:
    """Class for creating and visualizing ASP program graphs."""
    
    @staticmethod
    def create_program_graph(file_path):
        # Creates a directed graph from an ASP program with:
        # - Negation
        # - AND connections
        # - Choice rules with cardinality constraints
        # (Temporal dependencies have been removed)
        
        G = nx.DiGraph()
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        rules = [line.strip() for line in content.split('\n') 
                if line.strip() and not re.match(r'^\d+(\.\d+)*$', line.strip())]
        
        and_connections = set()
        
        for rule in rules:
            if not rule or rule.startswith('%'):
                continue
            
            if ':-' in rule:
                head, body = rule.split(':-')
            else:
                if rule.startswith(':-'):
                    head = None
                    body = rule[2:]
                else:
                    head = rule.rstrip('.')
                    body = None
            
            # Process head
            head_predicates = []
            if head:
                head = head.strip()
                choice_bounds = None
                
                # Check if this is a choice rule
                if '{' in head and '}' in head:
                    # Extract bounds and content
                    bounds_match = re.match(r'(\d+)\s*{(.*?)}\s*(\d+)', head)
                    if bounds_match:
                        lower_bound, choice_content, upper_bound = bounds_match.groups()
                        choice_bounds = (int(lower_bound), int(upper_bound))
                        head = choice_content.strip()
                
                # Split head into multiple predicates if they exist
                head_parts = [p.strip() for p in head.split(';')]
                
                for head_part in head_parts:
                    head_match = re.match(r'(\w+)\((.*?)\)', head_part)
                    if head_match:
                        pred, args = head_match.groups()
                        args_parts = [arg.strip(' "\'') for arg in args.split(',')]
                        # Remove time variable handling
                        head_predicates.append((pred, args_parts, None, choice_bounds))
            
            # Process body
            body_predicates = []
            if body:
                body_literals = []
                current_literal = ""
                paren_count = 0
                
                for char in body.rstrip('.'):
                    if char == ',' and paren_count == 0:
                        if current_literal.strip():
                            body_literals.append(current_literal.strip())
                        current_literal = ""
                    else:
                        if char == '(':
                            paren_count += 1
                        elif char == ')':
                            paren_count -= 1
                        current_literal += char
                
                if current_literal.strip():
                    body_literals.append(current_literal.strip())
                
                body_nodes = []
                for lit in body_literals:
                    # Skip time-related literals
                    if '=' in lit or lit.startswith('time('):
                        continue
                    
                    # Skip inequality checks which are typically time-related
                    inequality_match = re.match(r'(\w+)\s*([<>]=?)\s*(\w+)', lit)
                    if inequality_match:
                        continue
                    
                    is_negated = lit.startswith('not ')
                    if is_negated:
                        lit = lit.replace('not ', '').strip()
                    
                    lit_match = re.match(r'(\w+)\((.*?)\)', lit)
                    if lit_match:
                        pred, args = lit_match.groups()
                        args_parts = [arg.strip(' "\'') for arg in args.split(',')]
                        node_name = f"{pred}({', '.join(args_parts)})"
                        body_nodes.append(node_name)
                        body_predicates.append((pred, args_parts, None, is_negated))
                
                # Create AND connections between body predicates
                for i in range(len(body_nodes)):
                    for j in range(i + 1, len(body_nodes)):
                        and_connections.add((body_nodes[i], body_nodes[j]))
            
            # Create nodes and edges
            if head_predicates:
                # If this is a choice rule with multiple predicates, create a choice node
                if any(bounds for _, _, _, bounds in head_predicates) and len(head_predicates) > 1:
                    bounds = head_predicates[0][3]  # Get bounds from first predicate
                    choice_node = f"choice_{bounds[0]}_{bounds[1]}"
                    G.add_node(choice_node, 
                              node_type='choice',
                              lower_bound=bounds[0],
                              upper_bound=bounds[1])
                    
                    # Connect choice node to all predicates in the choice rule
                    for head_pred, head_args, _, _ in head_predicates:
                        head_node = f"{head_pred}({', '.join(head_args)})"
                        G.add_node(head_node)
                        G.add_edge(choice_node, head_node, 
                                 connection_type='choice',
                                 temporal=False)
                        
                        # Connect body predicates to the choice node
                        for body_pred, body_args, _, is_negated in body_predicates:
                            body_node = f"{body_pred}({', '.join(body_args)})"
                            G.add_node(body_node)
                            G.add_edge(body_node, choice_node, 
                                     negated=is_negated,
                                     temporal=False)
                
                else:
                    # Regular rules (non-choice)
                    for head_pred, head_args, _, _ in head_predicates:
                        head_node = f"{head_pred}({', '.join(head_args)})"
                        G.add_node(head_node)
                        
                        for body_pred, body_args, _, is_negated in body_predicates:
                            body_node = f"{body_pred}({', '.join(body_args)})"
                            G.add_node(body_node)
                            G.add_edge(body_node, head_node, 
                                     negated=is_negated,
                                     temporal=False)
        
        # Add AND connections to the graph
        for node1, node2 in and_connections:
            G.add_edge(node1, node2, connection_type='and')
            G.add_edge(node2, node1, connection_type='and')
        
        return G
    
    @staticmethod
    def visualize_graph(G, layout_type='planar'):
        # Visualizes the ASP program graph with different layout options:
        # - planar: Attempts planar layout
        # - circular: Circular layout
        # - kamada_kawai: Force-directed layout that tries to minimize edge crossings
        # - multipartite: Layered layout based on node depths
        # - spring: Original spring layout (as backup)
        
        plt.figure(figsize=(20, 20))
        
        # Choose layout algorithm
        try:
            if layout_type == 'planar':
                # First check if graph is planar
                if nx.check_planarity(G)[0]:
                    pos = nx.planar_layout(G)
                else:
                    print("Graph is not planar, falling back to Kamada-Kawai layout")
                    pos = nx.kamada_kawai_layout(G)
            elif layout_type == 'circular':
                pos = nx.circular_layout(G)
            elif layout_type == 'kamada_kawai':
                pos = nx.kamada_kawai_layout(G)
            elif layout_type == 'multipartite':
                # Group nodes by their depth in the graph
                depths = {}
                for node in G.nodes():
                    if G.in_degree(node) == 0:  # Root nodes
                        depths[node] = 0
                    else:
                        # Find maximum depth of predecessors + 1
                        pred_depths = [depths[pred] for pred in G.predecessors(node) if pred in depths]
                        depths[node] = max(pred_depths) + 1 if pred_depths else 0
                
                # Create layers for multipartite layout
                layers = {}
                for node, depth in depths.items():
                    if depth not in layers:
                        layers[depth] = []
                    layers[depth].append(node)
                
                # Convert to format needed by multipartite_layout
                subset_sizes = [len(nodes) for depth, nodes in sorted(layers.items())]
                node_indices = {}
                idx = 0
                for depth, nodes in sorted(layers.items()):
                    for node in nodes:
                        node_indices[node] = idx
                        idx += 1
                
                pos = nx.multipartite_layout(G, subset_sizes=subset_sizes, 
                                           node_indices=node_indices)
            else:
                pos = nx.spring_layout(G, k=2, iterations=50)
                
        except Exception as e:
            print(f"Layout error: {e}. Falling back to spring layout.")
            pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Separate nodes by type
        regular_nodes = [n for n, d in G.nodes(data=True) if not d.get('node_type') == 'choice']
        choice_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'choice']
        
        # Draw regular nodes
        nx.draw(G, pos, nodelist=regular_nodes, 
                              node_color='lightblue', node_size=2000)
        
        # Draw choice nodes as diamonds
        if choice_nodes:
            nx.draw_networkx_nodes(G, pos, nodelist=choice_nodes,
                                  node_color='lightgreen', node_shape='d', node_size=1500)
        
        # Separate edges by type
        regular_edges = [(u, v) for (u, v, d) in G.edges(data=True) 
                         if not d.get('negated') 
                         and not d.get('connection_type')]
        negated_edges = [(u, v) for (u, v, d) in G.edges(data=True) 
                         if d.get('negated')]
        choice_edges = [(u, v) for (u, v, d) in G.edges(data=True) 
                        if d.get('connection_type') == 'choice']
        and_edges = [(u, v) for (u, v, d) in G.edges(data=True) 
                     if d.get('connection_type') == 'and']
        
        # Draw different types of edges
        nx.draw_networkx_edges(G, pos, edgelist=regular_edges, edge_color='gray',
                              arrows=True, arrowsize=30, width=3)
        nx.draw_networkx_edges(G, pos, edgelist=negated_edges, edge_color='red',
                              arrows=True, arrowsize=30, width=3)
        nx.draw_networkx_edges(G, pos, edgelist=choice_edges, edge_color='green',
                              arrows=True, arrowsize=30, width=3, style=(0, (5, 5)))
        nx.draw_networkx_edges(G, pos, edgelist=and_edges, edge_color='purple',
                              arrows=False, width=2)
        
        # Add edge labels for temporal relationships and AND connections
        edge_labels = {}
        for u, v, d in G.edges(data=True):
            if d.get('connection_type') == 'and':
                edge_labels[(u, v)] = 'AND'
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)
        
        # Draw node labels
        labels = {}
        for node in G.nodes():
            if node.startswith('choice'):
                bounds = G.nodes[node]
                lower = bounds['lower_bound']
                upper = bounds['upper_bound']
                labels[node] = f'Choice\n{lower}-{upper}'
            else:
                labels[node] = '\n'.join([node[i:i+20] for i in range(0, len(node), 20)])
        nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
        
        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], color='gray', label='Regular Dependency'),
            plt.Line2D([0], [0], color='red', label='Negated Dependency'),
            plt.Line2D([0], [0], color='green', linestyle='--', dashes=(5, 5), 
                      label='Choice Rule'),
            plt.Line2D([0], [0], color='purple', label='AND Connection'),
            plt.Line2D([0], [0], marker='d', color='lightgreen', label='Choice Node',
                      markersize=10, linestyle='none')
        ]
        plt.legend(handles=legend_elements, loc='upper right')
        
        plt.title("ASP Program Graph")
        plt.axis('off')
        plt.tight_layout()
        plt.show()