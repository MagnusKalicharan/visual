import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")
def cross(v1, v2):
    return np.cross(v1, v2)

def graph(v1, v2, v_cross):
    fig = go.Figure()
    max_val=max(np.max(np.abs(v1)),np.max(np.abs(v2)),np.max(np.abs(v_cross)))
    BOUND=float(max(5.0,max_val+2.0))
    axis_line=dict(color='black',width=3)
    fig.add_trace(go.Scatter3d(x=[-BOUND, BOUND],y=[0,0],z=[0,0],mode='lines',line=axis_line,showlegend=False))
    fig.add_trace(go.Scatter3d(x=[0,0],y=[-BOUND, BOUND],z=[0,0],mode='lines',line=axis_line,showlegend=False))
    fig.add_trace(go.Scatter3d(x=[0,0],y=[0,0],z=[-BOUND, BOUND],mode='lines',line=axis_line,showlegend=False))
    fig.add_trace(go.Scatter3d(
        x=[BOUND, 0, 0], y=[0, BOUND, 0], z=[0, 0, BOUND],
        mode='text', text=['X Axis', 'Y Axis', 'Z Axis'], 
        textposition='top center',
        textfont=dict(size=14, color='black'), showlegend=False
    ))
    def add_vector(fig, vector, color, name):
        fig.add_trace(go.Scatter3d(
            x=[0, vector[0]], y=[0, vector[1]], z=[0, vector[2]],
            mode='lines', line=dict(color=color, width=6), name=name
        ))
        mag = np.linalg.norm(vector)
        if mag > 0:
            u_norm, v_norm, w_norm = vector[0]/mag, vector[1]/mag, vector[2]/mag      
            cone_size = BOUND * 0.08
            fig.add_trace(go.Cone(
                x=[vector[0]], y=[vector[1]], z=[vector[2]],
                u=[u_norm], v=[v_norm], w=[w_norm],
                sizemode="absolute", sizeref=cone_size, anchor="tip", 
                colorscale=[[0, color], [1, color]], showscale=False, name=name, showlegend=False
            ))

    add_vector(fig, v1, 'red', 'Vector A')
    add_vector(fig, v2, 'blue', 'Vector B')
    add_vector(fig, v_cross, 'green', 'A × B')

    axis_config = dict(
        range=[-BOUND, BOUND],
        showbackground=False,  
        showgrid=True,         
        gridcolor='lightgray',
        zeroline=False,        
        showticklabels=True,   
        title=""
    )

    fig.update_layout(
        template="plotly_white",
        scene=dict(
            xaxis=axis_config,
            yaxis=axis_config,
            zaxis=axis_config,
            aspectmode='cube' 
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=600
    )
    return fig
col1, col2 = st.columns([1,2]) 
with col1:
    st.title("Parameters")
    st.subheader("Vector A")
    a_x = st.slider("A: X",-5.0,5.0,2.0,0.5,width=300)
    a_y = st.slider("A: Y",-5.0,5.0,0.0,0.5,width=300)
    a_z = st.slider("A: Z",-5.0,5.0,0.0,0.5,width=300)

    st.subheader("Vector B")
    b_x = st.slider("B: X",-5.0, 5.0, 0.0, 0.5,width=300)
    b_y = st.slider("B: Y",-5.0, 5.0, 3.0, 0.5,width=300)
    b_z = st.slider("B: Z",-5.0, 5.0, 0.0, 0.5,width=300)
    
    

    


with col2:
    vector_a=np.array([a_x, a_y, a_z])
    vector_b=np.array([b_x, b_y, b_z])
    cross_result=cross(vector_a, vector_b)
    fig=graph(vector_a, vector_b, cross_result)
    fig.update_layout(height=700)
    st.plotly_chart(fig, theme=None, use_container_width=True)
st.subheader("Cross Product")
st.markdown(r"$\mathbf{A} \times \mathbf{B} = \begin{vmatrix} \mathbf{i} & \mathbf{j} & \mathbf{k} \\ a_x & a_y & a_z \\ b_x & b_y & b_z \end{vmatrix}$")
    
st.write("### Vectors")
st.write(rf"$\mathbf{{A}} = [{a_x}, {a_y}, {a_z}]$")
st.write(rf"$\mathbf{{B}} = [{b_x}, {b_y}, {b_z}]$")
st.write(rf"$\mathbf{{A}} \times \mathbf{{B}} = [{cross_result[0]}, {cross_result[1]}, {cross_result[2]}]$")