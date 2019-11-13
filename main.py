import numpy as np
import matplotlib.pyplot as plt
from docplex.mp.model import Model
import streamlit as st
import credentials

st.title('Capacitated Vehicle Routing Problem')
print("")
st.header('Using IBM CPLEX...')

# st.sidebar.text("Number of buses = 15")
# st.slider("Number of buses", 0, 15, 5)
# st.text("")
num_students = st.slider("Number of students", 0, 15, 10)
st.text("")
st.text('Total buses = 15')
capacity = st.slider("Capacity of bus", 0, 20, 15)
# st.text('Capacity of every bus = 100')
st.text("")

url = credentials.url
key = credentials.key

print(url,key)

def plot_solution(arcs, x, y, q):
    print('Plotting')
    plt.figure(figsize=(25,12.5))
    plt.rc('font', size=20)

    plt.scatter(x[1:], y[1:], c='b')

    for i in range(1,len(x)):
        plt.annotate('$q_{}={}$'.format(i,q[i]), (x[i]+3,y[i]))

    for i,j in arcs:
        plt.plot([x[i],x[j]], [y[i],y[j]], c='g', alpha=0.8)

    plt.plot(x[0], y[0], c='r', marker='s')
    plt.annotate('school', (x[0]+3,y[0]-2))
    plt.title("CVRP solution")
    plt.axis('equal')
    st.pyplot(plt)
    print('Plotting finish')

def main():
    r = np.random
    r.seed(0)

    n = num_students # no.of students
    Q = capacity # Bus capacity
    N = [i for i in range(1,n+1)] # list of students
    V = [0] + N # set of vertices including school
    q = {i:r.randint(1,10) for i in N} # node number / demand

    loc_x = r.rand(len(V))*200
    loc_y = r.rand(len(V))*100

    A = [(i,j) for i in V for j in V if i!=j]
    c = {(i,j):np.hypot(loc_x[i]-loc_x[j],loc_y[i]-loc_y[j]) for i,j in A}

    mdl = Model('CVRP')

    x = mdl.binary_var_dict(A, name='x')
    u = mdl.continuous_var_dict(N, ub=Q, name='u')

    mdl.minimize(mdl.sum(c[i,j]*x[i,j] for i,j in A))
    mdl.add_constraints(mdl.sum(x[i,j] for j in V if j!=i)==1 for i in N)
    mdl.add_constraints(mdl.sum(x[i,j] for i in V if i!=j)==1 for j in N)
    mdl.add_indicator_constraints_(mdl.indicator_constraint(x[i,j],u[i]+q[j]==u[j])for i,j in A if i!=0 and j!=0)
    mdl.add_constraints(u[i]>=q[i] for i in N)
    solution = mdl.solve(url=url, key=key)

    if solution:
        st.text(solution)
        st.write("Total time: ", solution.solve_details.time)
        st.write("Complexity: ", solution.solve_status)

    active_arcs =[a for a in A if x[a].solution_value > 0.9]
    # if st.button("Show Graph"):
    plot_solution(active_arcs, loc_x, loc_y, q)

if st.button('Run Algorithm'):
    main()
