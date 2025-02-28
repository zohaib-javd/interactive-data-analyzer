import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Interactive Data Analyzer App")
st.title("📊Interactive Data Analyzer by ZeeJay🙅‍♂️")
st.subheader("Upload your data in CSV format to explore and visualize trends.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

    st.subheader("Descriptive Statistics")
    st.write(df.describe())

    # --- Data Filtering ---
    st.sidebar.header("Filter Your Data")

    # Multi-select filter for categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    for col in categorical_cols:
        selected_categories = st.sidebar.multiselect(f"Filter by {col}",
                                                        options=df[col].unique(),
                                                        default=list(df[col].unique()))
        df = df[df[col].isin(selected_categories)]

    # Range filter for numerical columns
    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
    for col in numerical_cols:
        min_val, max_val = min(df[col]), max(df[col])
        selected_range = st.sidebar.slider(f"Filter by {col}",
                                             min_value=float(min_val),
                                             max_value=float(max_val),
                                             value=(float(min_val), float(max_val)))
        df = df[(df[col] >= selected_range[0]) & (df[col] <= selected_range[1])]


    st.subheader("Filtered Data")
    st.dataframe(df)

    # --- Data Visualization ---
    st.subheader("Data Trend Visualizations")

    plot_type = st.selectbox("Select Plot Type", ["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart"])
    columns = df.columns.tolist()
    x_column = st.selectbox("Choose X-axis", columns)
    y_column = st.selectbox("Choose Y-axis", columns)


    if st.button("Generate Visualization"):
        st.subheader(f"{plot_type} of {y_column} vs {x_column}")
        if plot_type == "Line Chart":
            if df[x_column].dtype == 'object':
                st.warning("Line chart is best suited for numerical or datetime X-axis. Consider Bar or Scatter plot.")
            else:
                fig = px.line(df, x=x_column, y=y_column, title=f'{y_column} over {x_column}')
                st.plotly_chart(fig)
        elif plot_type == "Bar Chart":
            fig = px.bar(df, x=x_column, y=y_column, title=f'{y_column} by {x_column}')
            st.plotly_chart(fig)
        elif plot_type == "Scatter Plot":
            fig = px.scatter(df, x=x_column, y=y_column, title=f'{y_column} vs {x_column}')
            st.plotly_chart(fig)
        elif plot_type == "Pie Chart":
            if df[y_column].dtype != 'object':
                 st.warning("Pie chart is best suited for categorical Y-axis to show proportions.")
            else:
                fig = px.pie(df, names=x_column, values=y_column, title=f'Distribution of {y_column} across {x_column}')
                st.plotly_chart(fig)


else:
    st.write("Waiting for CSV file upload to begin analysis.")