import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons

def plot_interactive_map():
    # 1. Load Data
    try:
        df = pd.read_csv('RAW_DATA/world_population.csv')
    except FileNotFoundError:
        print("Error: 'RAW_DATA/world_population.csv' not found.")
        return

    # 2. Load World Map
    world_url = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
    try:
        world = gpd.read_file(world_url)
    except Exception as e:
        print(f"Error loading map data: {e}")
        return

    # 3. Merge Data
    world_data = world.merge(df, left_on='ADM0_A3', right_on='CCA3', how='left')

    # 4. Identify Columns to Plot
    # We only want numeric columns (Population, Area, etc.) and exclude ID columns
    exclude_cols = ['Rank', 'CCA3', 'Country/Territory', 'Capital', 'Continent', 'geometry', 'ADM0_A3', 'index_right']
    
    # Get list of numeric columns from the original CSV part of the merged data
    possible_cols = [col for col in df.columns if col not in exclude_cols and pd.api.types.is_numeric_dtype(df[col])]
    
    # Default column
    current_col = '2022 Population'
    if current_col not in possible_cols:
        current_col = possible_cols[0]

    # 5. Create the Plot Layout
    # We make space on the left for the buttons
    fig, ax = plt.subplots(figsize=(16, 10))
    plt.subplots_adjust(left=0.25) # Adjust plot to leave room on the left

    # Function to draw the map
    def draw_map(column_name):
        ax.clear() # Clear the previous map
        ax.set_axis_off()
        ax.set_title(f"World Data: {column_name}", fontsize=18)
        
        # Plot base map (grey for missing data)
        world.plot(ax=ax, color='lightgrey', edgecolor='black', linewidth=0.1)
        
        # Plot data
        # Note: We don't use a built-in legend bar here because it gets buggy 
        # when redrawing constantly in Matplotlib.
        world_data.plot(column=column_name,
                        ax=ax,
                        cmap='OrRd',
                        edgecolor='black',
                        linewidth=0.1,
                        missing_kwds={'color': 'lightgrey'})
        
        fig.canvas.draw_idle()

    # 6. Create the Radio Buttons (Menu)
    # Create an axis area for the buttons [left, bottom, width, height]
    rax = plt.axes([0.02, 0.2, 0.18, 0.6], facecolor='#f0f0f0')
    
    # Create the widget
    radio = RadioButtons(rax, possible_cols)

    # 7. Connect the button click to the draw function
    def change_column(label):
        draw_map(label)

    radio.on_clicked(change_column)

    # 8. Draw initial map
    draw_map(current_col)
    
    plt.show()

if __name__ == "__main__":
    plot_interactive_map()