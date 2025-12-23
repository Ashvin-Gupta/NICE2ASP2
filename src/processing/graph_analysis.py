import re
import numpy as np
import networkx as nx
from grakel import Graph, WeisfeilerLehmanOptimalAssignment
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import ot
import csv
import os

class GraphAnalyzer:
    # Class for analyzing and comparing ASP program graphs
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    
    def create_node_embeddings(self, G):
            # Create embeddings for each node in a simpler format

            nodes = list(G.nodes())
            node_to_idx = {node: i for i, node in enumerate(nodes)}
            
            # Create embeddings for each node
            embeddings = {}
            for node in nodes:
                # Extract predicate name and arguments
                match = re.match(r'(\w+)\((.*?)\)', str(node))
                if match:
                    pred_name, args = match.groups()
                    text = f"Predicate {pred_name} with arguments {args}"
                else:
                    # Handle special nodes like choice nodes
                    if G.nodes[node].get('node_type') == 'choice':
                        bounds = G.nodes[node]
                        lower = bounds.get('lower_bound', 0)
                        upper = bounds.get('upper_bound', 0)
                        text = f"Choice rule with bounds {lower}-{upper}"
                    else:
                        text = str(node)
                
                embeddings[node] = self.model.encode(text)
            
            return embeddings, nodes, node_to_idx
    
    def create_semantic_adjacency_matrices(self, G, embeddings, nodes, node_to_idx):
            # Create semantic adjacency matrices for each edge type

            edge_types = ['regular', 'negated', 'choice', 'and']

            n = len(nodes)
            embedding_dim = len(next(iter(embeddings.values())))
            
            # Initialize matrices for each edge type
            matrices = {edge_type: np.zeros((n, n, embedding_dim * 2)) for edge_type in edge_types}
            
            # Fill matrices with semantic information
            for u, v, data in G.edges(data=True):
                i, j = node_to_idx[u], node_to_idx[v]
                
                # Determine edge type
                edge_type = 'regular'
                if data.get('negated'):
                    edge_type = 'negated'
                elif data.get('connection_type') == 'choice':
                    edge_type = 'choice'
                elif data.get('connection_type') == 'and':
                    edge_type = 'and'
                
                # Store concatenated source and target embeddings
                matrices[edge_type][i, j] = np.concatenate([embeddings[u], embeddings[v]])
            
            # Add node self-information to diagonal for isolated nodes
            for node in nodes:
                i = node_to_idx[node]
                if G.degree(node) == 0:
                    matrices['regular'][i, i] = np.concatenate([embeddings[node], embeddings[node]])
            
            return matrices
        
        
    def compute_semantic_adjacency_similarity(self, G1, G2):
        # Compute similarity between two graphs using semantic adjacency matrices that capture both source and target node semantics, handling different graph sizes.
        
        # Define edge types to consider
        edge_types = ['regular', 'negated', 'choice', 'and']
        
        # Get node embeddings
        embeddings1, nodes1, node_to_idx1 = self.create_node_embeddings(G1)
        embeddings2, nodes2, node_to_idx2 = self.create_node_embeddings(G2)
        
        # Create semantic adjacency matrices for each edge type
        
        
        # Get semantic adjacency matrices
        matrices1 = self.create_semantic_adjacency_matrices(G1, embeddings1, nodes1, node_to_idx1)
        matrices2 = self.create_semantic_adjacency_matrices(G2, embeddings2, nodes2, node_to_idx2)
        
        # Calculate similarity for each edge type
        type_similarities = {}
        for edge_type in edge_types:
            # Extract non-zero entries from each matrix (only consider actual edges)
            edges1 = []
            edges2 = []
            
            for i in range(len(nodes1)):
                for j in range(len(nodes1)):
                    if not np.all(matrices1[edge_type][i, j] == 0):
                        edges1.append(matrices1[edge_type][i, j])
            
            for i in range(len(nodes2)):
                for j in range(len(nodes2)):
                    if not np.all(matrices2[edge_type][i, j] == 0):
                        edges2.append(matrices2[edge_type][i, j])
            
            # Convert to numpy arrays
            edges1 = np.array(edges1)
            edges2 = np.array(edges2)
          
            # Skip if either has no edges of this type
            if len(edges1) == 0 and len(edges2) == 0:
                type_similarities[edge_type] = 1.0  # Both empty, perfect match
                print(f"Similarity for {edge_type}: 1.0000 (both empty)")
                continue
            elif len(edges1) == 0 or len(edges2) == 0:
                type_similarities[edge_type] = 0.0  # One empty, one not, no match
                print(f"Similarity for {edge_type}: 0.0000 (one empty)")
                continue
            
            # Calculate pairwise cosine similarities between all edges
            similarity_matrix = np.zeros((len(edges1), len(edges2)))
            for i in range(len(edges1)):
                for j in range(len(edges2)):
                    similarity_matrix[i, j] = np.dot(edges1[i], edges2[j]) / (
                        np.linalg.norm(edges1[i]) * np.linalg.norm(edges2[j]))
            
            # Use optimal transport to find the best matching between edges
            # This handles different numbers of edges
            n1 = len(edges1)
            n2 = len(edges2)
            
            # Create normalized weights
            p = np.ones(n1) / n1
            q = np.ones(n2) / n2
            
            # Cost matrix is 1 - similarity
            cost_matrix = 1 - similarity_matrix
            
            # Compute Earth Mover's Distance
            try:
                # Compute optimal transport
                transport_plan = ot.emd(p, q, cost_matrix)
                
                # Calculate similarity from transport plan
                similarity = 1 - np.sum(transport_plan * cost_matrix)
            except Exception:
                # Fallback if ot package has issues
                # Use Hungarian algorithm for assignment
                from scipy.optimize import linear_sum_assignment
                row_ind, col_ind = linear_sum_assignment(cost_matrix)
                
                # Calculate average similarity of the optimal matching
                similarity = 1 - cost_matrix[row_ind, col_ind].mean()
            
            type_similarities[edge_type] = similarity
            # print(f"Similarity for {edge_type}: {similarity:.4f}")
        
        # Calculate overall similarity as average of type similarities
        overall_similarity = sum(type_similarities.values()) / len(type_similarities)
        # print(f"Overall similarity: {overall_similarity:.4f}")

        # Calculate structure penalties
        node_diff = abs(len(G1.nodes()) - len(G2.nodes())) / max(len(G1.nodes()), len(G2.nodes()))
        edge_diff = abs(len(G1.edges()) - len(G2.edges())) / max(len(G1.edges()), len(G2.edges()))
        
        size_penalty_factor = 0.5
        # Average the structural differences
        structure_penalty = (node_diff + edge_diff) / 2 * size_penalty_factor
        
        # Apply penalty to similarity
        adjusted_similarity = overall_similarity * (1 - structure_penalty)
        
        return adjusted_similarity, overall_similarity, structure_penalty
    
    
    def calculate_graph_similarity(self, G_gt, G_gen_list, output_file, gen_names=None, config=None):
        # Calculate similarity between a ground truth ASP program graph and multiple generated graphs and save metrics to CSV.
        
        try:
            # Ensure gen_names is a list of the right length if provided
            if gen_names is not None and len(gen_names) != len(G_gen_list):
                raise ValueError("Length of gen_names must match length of G_gen_list")
            
            # If gen_names not provided, create default names
            if gen_names is None:
                gen_names = [f"generated_{i+1}" for i in range(len(G_gen_list))]
                
            # Get experiment version from config
            experiment_version = "Unknown"
            if config and 'experiment' in config and 'version' in config['experiment']:
                experiment_version = config['experiment']['version']
            
            # Process each generated graph against the ground truth
            all_metrics = []
            
            for i, G_gen in enumerate(G_gen_list):
                # Create a dictionary to store only the required metrics
                metrics = {}
                
                # Add experiment version
                metrics['experiment'] = experiment_version
                
                
                # Structure-aware semantic adjacency similarity
                adj_sim = self.compute_semantic_adjacency_similarity(G_gt, G_gen)
                metrics['adjacency_similarity'] = round(adj_sim[0], 5)
                
                all_metrics.append(metrics)
            
            # Create results directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Define the fieldnames in the desired order (experiment first)
            fieldnames = ['experiment', 'adjacency_similarity']
            
            # Check if file exists
            file_exists = os.path.isfile(output_file)
            
            # Write or append metrics to CSV
            with open(output_file, mode='a' if file_exists else 'w', newline='') as f:
                if not file_exists:
                    print(f"Creating new metrics file: {output_file}")
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                else:
                    print(f"Appending metrics to {output_file}")
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writerows(all_metrics)
                
            return all_metrics  # Return metrics dictionary for potential further use
            
        except Exception as e:
            print(f"Error computing similarity: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    