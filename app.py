import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV files
tracks_df = pd.read_csv('tracks.csv')
artists_df = pd.read_csv('artists.csv')
playlists_df = pd.read_csv('playlists.csv')

# Ensure the release_date column is in datetime format
tracks_df['release_date'] = pd.to_datetime(tracks_df['release_date'], errors='coerce')

# Add a 'day_of_week' column to the DataFrame
tracks_df['day_of_week'] = tracks_df['release_date'].dt.day_name()

# Streamlit app starts here
st.title("Spotify Wrapped for Your City 🎵📊")

st.sidebar.title("Filter Options")

# Sidebar filters for genre and year range
genres = tracks_df['genre'].unique()

# Dropdown for genre selection
selected_genres = st.sidebar.multiselect('Select Genres', genres, default=[])

# Filter the DataFrame to show only artists belonging to the selected genres
if selected_genres:
    filtered_tracks_df = tracks_df[tracks_df['genre'].isin(selected_genres)]
else:
    filtered_tracks_df = tracks_df

# Update the list of artists based on the selected genre(s)
artists = filtered_tracks_df['artist'].unique()

# Dropdown for artist selection
selected_artists = st.sidebar.multiselect('Select Artists', artists, default=[])

# Slider for selecting year range
year_min = int(tracks_df['year'].min())
year_max = int(tracks_df['year'].max())
selected_year_range = st.sidebar.slider('Select Year Range', year_min, year_max, (year_min, year_max))

# Filter the data based on user input
filtered_data = filtered_tracks_df[
    ((filtered_tracks_df['artist'].isin(selected_artists)) if selected_artists else True) & 
    (filtered_tracks_df['year'] >= selected_year_range[0]) & 
    (filtered_tracks_df['year'] <= selected_year_range[1])
]

# Check if the filtered data is empty to avoid errors
if filtered_data.empty:
    st.write("No data available for the selected filters. Please adjust your selections.")
else:
    # Visualization: Comparison of Genres or Artists
    st.subheader("Comparison of Selected Genres or Artists")

    # Most Popular Genres
    if selected_genres:
        st.write("### Popularity by Genre")
        genre_popularity = filtered_data.groupby('genre')['popularity'].mean().sort_values(ascending=False)

        fig, ax = plt.subplots()
        sns.barplot(x=genre_popularity.index, y=genre_popularity.values, ax=ax)
        ax.set_xlabel("Genre")
        ax.set_ylabel("Average Popularity")
        ax.set_title("Popularity by Genre")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Most Popular Artists
    if selected_artists:
        st.write("### Popularity by Artist")
        artist_popularity = filtered_data.groupby('artist')['popularity'].mean().sort_values(ascending=False)

        fig, ax = plt.subplots()
        sns.barplot(x=artist_popularity.index, y=artist_popularity.values, ax=ax)
        ax.set_xlabel("Artist")
        ax.set_ylabel("Average Popularity")
        ax.set_title("Popularity by Artist")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Visualization: Song Popularity Trends Over Time
    st.subheader("Song Popularity Trends Over Time in Selected Criteria")
    filtered_data['month_year'] = pd.to_datetime(filtered_data['release_date']).dt.to_period('M')
    popularity_trends = filtered_data.groupby('month_year')['popularity'].mean()

    fig, ax = plt.subplots()
    popularity_trends.plot(ax=ax)
    ax.set_xlabel("Month-Year")
    ax.set_ylabel("Average Popularity")
    ax.set_title("Popularity Trends Over Time")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # New Visualization: Number of Tracks by Day of the Week
    st.subheader("Number of Tracks by Day of the Week")
    tracks_by_day = filtered_data['day_of_week'].value_counts().sort_index()

    fig, ax = plt.subplots()
    sns.barplot(x=tracks_by_day.index, y=tracks_by_day.values, ax=ax)
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel("Number of Tracks")
    ax.set_title("Tracks by Day of the Week")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # New Visualization: Most Popular Track
    st.subheader("Most Popular Track in Selected Criteria")
    most_popular_track = filtered_data.loc[filtered_data['popularity'].idxmax()]

    st.write(f"**Track Name:** {most_popular_track['name']}")
    st.write(f"**Artist:** {most_popular_track['artist']}")
    st.write(f"**Popularity Score:** {most_popular_track['popularity']}")
    st.write(f"**Release Date:** {most_popular_track['release_date']}")

# Additional insights and guidance
st.write("## Insights & Recommendations")
st.write("Use the filters to explore different genres, artists, and trends in your city's music preferences. Adjust the selections to see how popularity changes over time or to compare multiple genres or artists.")

# Provide guidance text to improve user experience
st.sidebar.write("### Adjust the filters to explore different music trends!")
st.sidebar.write("Select multiple genres or artists to compare their popularity and trends.")
st.sidebar.write("Use the slider to adjust the time range for your analysis.")

# Footer or conclusion
st.write("## Conclusion")
st.write("This dashboard provides insights into the music preferences of your city based on Spotify data. Use the filters to explore various trends and discover new music!")


# Placeholder for recommendation system
def recommend_songs(filtered_data, n_recommendations=5):
    # This could be a simple popularity-based recommendation
    top_songs = filtered_data.sort_values(by='popularity', ascending=False).head(n_recommendations)
    return top_songs[['name', 'artist', 'popularity']]

# Display recommendations in the sidebar
if not filtered_data.empty:
    recommended_songs = recommend_songs(filtered_data)
    st.sidebar.write("Recommended Songs:")
    for idx, row in recommended_songs.iterrows():
        st.sidebar.write(f"{row['name']} by {row['artist']} (Popularity: {row['popularity']})")
