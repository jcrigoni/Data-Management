# .\venv\Scripts\activate
# python -m streamlit run dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import chart_studio.plotly as py
import cufflinks as cf
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objs as go
#import altair as alt



# Page 1
def page1():
    # Read the dataset from a CSV file
    df = pd.read_csv("output_df.csv")

    # Integrate PNG image
    st.image("wordcloud.png", use_column_width=True)

    # Titre de la Page
    st.markdown("<h1 style='color: #ff6600;'>Amazon Business Research Analyst</h1>", unsafe_allow_html=True)
    st.markdown("""En Mars 2021 Amazon lance un nouveau business en Inde: Amazon Food.
    La livraison à domicile de repas, service du type UberEats.
    Amazon en collaboration avec Kaggle lance un challenge pour embaucher ses future Data Scientists.
    En Décembre 2022, ce service n'ayant pas rencontré sa clientèle, Amazon abandonne le projet.""")
    

    # Selectbox with CSV options
    options = ['Updated.csv', 'Clean_test.csv', 'Encoded_clean_test.csv']
    source = st.selectbox("Choisissez un DataSet", options)
    
    # Information dictionaries
    info = {
        'Updated.csv': {
            'Observations': 2442,
            'Variables': '19 + TARGET',
            'Variables Qualitatives': 'Encodées Numérique'
        },
        'Clean_test.csv': {
            'Observations': 11399,
            'Variables': 20,
            'Variables Qualitatives': 'Modalités'
        },
        'Encoded_clean_test.csv': {
            'Observations': 11399,
            'Variables': 20,
            'Variables Qualitatives': 'Encodées Numérique'
        }
    }

    # Create a DataFrame from the selected option's information
    data = {
        'Category': ['Observations', 'Variables', 'Variables Qualitatives'],
        'Information': [info[source]['Observations'], info[source]['Variables'], info[source]['Variables Qualitatives']]
    }
    df_info = pd.DataFrame(data)

    # Display the DataFrame as a table
    st.markdown(f"<h2 style='color: #ff6600;'>{source}</h2>", unsafe_allow_html=True)
    st.write(df_info.to_html(index=False, header=False), unsafe_allow_html=True)

    st.markdown("\n \n \n")


    st.markdown("<h2 style='color: #ff6600;'>Description des 20 variables</h2>", unsafe_allow_html=True)
    # Data for the table
    data = {
        "Variable": [
            "Unnamed: 0", "ID", "Delivery_person_ID", "Delivery_person_Age", "Delivery_person_Ratings",
            "Restaurant_latitude", "Restaurant_longitude", "Delivery_location_latitude", 
            "Delivery_location_longitude", "Time_Orderd", "Time_Order_picked", "Weatherconditions",
            "Road_traffic_density", "Vehicle_condition", "Type_of_order", "Type_of_vehicle",
            "multiple_deliveries", "Festival", "City", "Time_taken(min)"
        ],
        "Description": [
            "Copie de l'index décalée d'un rang", "Identification de la commande",
            "Identification du livreur. Sequence de caractères, contient l'abbreviation des noms de villes", "Âge du Livreur",
            "Note du livreur dans l'application", "Latitude du Restaurant (Coordonnée GPS)", "Longitude du Restaurant (Coordonnée GPS)",
            "Latitude de l'adresse de livraison (Coordonnée GPS)", "Longitude de l'adresse de livraison (Coordonnée GPS)",
            "Heure à laquelle à lieu la commande", "Heure de ramassage de la commande par le livreur", "Conditions Météo encodée en numérique",
            "Conditions du traffic encodée en numérique", "Condition de maintenance du véhicule encodée en numérique",
            "Type de produit commandé encodée en numérique", "Type de véhicule encodée en numérique",
            "Nombre de commande pris en charge par le livreur en plus de la principale",
            "Présence d'évènement au moment de la commande",
            "Densité d'urbanisation", "VARIABLE CIBLE: Temps de trajet"
        ],
        "Type": [
            "int64", "object", "object", "int64", "float64", "float64", "float64", "float64",
            "float64", "object", "object", "int64", "int64", "int64", "int64", "int64", "float64",
            "int64", "int64", "float64"
        ]
    }

    # Convert to DataFrame
    df_variables = pd.DataFrame(data)

    # Identification table
    identification_df = df_variables[df_variables['Variable'].isin(["Unnamed: 0", "ID", "Delivery_person_ID"])]

    # Informations livreur table
    informations_livreur_df = df_variables[df_variables['Variable'].isin(["Delivery_person_Age", "Delivery_person_Ratings"])]

    # Geographie table
    geographie_df = df_variables[df_variables['Variable'].isin([
        "Restaurant_latitude", "Restaurant_longitude", "Delivery_location_latitude", "Delivery_location_longitude"
    ])]

    # Temps table
    temps_df = df_variables[df_variables['Variable'].isin(["Time_Orderd", "Time_Order_picked"])]

    # Variables catégorielles table
    variables_categorielles_df = df_variables[df_variables['Variable'].isin([
        "Weatherconditions", "Road_traffic_density", "Type_of_order", "Vehicle_condition", "Type_of_vehicle", "City", "Festival"
    ])]

    # Variables numériques table
    variables_quantitatives_df = df_variables[df_variables['Variable'].isin([
         "multiple_deliveries", "Time_taken(min)"
    ])]

    # Display the tables in Streamlit
    st.subheader('Index & Identification')
    st.table(identification_df)

    st.subheader('Informations sur les livreurs (quantitatives)')
    st.table(informations_livreur_df)

    st.subheader('Variables Géographiques')
    st.table(geographie_df)

    st.subheader('Variables Temporelles')
    st.table(temps_df)

    st.subheader('Variables Catégorielles')
    st.table(variables_categorielles_df)

    st.subheader('Variables Quantitatives')
    st.table(variables_quantitatives_df)

    st.markdown("\n \n \n")

    # Titre Target
    st.markdown("<h2 style='color: #ff6600;'>Target</h2>", unsafe_allow_html=True)
    st.write("""**Time_taken(min):** C'est la variable cible. Le temps de livraison à partir du ramassage de la commande dans le restaurant. C'est le temps que Amazon cherche à minimiser et à prédire les plus précisément possible. Ses valeurs sont comprises entre 10mn et 54mn""")
    
    st.markdown("\n \n \n")

    # Titre Valeurs Manquantes
    st.markdown("<h2 style='color: #ff6600;'>Valeurs Manquantes</h2>", unsafe_allow_html=True)
    # Create a DataFrame with the missing values information
    data = {
        'Variables': ['Delivery_person_Ratings', 'Time_Orderd', 'multiple_deliveries'],
        'Valeurs Manquantes': [94, 89, 54],
        'Types de traitement': ['Valeur Moyenne', 'Colonne Drop', 'Valeur Moyenne']
    }
    df_missing = pd.DataFrame(data)
    
    # Convert DataFrame to HTML without index and header
    html_table = df_missing.to_html(index=False)
    
    # Display the table in Streamlit
    st.write(html_table, unsafe_allow_html=True)

    st.markdown("\n \n \n")


    # Titre Valeurs Manquantes
    st.markdown("<h2 style='color: #ff6600;'>Valeurs Aberrantes et Filtres</h2>", unsafe_allow_html=True)
    # Create a DataFrame with the missing values information
    data = {
        'Variables': ['Latitudes et Longitudes', 'Time_Order_picked'],
        'Aberrations': ['Négatives ou égale à 0', 'de type 9:60'],
        'Types de traitement': ['Lignes Filtrées', 'Fonction fix_time et formattage Datetime64']
    }
    df_aberration = pd.DataFrame(data)
    
    # Convert DataFrame to HTML without index and header
    html_table_2 = df_aberration.to_html(index=False)
    
    # Display the table in Streamlit
    st.write(html_table_2, unsafe_allow_html=True)

    st.markdown("\n \n \n")

    # Display the number of rows and columns in the dataframe
    number_of_rows, number_of_columns = df.shape
    st.write(f"<h4 style='color: #0061A8;'>Nombre de lignes restantes après traitement: {number_of_rows}</h4'>", unsafe_allow_html=True)
    st.write(f"<h4 style='color: #0061A8;'>Nombre de colonnes restantes après traitement: {number_of_columns}</h4>", unsafe_allow_html=True)

    st.markdown("\n \n \n")


    # Titre Dataframe
    st.markdown("<h2 style='color: #ff6600;'>Dataframe updated.csv</h2>", unsafe_allow_html=True)

    updated_df = pd.read_csv('updated.csv')
    st.dataframe(updated_df)

# Page 2
def page2():
    # Set Streamlit option to suppress deprecated warnings for pyplot
    st.set_option('deprecation.showPyplotGlobalUse', False)
    
    # Display an orange heading using Markdown
    st.markdown("<h1 style='color: #ff6600;'>Statistiques Descriptives</h1>", unsafe_allow_html=True)
    
    # Read the dataset from a CSV file
    df = pd.read_csv("output_df.csv")
    
    # Drop unnecessary columns from the dataframe
    df_drop = df.drop(['Unnamed: 0', 'Restaurant_latitude', 'Restaurant_longitude',
                       'Delivery_location_latitude', 'Delivery_location_longitude'], axis=1)
    
    # Calculate descriptive statistics for the dataframe
    df_describe = df_drop.describe()

    # Display the descriptive statistics in a dataframe format
    st.dataframe(df_describe)  # Use st.table(df_describe) for a static table view
    
    # Display an orange heading using Markdown
    st.markdown("<h3 style='color: #ff6600;'>Fréquences des variables Qualitatives</h3>", unsafe_allow_html=True)

    # Calculate frequency counts for the qualitative variables
    road_traffic_counts = df['Road_traffic_density'].value_counts()
    weather_conditions_counts = df['Weatherconditions'].value_counts()

    # Create two columns
    col1, col2 = st.columns(2)

    # Display frequency counts in the first column
    with col1:
        st.write('Frequencies of Road Traffic Density')
        st.write(road_traffic_counts)

    # Display frequency counts in the second column
    with col2:
        st.write('Frequencies of Weather Conditions')
        st.write(weather_conditions_counts)
    

    # Frequency of delivery speed
    st.markdown("<h3 style='color: #ff6600;'>Fréquence des vitesses moyennes de livraison</h3>", unsafe_allow_html=True)
    # Create a histogram using Plotly Express
    fig = px.histogram(df, x='Speed', nbins=12)
    
    # Adjust the gap between bars
    fig.update_layout(bargap=0.1, xaxis_title='Vitesse (km/h)', yaxis_title='Nombre de livraisons' )
    st.plotly_chart(fig)

    # Pie chart showing frequency of 'Type_of_vehicle'
    st.markdown("<h3 style='color: #ff6600;'>Pie Chart pour 'Type_of_vehicle'</h3>", unsafe_allow_html=True)
    vehicle_counts = df['Type_of_vehicle'].value_counts().reset_index()
    vehicle_counts.columns = ['Type_of_vehicle', 'Count']
    fig = px.pie(vehicle_counts, names='Type_of_vehicle', values='Count')
    st.plotly_chart(fig)

    # Box plot showing delivery time by vehicle type
    st.markdown("<h3 style='color: #ff6600;'>Box Plot Temps de livraison par 'Type_of_vehicle'</h3>", unsafe_allow_html=True)
    fig = px.box(df, x='Type_of_vehicle', y='Time_taken_min')
    fig.update_layout(xaxis_title='Types de Véhicules', yaxis_title='Durée de la livraison en mn')
    st.plotly_chart(fig)

    # Violin plot showing speed distribution by vehicle type
    st.markdown("<h3 style='color: #ff6600;'>Distribution de la vitesse moyenne par 'Type_of_vehicle'</h3>", unsafe_allow_html=True)
    fig = px.violin(df, x='Type_of_vehicle', y='Speed', box=True, points="all")
    fig.update_layout(xaxis_title='Types de Véhicules', yaxis_title='Vitesse Moyenne en km/h')
    st.plotly_chart(fig)
    
    # Violin plot showing delivery time by road traffic density
    st.markdown("<h3 style='color: #ff6600;'>Violon Plot Temps de livraison par 'Road_traffic_density'</h3>", unsafe_allow_html=True)
    fig = px.violin(df, x='Road_traffic_density', y='Time_taken_min')
    fig.update_layout(xaxis_title='Types de Densité du traffic', yaxis_title='Durée de la livraison en mn')
    st.plotly_chart(fig)

    # Calculate correlation for numeric columns
    st.markdown("<h3 style='color: #ff6600;'>Matrice de Corrélation</h3>", unsafe_allow_html=True)
    selected_columns = ['Delivery_person_Age', 'Delivery_person_Ratings', 'Multiple_deliveries',
                        'Time_taken_min', 'Distance', 'Speed']
    correlation_matrix = df[selected_columns].corr()

    # Display correlation matrix as a heatmap
    plt.figure(figsize=(6, 4))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True, annot_kws={"size": 10})
    plt.title('Heatmap')
    st.pyplot()

    


# Page 3
def page3():
    st.markdown("<h1 style='color: #ff6600;'>Visualisations</h1>", unsafe_allow_html=True)
    # Function to display map with restaurants
    def map_restaurants(df, zoom_level):
        fig = px.scatter_mapbox(
            df,
            lat='LATITUDE',
            lon='LONGITUDE',
            hover_name='City_name',
            zoom=zoom_level,
            height=300
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig)

    # Function to compute vehicle and delivery ratings statistics
    def compute_statistics(df):
        grouped_vehicle_type = df.groupby('Type_of_vehicle').agg(
            Orders=('City', 'size'),
            Average_Speed=('Speed', 'mean'),
            Average_Distance=('Distance','mean')
        )

        grouped_ratings = df.groupby('Delivery_person_Ratings').agg(
            Orders=('City', 'size'),
            Average_Speed=('Speed', 'mean'),
            Average_Distance=('Distance','mean')
        )
        grouped_ratings = grouped_ratings.sort_values(by='Delivery_person_Ratings', ascending=False)

        return grouped_ratings, grouped_vehicle_type

    # Function to create hourly traffic graph
    def plot_hourly_traffic(df):
        df['Order_Hour'] = pd.to_datetime(df['Time_Order_picked']).dt.hour

        order_counts_by_hour = df.groupby('Order_Hour').size().reset_index(name='Order_Count')
        avg_speed_by_hour = df.groupby('Order_Hour')['Speed'].mean().reset_index(name='Average_Speed')
        avg_distance_by_hour = df.groupby('Order_Hour')['Distance'].mean().reset_index(name='Average_Distance')
        combined_df = order_counts_by_hour.merge(avg_speed_by_hour, on='Order_Hour').merge(avg_distance_by_hour, on='Order_Hour')
        combined_df = combined_df.drop(combined_df.index[0])

        fig = go.Figure()
        fig.add_trace(go.Bar(x=combined_df['Order_Hour'], y=combined_df['Order_Count'], name='Number of Orders', yaxis='y1'))
        fig.add_trace(go.Scatter(x=combined_df['Order_Hour'], y=combined_df['Average_Speed'], name='Average Speed', yaxis='y2', mode='lines+markers'))
        fig.add_trace(go.Scatter(x=combined_df['Order_Hour'], y=combined_df['Average_Distance'], name='Average Distance per Hour', yaxis='y2', mode='lines+markers'))

        fig.update_layout(
            #title='Nombre de Commandes, Vitesse Moyenne, et Distance Moyenne par Heure',
            xaxis=dict(title='Hour of Day'),
            yaxis=dict(title='Number of Orders', titlefont=dict(color='blue'), tickfont=dict(color='blue')),
            yaxis2=dict(title='Speed (km/h) and Distance (km)', titlefont=dict(color='red'), tickfont=dict(color='red'), anchor='x', overlaying='y', side='right'),
            legend=dict(x=0.1, y=1.1, traceorder='normal', font=dict(size=12), orientation='h')
        )
        st.markdown("<h3 style='color: #ff6600;'>Nombre de Commandes, Vitesse Moyenne, et Distance Moyenne par Heure</h3>", unsafe_allow_html=True)

        st.plotly_chart(fig)

    # Function to plot traffic density over time
    def plot_traffic_density(df):
        df['Time_Order_picked'] = pd.to_datetime(df['Time_Order_picked'])
        df.set_index('Time_Order_picked', inplace=True)
        df_traffic_count = df.groupby('Road_traffic_density').resample('1H').size().unstack().transpose().fillna(0)
        df_traffic_count = df_traffic_count.drop(df_traffic_count.index[0:7])
        

        plt.figure(figsize=(12, 8))
        plt.stackplot(df_traffic_count.index.strftime('%H:%M'), df_traffic_count['Jam'], df_traffic_count['High'],  df_traffic_count['Medium'], df_traffic_count['Low'],
                    colors=['red', '#ff6600', 'blue', 'green'])
        plt.xlabel('Heure')
        plt.ylabel("Nombre de Commandes")
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.legend(['Jam','High', 'Medium', 'Low'], title='Traffic Density', loc='upper left')
        st.markdown("<h3 style='color: #ff6600;'>Densité du traffic et Fréquence de commandes par heure</h3>", unsafe_allow_html=True)
        st.pyplot(plt)

    # Main function for the Streamlit app
    def main():

        # Load data
        df = pd.read_csv('output_df.csv')
        df.rename(columns={'Restaurant_latitude': 'LATITUDE', 'Restaurant_longitude': 'LONGITUDE'}, inplace=True)

        # Select all cities or a specific city
        select_all = st.checkbox('All cities')
        selected_city = st.selectbox('City', options=df['City_name'].unique())
        if not select_all and not selected_city:  
            select_all = True

        if select_all:
            zoom_level = 3
            min_lat = df['LATITUDE'].min()
            max_lat = df['LATITUDE'].max()
            min_lon = df['LONGITUDE'].min()
            max_lon = df['LONGITUDE'].max()

            # Display map with all restaurants
            st.markdown("<h3 style='color: #ff6600;'>Carte des Restaurants</h3>", unsafe_allow_html=True)
            map_restaurants(df, zoom_level)

            # Display geographic coordinates
            with st.expander("Coordinates"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Min Latitude: {min_lat}")
                    st.write(f"Max Latitude: {max_lat}")
                with col2:
                    st.write(f"Min Longitude: {min_lon}")
                    st.write(f"Max Longitude: {max_lon}")

            # Display statistics tables
            with st.expander("Tables"):
                grouped_ratings, grouped_vehicle_type = compute_statistics(df)
                st.markdown("<h3 style='color: #ff6600;'>Ratings par villes</h3>", unsafe_allow_html=True)
                st.write(grouped_ratings)
                st.markdown("<h3 style='color: #ff6600;'>Types de Véhicules</h3>", unsafe_allow_html=True)
                st.write(grouped_vehicle_type)

            # Display hourly traffic graph and traffic density
            with st.expander("Road traffic density"):
                plot_hourly_traffic(df)
                plot_traffic_density(df)

        else:
            zoom_level = 10
            filtered_df = df[df['City_name'] == selected_city]
            min_lat = filtered_df['LATITUDE'].min()
            max_lat = filtered_df['LATITUDE'].max()
            min_lon = filtered_df['LONGITUDE'].min()
            max_lon = filtered_df['LONGITUDE'].max()

            # Display map with filtered restaurants by city
            st.markdown("<h3 style='color: #ff6600;'>Carte des Restaurants</h3>", unsafe_allow_html=True)
            map_restaurants(filtered_df, zoom_level)

            # Display geographic coordinates for selected city
            with st.expander("Coordinates"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Min Latitude: {min_lat}")
                    st.write(f"Max Latitude: {max_lat}")
                with col2:
                    st.write(f"Min Longitude: {min_lon}")
                    st.write(f"Max Longitude: {max_lon}")

            # Display statistics tables for selected city
            with st.expander("Tables"):
                grouped_ratings, grouped_vehicle_type = compute_statistics(filtered_df)
                st.markdown("<h3 style='color: #ff6600;'>Ratings par villes</h3>", unsafe_allow_html=True)
                st.write(grouped_ratings)
                st.markdown("<h3 style='color: #ff6600;'>Types de Véhicules</h3>", unsafe_allow_html=True)
                st.write(grouped_vehicle_type)

            # Display hourly traffic graph and traffic density for selected city
            with st.expander("Road traffic density"):
                plot_hourly_traffic(filtered_df)
                plot_traffic_density(filtered_df)

    # Run the main function when the script is executed directly
    if __name__ == "__main__":
        main()



# Sidebar navigation
page = st.sidebar.radio("Selectionnez une page", ["Description du jeu de données", "Statistiques Descriptives", "Visualisations"])

# Display selected page
if page == "Description du jeu de données":
    page1()
elif page == "Statistiques Descriptives":
    page2()
elif page == "Visualisations":
    page3()
