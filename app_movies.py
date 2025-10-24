import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
import warnings
warnings.filterwarnings('ignore')

# ---------------------- 1. 数据加载与预处理 ----------------------
@st.cache_data  # 缓存数据，提升加载速度
def load_data():
    # 读取CSV数据（需将文件路径替换为你的本地路径）
    df = pd.read_csv("movies_updated.csv")
    # 数据清洗：处理缺失值、统一单位（预算/票房转为百万美元）
    df = df[df['year'].between(1980, 1989)]  # 筛选1980-1989年数据
    df['budget'] = pd.to_numeric(df['budget'], errors='coerce').fillna(0) / 1000000  # 预算转百万美元
    df['gross'] = pd.to_numeric(df['gross'], errors='coerce').fillna(0) / 1000000    # 票房转百万美元
    df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0)              # 评分清洗
    # 提取高频电影类型（Top5：Action/Comedy/Drama/Horror/Adventure）
    top_genres = df['genre'].value_counts().head(5).index.tolist()
    df['genre_filtered'] = df['genre'].where(df['genre'].isin(top_genres), 'Other')
    return df

df = load_data()

# ---------------------- 2. 页面配置 ----------------------
st.set_page_config(
    page_title="movies_1980s_analysis",
    layout="wide"  # 宽屏布局，适配筛选区与图表区并列
)
# 设置中文字体（解决matplotlib中文乱码）
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ---------------------- 3. 侧边栏筛选组件（三种类型） ----------------------
st.sidebar.title("select filters")

# 3.1 滑块筛选：评分区间（数值型）
score_min, score_max = st.sidebar.slider(
    "movie score range",
    min_value=float(df['score'].min()),
    max_value=float(df['score'].max()),
    value=(6.0, 8.0),  # 默认范围
    step=0.1
)

# 3.2 输入框筛选：导演/演员（文本型，模糊查询）
search_type = st.sidebar.radio("Types", ["Director", "Star"])
search_keyword = st.sidebar.text_input(f"input {search_type} key words", "")

# 3.3 多选框筛选：电影类型（分类数据）
genre_options = df['genre_filtered'].unique().tolist()
selected_genres = st.sidebar.multiselect(
    "type of movie",
    options=genre_options,
    default=genre_options  # 默认全选
)

# ---------------------- 4. 数据筛选逻辑 ----------------------
def filter_data(df, score_min, score_max, search_keyword, search_type, selected_genres):
    # 1. 评分筛选
    filtered_df = df[(df['score'] >= score_min) & (df['score'] <= score_max)]
    # 2. 导演/演员筛选（模糊匹配）
    if search_keyword:
        if search_type == "Director":
            filtered_df = filtered_df[filtered_df['director'].str.contains(search_keyword, case=False, na=False)]
        else:
            filtered_df = filtered_df[filtered_df['star'].str.contains(search_keyword, case=False, na=False)]
    # 3. 类型筛选
    filtered_df = filtered_df[filtered_df['genre_filtered'].isin(selected_genres)]
    return filtered_df

filtered_df = filter_data(df, score_min, score_max, search_keyword, search_type, selected_genres)

# ---------------------- 5. 主页面内容：图表与结果展示 ----------------------
st.title("series movies analysis (1980-1989)")
st.subheader(f"result: find {len(filtered_df)} movies")

# 显示核心数据列表（默认隐藏，可展开）
with st.expander("🔍 View Filtered Movie Data"):
    display_cols = ['name', 'year', 'genre', 'score', 'director', 'star', 'budget', 'gross']
    st.dataframe(filtered_df[display_cols].round(2), use_container_width=True)

# 数据导出功能（筛选后结果导出为Excel）
if len(filtered_df) > 0:
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_movies_1980s.csv",
        mime="text/csv"
    )

# ---------------------- 6. 可视化图表（三大图表，按设计方案实现） ----------------------
col1, col2 = st.columns(2)  # 两列布局，并列显示图表

# 6.1 图表1：各类型电影评分分布（箱线图）
with col1:
    st.subheader("1. score distribution by genre")
    fig, ax = plt.subplots(figsize=(10, 6))
    # 绘制箱线图
    genres = filtered_df['genre_filtered'].unique()
    box_data = [filtered_df[filtered_df['genre_filtered'] == g]['score'].dropna() for g in genres]
    bp = ax.boxplot(box_data, labels=genres, patch_artist=True)
    # 美化图表
    for patch, color in zip(bp['boxes'], plt.cm.Set3(np.linspace(0, 1, len(genres)))):
        patch.set_facecolor(color)
    ax.set_xlabel("types of movie", fontsize=12)
    ax.set_ylabel("score", fontsize=12)
    ax.set_title("score distribution by genre", fontsize=14, pad=20)
    ax.grid(axis='y', alpha=0.3)
    st.pyplot(fig)
 

# 6.2 图表2：评分与票房相关性（散点图）
with col2:
    st.subheader("2. correlation between score and gross")
    fig, ax = plt.subplots(figsize=(10, 6))
    # 按类型绘制散点
    for genre, color in zip(genres, plt.cm.Set2(np.linspace(0, 1, len(genres)))):
        genre_df = filtered_df[filtered_df['genre_filtered'] == genre]
        ax.scatter(
            genre_df['score'], 
            genre_df['gross'], 
            label=genre, 
            alpha=0.6, 
            s=50  # 点大小
        )
    # 标注高评分高票房电影（评分≥8.0且票房≥300百万美元）
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
    # 美化图表
    ax.set_xlabel("score of movies", fontsize=12)
    ax.set_ylabel("global box office(100thousand $)", fontsize=12)
    ax.set_title("correlation between score and gross", fontsize=14, pad=20)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # 图例靠右
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    

# 6.3 图表3：各年份投入产出比（分组柱状图）
st.subheader("3. yearly budget vs gross comparison")
fig, ax1 = plt.subplots(figsize=(12, 6))
# 计算各年份平均预算/票房
yearly_data = filtered_df.groupby('year').agg({
    'budget': 'mean',
    'gross': 'mean'
}).reset_index()
# 绘制双Y轴柱状图
x = yearly_data['year']
width = 0.35  # 柱子宽度

# 左Y轴：平均预算
bars1 = ax1.bar(x - width/2, yearly_data['budget'], width, label='average budget', color='#1f77b4', alpha=0.8)
ax1.set_xlabel("year", fontsize=12)
ax1.set_ylabel("average budget", fontsize=12, color='#1f77b4')
ax1.tick_params(axis='y', labelcolor='#1f77b4')
ax1.set_xticks(x)  # 显示所有年份

# 右Y轴：平均票房
ax2 = ax1.twinx()
bars2 = ax2.bar(x + width/2, yearly_data['gross'], width, label='average budget', color='#ff7f0e', alpha=0.8)
ax2.set_ylabel("average box office(billion $)", fontsize=12, color='#ff7f0e')
ax2.tick_params(axis='y', labelcolor='#ff7f0e')

# 添加数值标签（显示预算/票房具体值）
def add_labels(bars, ax):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f'{height:.1f}',
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords='offset points',
            ha='center', va='bottom',
            fontsize=8
        )

add_labels(bars1, ax1)
add_labels(bars2, ax2)

# 合并图例
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

ax1.set_title("Comparison of average film budgets and box office revenues", fontsize=14, pad=20)
st.pyplot(fig)


# ---------------------- 7. 图表交互：点击跳转详情页（示例） ----------------------
st.subheader("movie detail view")
selected_movie = st.selectbox("select one movie to know more details", filtered_df['name'].tolist())
if selected_movie:
    movie_detail = filtered_df[filtered_df['name'] == selected_movie].iloc[0]
    st.write(f"### {selected_movie}")

    # safe retrieval with fallbacks
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

    st.write(f"**year**:{year_str} | **genre**:{genre} | **score**:{score}")
    st.write(f"**director**:{director} | **star**:{star}")
    st.write(f"**budget**:{budget_str} million$ | **gross**:{gross_str} million$")
    st.write(f"**runtime**:{runtime} min | **company**:{company}")