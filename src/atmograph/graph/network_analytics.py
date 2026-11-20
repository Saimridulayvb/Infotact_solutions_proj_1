"""
NetworkX in-memory representation for local topological and graph analytics.
"""

from typing import Dict, Any, List
import networkx as nx
import pandas as pd

class GraphAnalytics:
    """Provides graph metric calculations on the semiconductor network."""

    def __init__(self):
        self.graph = nx.DiGraph()

    def build_from_processed(
        self,
        companies_df: pd.DataFrame,
        relationships_df: pd.DataFrame,
        goes_into_df: pd.DataFrame
    ) -> None:
        # Add companies
        for _, r in companies_df.iterrows():
            self.graph.add_node(str(r["provider_id"]), label="Company", name=r["provider_name"])

        # Add inputs
        for _, r in relationships_df.iterrows():
            self.graph.add_node(str(r["provided_id"]), label="Input", name=r.get("input_name", ""))
            self.graph.add_edge(str(r["provider_id"]), str(r["provided_id"]), type="SUPPLIES")

        # Add sequence
        for _, r in goes_into_df.iterrows():
            self.graph.add_edge(str(r["input_id"]), str(r["goes_into_id"]), type="GOES_INTO")

    def compute_summary_metrics(self) -> Dict[str, Any]:
        return {
            "node_count": self.graph.number_of_nodes(),
            "edge_count": self.graph.number_of_edges(),
            "is_directed": self.graph.is_directed(),
            "is_dag": nx.is_directed_acyclic_graph(self.graph)
        }

    def top_degree_nodes(self, top_n: int = 5) -> List[tuple]:
        degrees = sorted(self.graph.degree(), key=lambda x: x[1], reverse=True)
        return degrees[:top_n]

    def get_node_count(self) -> int:
        """Return total node count in graph."""
        return self.graph.number_of_nodes()


    def get_edge_count(self) -> int:
        """Return total count of directed edges in the in-memory NetworkX graph."""
        return self.graph.number_of_edges()


    def is_directed(self) -> bool:
        """Verify whether internal graph structure is a directed property graph."""
        return self.graph.is_directed()
