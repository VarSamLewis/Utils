import pandas as pd
import networkx as nx

class Table:
    def __init__(self, name: str):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Table) and self.name == other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class ColumnEdge:
    def __init__(self, column_name: str):
        self.column = column_name

    def __str__(self):
        return self.column

    def __repr__(self):
        return self.column


def build_table_graph(df: pd.DataFrame) -> nx.Graph:
    """
    Build a graph with Table objects as nodes and ColumnEdge objects as edge data.
    """
    graph = nx.Graph()
    name_to_table = {}

    # Group by column name to find shared keys
    column_to_tables = df.groupby("COLUMN_NAME")["TABLE_NAME"].apply(list)

    for column_name, table_names in column_to_tables.items():
        # Create Table objects
        tables = []
        for name in table_names:
            if name not in name_to_table:
                name_to_table[name] = Table(name)
            tables.append(name_to_table[name])

        for i in range(len(tables)):
            for j in range(i + 1, len(tables)):
                t1, t2 = tables[i], tables[j]
                graph.add_node(t1)
                graph.add_node(t2)
                graph.add_edge(t1, t2, column=ColumnEdge(column_name))

    return graph


def print_table_path(graph: nx.Graph, start_table_name: str, end_table_name: str):
    """
    Print the shortest path from start to end table, using column edges.
    """
    start = Table(start_table_name)
    end = Table(end_table_name)

    try:
        path = nx.shortest_path(graph, source=start, target=end)
    except nx.NetworkXNoPath:
        print(f"No path between {start_table_name} and {end_table_name}")
        return

    print(f"\nPath from {start} to {end}:")
    for i in range(len(path) - 1):
        t1, t2 = path[i], path[i + 1]
        column = graph.edges[t1, t2]['column']
        print(f"{t1}.{column} → {t2}.{column}")


def load_metadata_from_csv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df[["TABLE_NAME", "COLUMN_NAME"]]


def main():
    file_path = "keys_only_metadata.csv"  # <-- CSV instead of Excel
    metadata_df = load_metadata_from_csv(file_path)

    graph = build_table_graph(metadata_df)
    print(f"Graph contains {len(graph.nodes)} tables and {len(graph.edges)} links.")

    # Example
    print_table_path(graph, "orders", "customers")
    print_table_path(graph, "transactions", "accounts")


if __name__ == "__main__":
    main()
