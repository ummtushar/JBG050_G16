import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from minisom import MiniSom
from sklearn.preprocessing import MinMaxScaler
import folium
from textblob import TextBlob
import geopandas as gpd
from matplotlib.colors import Normalize, rgb2hex
from branca.colormap import LinearColormap

df = pd.read_csv('../data/Final datasets raw/Borough-Table 1.csv', delimiter = ';')
df = df[['Date', 'Survey', 'Borough', 'Measure', 'Proportion', 'MPS']]

#LDA
# texts = df['Measure'].tolist()
# vectorizer = CountVectorizer(stop_words='english')
# doc_term_matrix = vectorizer.fit_transform(texts)

# lda = LatentDirichletAllocation(n_components=2, random_state=42)
# lda.fit(doc_term_matrix)

# # Display topics
# for i, topic in enumerate(lda.components_):
#     print(f"Top words for topic #{i}:")
#     print([vectorizer.get_feature_names_out()[index] for index in topic.argsort()[-10:]])
#     print("\n")

################################################ Mapping the trust on the map ############################################################
# # Calculate sentiment score for each entry
# df['Sentiment_Score'] = df['Measure'].apply(lambda x: TextBlob(x).sentiment.polarity)

# # Group by borough and count the number of positive feedbacks
# positive_feedback_count = df[df['Sentiment_Score'] > 0].groupby('Borough').size().reset_index(name='Positive_Feedback_Count')

# # Load London borough boundaries
# london_boroughs = gpd.read_file("data/london_boroughs.geojson")

# # Merge positive feedback count with borough boundaries and handle missing data
# london_boroughs_feedback = london_boroughs.merge(positive_feedback_count, left_on='name', right_on='Borough', how='left')
# london_boroughs_feedback['Positive_Feedback_Count'].fillna(0, inplace=True)

# # Check for CRS information and convert if necessary
# if london_boroughs_feedback.crs is None:
#     london_boroughs_feedback.set_crs(epsg=4326, inplace=True)  # Assuming the GeoJSON is in WGS 84
# london_boroughs_feedback = london_boroughs_feedback.to_crs(epsg=3857)  # Converting to Web Mercator for area calculations
# london_boroughs_feedback['Borough_Area'] = london_boroughs_feedback['geometry'].area / 1e6  # Convert area from sq meters to sq kilometers

# # Scaling positive feedback counts for color mapping
# scaler = MinMaxScaler()
# london_boroughs_feedback['Scaled_Feedback'] = scaler.fit_transform(london_boroughs_feedback[['Positive_Feedback_Count']])

# # Create a colormap for positive feedback
# feedback_colormap = LinearColormap(colors=['#ffcccc', '#990000'], vmin=0, vmax=1, caption='Positive Feedback Intensity')

# # Create a map of London
# london_map = folium.Map(location=[51.5074, -0.1278], zoom_start=10)

# # Function to adjust circle size
# def radius_picker(count):
#     return 5 + 20 * count  # Adjust this formula to control the radius size

# # Add GeoJson to map to show boundaries
# folium.GeoJson(london_boroughs_feedback, name='London Boroughs').add_to(london_map)

# # Add boroughs to the map with circle size and color intensity based on feedback
# for index, row in london_boroughs_feedback.iterrows():
#     feedback_color = rgb2hex(feedback_colormap(row['Scaled_Feedback']))
#     folium.CircleMarker(
#         location=[row.geometry.centroid.y, row.geometry.centroid.x],
#         radius=radius_picker(row['Positive_Feedback_Count']),
#         color='grey',
#         fill=True,
#         fill_color=feedback_color,
#         fill_opacity=0.7,
#         popup=f"Borough: {row['name']}<br>Positive Feedback: {row['Positive_Feedback_Count']}"
#     ).add_to(london_map)

# feedback_colormap.add_to(london_map)
# london_map.save('london_sentiment_map.html')

########################################  ####################################################

