import streamlit as st
import math
import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Graph, Use Case: Emergency Supply Robot

locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6)
}

hospital_graph = {
    "Pharmacy": {
        "Main_Corridor": 2.2,
        "Patient_Wing": 4.1
    },

    "Main_Corridor": {
        "Nursing_Station": 2.2
    },

    "Patient_Wing": {
        "Laboratory": 5.0
    },

    "Nursing_Station": {
        "Laboratory": 3.2,
        "Emergency_Ward": 6.0
    },

    "Laboratory": {
        "Emergency_Ward": 3.2
    },

    "Emergency_Ward": {}
}

# Heuristic (Euclidean Distance)
def heuristic(current, goal):
    x1, y1 = locations[current]
    x2, y2 = locations[goal]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Path reconstruction
def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

# GBFS (Greedy Best-First Search)
def gbfs(start, goal):
    if start == goal:
        return [start], 0.0

    frontier = []
    heapq.heappush(frontier, (heuristic(start, goal), start))
    came_from = {start: None}
    explored = set()

    while frontier:
        h, current = heapq.heappop(frontier)

        if current in explored:
            continue

        explored.add(current)

        if current == goal:
            break

        for neighbor in hospital_graph.get(current, {}):
            if neighbor not in explored and neighbor not in came_from:
                came_from[neighbor] = current
                heapq.heappush(frontier, (heuristic(neighbor, goal), neighbor))

    if goal not in came_from:
        return None, 0.0

    path = reconstruct_path(came_from, goal)
    cost = sum(hospital_graph[path[i]][path[i + 1]] for i in range(len(path) - 1))
    return path, cost

# A* Search
def a_star(start, goal):
    if start == goal:
        return [start], 0.0

    frontier = []
    heapq.heappush(frontier, (heuristic(start, goal), start))
    came_from = {start: None}
    g_cost = {start: 0.0}
    explored = set()

    while frontier:
        f, current = heapq.heappop(frontier)

        if current in explored:
            continue

        explored.add(current)

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, g_cost[goal]

        for neighbor, weight in hospital_graph.get(current, {}).items():
            tentative_g = g_cost[current] + weight

            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                came_from[neighbor] = current
                f_value = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(frontier, (f_value, neighbor))

    return None, 0.0

##########################################
# Streamlit GUI Code

# Set Page Config
st.set_page_config(
    page_title="Emergency Supply Robot - Path Finder",
    page_icon="🤖",
    layout="centered"
)

# meaningful title and description for the app
st.title("🤖 Emergency Supply Robot Path Finder")
st.markdown(
    "Find optimal navigation routes for an autonomous hospital supply robot using "
    "**Greedy Best-First Search (GBFS)** or **A* Search**."
)

# define the nodes and their coordinates
nodes = list(hospital_graph.keys())

# create a selectbox for the user to choose the start and goal nodes
col1, col2 = st.columns(2)
with col1:
    start = st.selectbox(
        "Select Initial Node",
        options=nodes,
        index=nodes.index("Pharmacy")
    )

with col2:
    goal = st.selectbox(
        "Select Goal Node",
        options=nodes,
        index=nodes.index("Emergency_Ward")
    )

# create a selectbox for the user to choose the search algorithm
algorithm = st.selectbox(
    "Select Search Algorithm",
    options=["A*", "GBFS"]
)

if st.button("Run Search", type="primary"):
    if algorithm == "GBFS":
        path, cost = gbfs(start, goal)
    else:
        path, cost = a_star(start, goal)

    if path is None:
        st.error(f"❌ No path found from **{start}** to **{goal}**.")
    else:
        # Display result
        st.subheader("Search Result")
        st.write(f"**Algorithm:** {algorithm}")
        st.write(f"**Solution Path:** {' → '.join(path)}")
        st.write(f"**Total Path Cost:** {cost:.2f}")

        # Visualize NetworkX graph
        G = nx.DiGraph()

        for node, neighbors in hospital_graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)

        pos = locations

        fig, ax = plt.subplots(figsize=(10, 6))

        # Base graph visualization
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color="lightseagreen", node_size=2000)
        nx.draw_networkx_edges(G, pos, ax=ax, arrows=True, arrowsize=20, node_size=2000, edge_color="#888888")
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=9, font_weight="bold")

        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=8)

        # Highlight solution path
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=path, ax=ax, node_color="coral", node_size=2000)
        if path_edges:
            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=path_edges,
                ax=ax,
                edge_color="red",
                width=3,
                arrows=True,
                arrowsize=20,
                node_size=2000
            )

        ax.set_title(f"{algorithm} Solution Path | Total Cost = {cost:.2f}", fontsize=12, fontweight="bold")
        ax.axis("off")

        st.pyplot(fig)
