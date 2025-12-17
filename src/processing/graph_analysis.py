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
    
    # def nx_to_grakel(self, G):
    #     # Convert a NetworkX graph to a GraKeL graph with structural node and edge labels

    #     # Create node index mapping first
    #     node_to_idx = {node: i for i, node in enumerate(G.nodes())}
        
    #     # Convert edges using node indices
    #     edges = [(node_to_idx[u], node_to_idx[v]) for u, v in G.edges()]
        
    #     # Create structural node labels
    #     node_labels = {}
    #     for node, idx in node_to_idx.items():
    #         # Get node structural properties
    #         in_degree = G.in_degree(node)
    #         out_degree = G.out_degree(node)
            
    #         # Count different edge types
    #         edge_counts = {
    #             'negated': 0,
    #             'choice': 0,
    #             'and': 0,
    #             'regular': 0
    #         }
            
    #         # Convert edge views to lists before combining
    #         all_edges = list(G.in_edges(node, data=True)) + list(G.out_edges(node, data=True))
            
    #         for _, _, data in all_edges:
    #             if data.get('negated'): edge_counts['negated'] += 1
    #             elif data.get('connection_type') == 'choice': edge_counts['choice'] += 1
    #             elif data.get('connection_type') == 'and': edge_counts['and'] += 1
    #             else: edge_counts['regular'] += 1
            
    #         # Get arity (number of arguments)
    #         match = re.match(r'\w+\((.*?)\)', str(node))
    #         if match:
    #             args = match.group(1).split(',')
    #             arity = len(args)
    #         else:
    #             arity = 0
                
    #         # Create structural label
    #         if G.nodes[node].get('node_type') == 'choice':
    #             node_type = 'choice'
    #             bounds = G.nodes[node]
    #             label = f"{node_type}_bounds_{bounds.get('lower_bound')}_{bounds.get('upper_bound')}"
    #         else:
    #             label_parts = [
    #                 f"arity_{arity}",
    #                 f"in_{in_degree}",
    #                 f"out_{out_degree}"
    #             ]
                
    #             # Add edge type counts
    #             for edge_type, count in edge_counts.items():
    #                 if count > 0:
    #                     label_parts.append(f"{edge_type}_{count}")
                
    #             label = "_".join(label_parts)
            
    #         node_labels[idx] = label
        
    #     # Create edge labels based only on type
    #     edge_labels = {}
    #     for u, v, d in G.edges(data=True):
    #         if d.get('connection_type') == 'and':
    #             label = 'and'
    #         elif d.get('connection_type') == 'choice':
    #             label = 'choice'
    #         elif d.get('negated'):
    #             label = 'negated'
    #         else:
    #             label = 'regular'
    #         edge_labels[(node_to_idx[u], node_to_idx[v])] = label

    #     return Graph(edges, node_labels=node_labels, edge_labels=edge_labels)
    
    # def compute_node_embeddings(self, G):
    #     # Create rich text descriptino for each node. 
    #     # Description includes node name and type, number and types of incoming and outgoing edges, and connected nodes with relationship types
        
    #     node_texts = {}
    #     for node in G.nodes():
    #         # Basic node info
    #         node_type = 'choice' if G.nodes[node].get('node_type') == 'choice' else 'regular'
    #         text = f"Node {node} of type {node_type} "
            
    #         # Count incoming edges by type
    #         in_edges = G.in_edges(node, data=True)
    #         in_edge_counts = {
    #             'regular': 0,
    #             'negated': 0,
    #             'choice': 0,
    #             'and': 0
    #         }
            
    #         for _, _, data in in_edges:
    #             if data.get('negated'): in_edge_counts['negated'] += 1
    #             elif data.get('connection_type') == 'choice': in_edge_counts['choice'] += 1
    #             elif data.get('connection_type') == 'and': in_edge_counts['and'] += 1
    #             else: in_edge_counts['regular'] += 1
            
    #         # Add incoming edge information
    #         in_edge_info = [f"{edge_type} {count}" for edge_type, count in in_edge_counts.items() if count > 0]
    #         if in_edge_info:
    #             text += f"with incoming edges: {', '.join(in_edge_info)} "
            
    #         # Count outgoing edges by type
    #         out_edges = G.out_edges(node, data=True)
    #         out_edge_counts = {
    #             'regular': 0,
    #             'negated': 0,
    #             'choice': 0,
    #             'and': 0
    #         }
            
    #         for _, _, data in out_edges:
    #             if data.get('negated'): out_edge_counts['negated'] += 1
    #             elif data.get('connection_type') == 'choice': out_edge_counts['choice'] += 1
    #             elif data.get('connection_type') == 'and': out_edge_counts['and'] += 1
    #             else: out_edge_counts['regular'] += 1
            
    #         # Add outgoing edge information
    #         out_edge_info = [f"{edge_type} {count}" for edge_type, count in out_edge_counts.items() if count > 0]
    #         if out_edge_info:
    #             text += f"with outgoing edges: {', '.join(out_edge_info)} "
            
    #         # Add detailed connection information
    #         connections = []
            
    #         # Incoming connections
    #         for src, _, data in in_edges:
    #             edge_type = "regular"
    #             if data.get('negated'): edge_type = "negated"
    #             elif data.get('connection_type') == 'choice': edge_type = "choice"
    #             elif data.get('connection_type') == 'and': edge_type = "and"
                
    #             src_type = 'choice' if G.nodes[src].get('node_type') == 'choice' else 'regular'
    #             connections.append(f"from {src} ({src_type}) via {edge_type}")
            
    #         # Outgoing connections
    #         for _, tgt, data in out_edges:
    #             edge_type = "regular"
    #             if data.get('negated'): edge_type = "negated"
    #             elif data.get('connection_type') == 'choice': edge_type = "choice"
    #             elif data.get('connection_type') == 'and': edge_type = "and"
                
    #             tgt_type = 'choice' if G.nodes[tgt].get('node_type') == 'choice' else 'regular'
    #             connections.append(f"to {tgt} ({tgt_type}) via {edge_type}")
            
    #         if connections:
    #             text += f"connected {'; '.join(connections)}"
            
    #         node_texts[node] = text
        
    #     # Generate embeddings
    #     embeddings = {}
    #     for node, text in node_texts.items():
    #         embeddings[node] = self.model.encode(text)
        
    #     return embeddings
    
    # def compute_wl_similarity(self, G1, G2):
    #     # Compute Weisfeiler-Lehman graph kernel similarity focusing on structural properties:
    #     # - Node arity
    #     # - Edge types and patterns
    #     # - Local structure (in/out degree, edge type counts)
        
    #     # Convert to GraKeL graphs
    #     grakel_g1 = self.nx_to_grakel(G1)
    #     grakel_g2 = self.nx_to_grakel(G2)
        
    #     # Calculate WL similarity
    #     wl = WeisfeilerLehmanOptimalAssignment(n_iter=3, normalize=True)
    #     wl_sim = wl.fit_transform([grakel_g1, grakel_g2])[0, 1]
        
    #     return wl_sim
    
    # def compute_emd_similarity(self, embeddings1, embeddings2):
    #     # Compute Earth Mover's Distance between node embeddings

    #     # Convert embeddings to matrices
    #     X = np.array(list(embeddings1.values()))
    #     Y = np.array(list(embeddings2.values()))
        
    #     # Compute cost matrix using cosine distance
    #     C = 1 - cosine_similarity(X, Y)
        
    #     # Normalize weights
    #     p = np.ones(len(X)) / len(X)
    #     q = np.ones(len(Y)) / len(Y)
        
    #     # Compute EMD
    #     emd = ot.emd2(p, q, C)
        
    #     # Convert to similarity (1 - normalized_distance)
    #     base_similarity = 1 - (emd / np.max(C))
    #     penalty_factor = 0.5
    #     # Apply size difference penalty
    #     size_diff = abs(len(X) - len(Y)) / max(len(X), len(Y))
    #     size_penalty = size_diff * penalty_factor
        
    #     # Adjust similarity score
    #     adjusted_similarity = base_similarity * (1 - size_penalty)
        
    #     return adjusted_similarity, base_similarity, size_penalty
    
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
    
    
    # def calculate_graph_accuracy(self, G1, G2, threshold=0.9):
    #     # Calculate accuracy for graph comparison.
    #     # G1 is treated as ground truth, G2 as generated.
    #     # Accuracy is measured as the number of generated nodes that match ground truth nodes
    #     # (have cosine similarity >= threshold) divided by the number of ground truth nodes.
        
    #     embeddings1 = self.compute_node_embeddings(G1)
    #     embeddings2 = self.compute_node_embeddings(G2)
        
    #     X = np.array(list(embeddings1.values()))
    #     Y = np.array(list(embeddings2.values()))
        
    #     similarity_matrix = cosine_similarity(X, Y)
        
    #     # Count matches (number of ground truth nodes that have a match in generated)
    #     matches = sum(1 for i in range(len(X)) if np.max(similarity_matrix[i]) >= threshold)
        
    #     # Calculate accuracy
    #     accuracy = matches / len(X) if len(X) > 0 else 0
        
    #     return {
    #         'accuracy': accuracy,
    #         'matches': matches,
    #         'gt_nodes': len(X),
    #         'gen_nodes': len(Y)
    #     }
    
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
                
                # # Compute WL similarity
                # wl_sim = self.compute_wl_similarity(G_gt, G_gen)
                # metrics['wl_similarity'] = round(wl_sim, 5)

                # # Compute node embeddings
                # embeddings_gt = self.compute_node_embeddings(G_gt)
                # embeddings_gen = self.compute_node_embeddings(G_gen)
                
                # # Compute EMD similarity (adjusted)
                # emd_sim = self.compute_emd_similarity(embeddings_gt, embeddings_gen)
                # metrics['emd_adjusted_similarity'] = round(emd_sim[0], 5)
                
                # Structure-aware spectral similarity (adjusted)
                adj_sim = self.compute_semantic_adjacency_similarity(G_gt, G_gen)
                metrics['adjacency_similarity'] = round(adj_sim[0], 5)
            
                # # Graph accuracy (nodal similarity)
                # acc_metrics = self.calculate_graph_accuracy(G_gt, G_gen)
                # metrics['nodal_similarity'] = round(acc_metrics['accuracy'], 5)
                
                all_metrics.append(metrics)
            
            # Create results directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Define the fieldnames in the desired order (experiment first)
            # fieldnames = ['experiment', 'emd_adjusted_similarity', 'wl_similarity', 'adjacency_similarity', 'nodal_similarity']
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
    
    