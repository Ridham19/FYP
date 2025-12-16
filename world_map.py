import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


def plot_population_map():
    # 1. Load your data
    # Make sure the CSV file is in the same folder
    df = pd.read_csv('RAW_DATA/world_population.csv')

    # 2. Load the world map
    # We use the URL since the built-in dataset gave you an error
    # This dataset uses 'ADM0_A3' as the 3-letter country code
    world_url = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
    world = gpd.read_file(world_url)

    # 3. Merge the data
    # We join the map (world) with your data (df)
    # Map uses 'ADM0_A3' for code, Your data uses 'CCA3'
    # how='left' keeps all countries in the map, even if you don't have data for them
    world_data = world.merge(df, left_on='ADM0_A3', right_on='CCA3', how='left')

    # 4. Create the plot
    fig, ax = plt.subplots(figsize=(15, 10))

    # Plot the base map (light grey for countries with no data)
    world.plot(ax=ax, color='lightgrey', edgecolor='black', linewidth=0.5)

    # Plot the population data
    # column='2022 Population': This tells it which column to use for coloring
    # cmap='OrRd': The color map (Orange to Red)
    # legend=True: Shows the color scale bar
    world_data.plot(column='2022 Population',
                    ax=ax,
                    legend=True,
                    cmap='OrRd',
                    edgecolor='black',
                    linewidth=0.5,
                    missing_kwds={'color': 'lightgrey'},  # Color for missing countries
                    legend_kwds={'label': "Population (2022)", 'orientation': "horizontal"})

    # 5. Clean up the plot
    ax.set_title("World Population Map (2022)", fontsize=20)
    ax.set_axis_off()

    plt.show()


if __name__ == "__main__":
    plot_population_map()
