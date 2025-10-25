import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
import warnings

warnings.filterwarnings('ignore')


@st.cache_data  
def load_data():
    df = pd.read_csv("movies_updated.csv")
    
    df = df[df['year'].between(1980, 1989)]  
    df['budget'] = pd.to_numeric(df['budget'], errors='coerce').fillna(0) / 1000000  
    df['gross'] = pd.to_numeric(df['gross'], errors='coerce').fillna(0) / 1000000    
    df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0)              
 
    top_genres = df['genre'].value_counts().head(5).index.tolist()
    df['genre_filtered'] = df['genre'].where(df['genre'].isin(top_genres), 'Other')
    
    return df


df = load_data()


st.set_page_config(
    page_title="movies_1980s_analysis",
    layout="wide"  
)

plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


st.sidebar.title("Select Filters")


score_min, score_max = st.sidebar.slider(
    "Movie Score Range",
    min_value=float(df['score'].min()),
    max_value=float(df['score'].max()),
    value=(6.0, 8.0),  
    step=0.1
)


search_type = st.sidebar.radio("Search By", ["Director", "Star"])
search_keyword = st.sidebar.text_input(f"Enter {search_type} Keyword", "")


genre_options = df['genre_filtered'].unique().tolist()
selected_genres = st.sidebar.multiselect(
    "Movie Genre",
    options=genre_options,
    default=genre_options  
)


def filter_data(df, score_min, score_max, search_keyword, search_type, selected_genres):
    filtered_df = df[(df['score'] >= score_min) & (df['score'] <= score_max)]
    
    if search_keyword:
        if search_type == "Director":
            filtered_df = filtered_df[
                filtered_df['director'].str.contains(search_keyword, case=False, na=False)
            ]
        else:
            filtered_df = filtered_df[
                filtered_df['star'].str.contains(search_keyword, case=False, na=False)
            ]
    
    filtered_df = filtered_df[filtered_df['genre_filtered'].isin(selected_genres)]
    return filtered_df


filtered_df = filter_data(df, score_min, score_max, search_keyword, search_type, selected_genres)


st.title("1980s Movies Analysis Dashboard")
st.subheader(f"Filtered Results: {len(filtered_df)} Movies Found")


with st.expander("🔍 View Filtered Movie Data"):
    display_cols = ['name', 'year', 'genre', 'score', 'director', 'star', 'budget', 'gross']
    st.dataframe(filtered_df[display_cols].round(2), use_container_width=True)


if len(filtered_df) > 0:
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv,
        file_name="filtered_movies_1980s.csv",
        mime="text/csv"
    )


col1, col2 = st.columns(2)  


with col1:
    st.subheader("1. Score Distribution by Genre")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    genres = filtered_df['genre_filtered'].unique()
    box_data = [filtered_df[filtered_df['genre_filtered'] == g]['score'].dropna() 
                for g in genres]
    bp = ax.boxplot(box_data, labels=genres, patch_artist=True)
    
    for patch, color in zip(bp['boxes'], plt.cm.Set3(np.linspace(0, 1, len(genres)))):
        patch.set_facecolor(color)
    
    ax.set_xlabel("Movie Genre", fontsize=12)
    ax.set_ylabel("IMDb Score", fontsize=12)
    ax.set_title("Score Distribution Across Genres", fontsize=14, pad=20)
    ax.grid(axis='y', alpha=0.3)
    st.pyplot(fig)
 


with col2:
    st.subheader("2. Score vs Global Gross Correlation")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for genre, color in zip(genres, plt.cm.Set2(np.linspace(0, 1, len(genres)))):
        genre_df = filtered_df[filtered_df['genre_filtered'] == genre]
        ax.scatter(
            genre_df['score'], 
            genre_df['gross'], 
            label=genre, 
            alpha=0.6, 
            s=50  
        )
    
    high_perf = filtered_df[(filtered_df['score'] >= 8.0) & (filtered_df['gross'] >= 300)]
    for _, row in high_perf.iterrows():
        ax.annotate(
            row['name'], 
            xy=(row['score'], row['gross']),
            xytext=(5, 5),
            textcoords='offset points',
            fontsize=8,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.5)
        )
    
    ax.set_xlabel("IMDb Score", fontsize=12)
    ax.set_ylabel("Global Gross (Million USD)", fontsize=12)
    ax.set_title("Score vs Global Gross Correlation", fontsize=14, pad=20)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    


st.subheader("3. Yearly Budget vs Gross Comparison")
fig, ax1 = plt.subplots(figsize=(12, 6))

yearly_data = filtered_df.groupby('year').agg({
    'budget': 'mean',
    'gross': 'mean'
}).reset_index()

x = yearly_data['year']
width = 0.35  


bars1 = ax1.bar(
    x - width/2, 
    yearly_data['budget'], 
    width, 
    label='Average Budget', 
    color='#1f77b4', 
    alpha=0.8
)
ax1.set_xlabel("Year", fontsize=12)
ax1.set_ylabel("Average Budget (Million USD)", fontsize=12, color='#1f77b4')
ax1.tick_params(axis='y', labelcolor='#1f77b4')
ax1.set_xticks(x)  


ax2 = ax1.twinx()
bars2 = ax2.bar(
    x + width/2, 
    yearly_data['gross'], 
    width, 
    label='Average Gross', 
    color='#ff7f0e', 
    alpha=0.8
)
ax2.set_ylabel("Average Gross (Million USD)", fontsize=12, color='#ff7f0e')
ax2.tick_params(axis='y', labelcolor='#ff7f0e')


def add_labels(bars, ax):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f'{height:.1f}',
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords='offset points',
            ha='center', 
            va='bottom',
            fontsize=8
        )


add_labels(bars1, ax1)
add_labels(bars2, ax2)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

ax1.set_title(
    "Yearly Average Budget vs Gross (1980-1989)", 
    fontsize=14, 
    pad=20
)
st.pyplot(fig)


st.subheader("Movie Detail View")
selected_movie = st.selectbox(
    "Select a Movie to View Details", 
    filtered_df['name'].tolist()
)

if selected_movie:
    movie_detail = filtered_df[filtered_df['name'] == selected_movie].iloc[0]
    st.write(f"### {selected_movie}")

    year_val = movie_detail.get('year') if 'year' in movie_detail.index else None
    year_str = str(int(year_val)) if pd.notna(year_val) else "N/A"

    genre = movie_detail.get('genre', "N/A")
    score = movie_detail.get('score', "N/A")

    director = movie_detail.get('director', "N/A")
    star = movie_detail.get('star', "N/A")

    budget = movie_detail.get('budget')
    gross = movie_detail.get('gross')
    budget_str = f"{budget:.2f}" if pd.notna(budget) else "N/A"
    gross_str = f"{gross:.2f}" if pd.notna(gross) else "N/A"

    runtime = movie_detail.get('runtime', "N/A")
    company = movie_detail.get('company', "N/A")

    st.write(f"**Year**: {year_str} | **Genre**: {genre} | **Score**: {score}")
    st.write(f"**Director**: {director} | **Star**: {star}")
    st.write(f"**Budget**: {budget_str} Million USD | **Gross**: {gross_str} Million USD")
    st.write(f"**Runtime**: {runtime} min | **Production Company**: {company}")