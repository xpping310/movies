# Final-project
This is a movie analysis app of my final project in python class.It was made by JinghanXu , PingpingXing , ZilinXu.
# 1980s Movie Data Analysis App  

This is an interactive data analysis application built with Streamlit, focusing on analyzing movie data from the **1980-1989 period**. The app provides intuitive data visualization and filtering features to help users explore and understand relationships between key metrics such as movie ratings, budgets, and box office revenues from this decade.  


## Features  

- **Multi-dimensional Data Filtering**: Filter movies by rating range, director/actor keywords, and genre.  
- **Interactive Data Visualization**: Includes multiple charts to display rating distribution, correlation between ratings and box office, and yearly budget vs. revenue comparisons.  
- **Detailed Data Viewing**: Browse filtered movie lists and download results as a CSV file.  
- **Individual Movie Details**: Access comprehensive information about specific movies.  


## Installation & Setup  

### Prerequisites  
- Python 3.7 or higher  
- Required dependencies: `streamlit`, `pandas`, `matplotlib`, `numpy`  


### Installation Steps  
1. Clone or download this project to your local machine.  
2. Install the required dependencies using pip:  
   ```bash
   pip install streamlit pandas matplotlib numpy
   ```  
3. Ensure the data file `movies_updated.csv` is in the **same directory** as the application script.  
4. Run the app with the following command:  
   ```bash
   streamlit run your_script_name.py
   ```  
   (Replace `your_script_name.py` with the actual name of your Streamlit script, e.g., `movie_analysis_1980s.py`.)  


## Data Description  

The app analyzes movie data from 1980 to 1989, with key fields including:  
- `name`: Movie title  
- `year`: Release year  
- `genre`: Movie genre (e.g., Action, Comedy, Drama)  
- `score`: Movie rating (e.g., from IMDb or similar platforms)  
- `director`: Director of the movie  
- `star`: Lead actor/actress  
- `budget`: Production budget (converted to **millions of USD** for readability)  
- `gross`: Global box office revenue (converted to **millions of USD** for readability)  
- `runtime`: Movie duration (in minutes)  
- `company`: Production company  


## User Guide  

### 1. Using Filters (Left Sidebar)  
The sidebar provides three types of filters to narrow down movie results:  
- **Rating Range Slider**: Adjust the minimum and maximum movie ratings (default: 6.0–8.0).  
- **Search by Director/Star**: Select a search type ("Director" or "Star") and enter a keyword (case-insensitive, e.g., "Steven Spielberg" or "Tom Hanks").  
- **Genre Selection**: Choose one or more genres from the dropdown (defaults to all genres; less common genres are grouped under "Other").  

Filtered results update in real time across all charts and data tables.  


### 2. Viewing & Downloading Data  
- **Expand Filtered Data**: Click the `🔍 View Filtered Movie Data` expander to see the full list of movies matching your filters. The table displays key fields like title, year, genre, rating, and financial metrics (rounded to 2 decimal places).  
- **Download CSV**: If results exist, use the `📥 Download Filtered Data as CSV` button to save the filtered movie list to your local machine (file name: `filtered_movies_1980s.csv`).  


### 3. Interpreting Visualizations  
The app includes three core visualizations to analyze trends:  

#### 1. Rating Distribution by Genre (Box Plot)  
- **Purpose**: Shows how ratings are distributed across different genres (e.g., whether "Drama" movies have higher median ratings than "Action" movies).  
- **Details**: Each box represents the interquartile range (IQR) of ratings for a genre; outliers (unusually high/low ratings) are marked as individual points. Colors differentiate genres for clarity.  

#### 2. Correlation Between Rating and Box Office (Scatter Plot)  
- **Purpose**: Explores whether higher-rated movies tend to earn more at the box office.  
- **Details**:  
  - Each point represents a single movie, colored by genre.  
  - Movies with **ratings ≥ 8.0 and box office ≥ $300M** are annotated with their titles (high-performance outliers).  
  - A legend (top-left) identifies genres; grid lines help track values across axes.  

#### 3. Yearly Budget vs. Box Office (Dual-Axis Bar Chart)  
- **Purpose**: Compares average annual production budgets to average annual box office revenues.  
- **Details**:  
  - Blue bars: Average budget per year (left y-axis, in millions of USD).  
  - Orange bars: Average box office per year (right y-axis, in millions of USD).  
  - Numerical labels on bars show exact values (rounded to 1 decimal place).  
  - A combined legend (top-left) distinguishes between budget and box office metrics.  


### 4. Viewing Individual Movie Details  
- Use the `Select one movie to know more details` dropdown (under "Movie Detail View") to choose a specific movie from the filtered results.  
- The app displays comprehensive details for the selected movie, including:  
  - Basic info: Year, genre, rating  
  - Creative team: Director, lead actor/actress  
  - Financials: Budget and box office (in millions of USD)  
  - Logistics: Runtime (minutes) and production company  


## Notes  
- **Data Loading**: The first run may take a few seconds to load and cache data (via `@st.cache_data` for faster subsequent loads).  
- **Font Compatibility**: The app is configured to support Chinese and English fonts (e.g., `WenQuanYi Zen Hei`, `Arial Unicode MS`) to avoid text rendering issues.  
- **Unit Consistency**: Budget and box office values are uniformly converted to millions of USD to simplify comparisons.  


With this app, you can gain insights into 1980s film industry trends, genre performance, and the relationship between critical acclaim (ratings) and commercial success (box office).