import streamlit as st
import math
import heapq
import networkx as nx
import matplotlib.pyplot as plt
# import the necessary functions and variables from searchAlgos.py
from searchAlgos import (
    hospital_graph,
    locations,
    gbfs,
    a_star
)

# Streamlit GUI
#*******************#

# Set Page Config

# write meaningful title and description for the app

# define the nodes and their coordinates
nodes = list(hospital_graph.keys())

# create a selectbox for the user to choose the start and goal nodes
start = st.selectbox(
    "Select Initial Node",
    #pass the list of nodes to the selectbox
    # set the default value to "Pharmacy"
)

goal = st.selectbox(
    "Select Goal Node",
    #pass the list of nodes to the selectbox
    # set the default value to "Emergency_Ward"
)

# create a selectbox for the user to choose the search algorithm


if st.button("Run Search"):

    if algorithm == "GBFS":

        # run the GBFS algorithm with the selected start and goal nodes
        pass
    else:

        # run the A* algorithm with the selected start and goal nodes
        pass

    if path is None:

       # display a error message indicating that no path was found
       pass 

    else:
       
        # Display result
        st.subheader("Search Result")

        st.write(
            f"**Algorithm:** {algorithm}"
        )

        st.write(
            f"**Solution Path:** {' → '.join(path)}"
        )

        st.write(
            f"**Total Path Cost:** {cost:.2f}"
        )


        
        # Visualize NetworkX graph
        
        G = nx.DiGraph()

        for node, neighbors in hospital_graph.items():

            for neighbor, weight in neighbors.items():

               pass
        pos = locations

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        

        ax.set_title(
            f"{algorithm} Solution Path"
        )

        ax.axis("off")

        st.pyplot(fig)