# utils/chart_generator.py
import matplotlib.pyplot as plt

def create_profit_chart(summary_df, chart_path):
    """
    Create a bar chart for total profit by product in Teal/Gray style,
    with product names on X-axis and profit in Euros on Y-axis.
    
    Args:
        summary_df (pd.DataFrame): Summary table with 'product' and 'Total_Profit' columns
        chart_path (str): Path to save the chart PNG
    """
    plt.figure(figsize=(10, 6))
    plt.style.use('dark_background')  # dark background base

    # Colors: alternate bars black and white
    colors = ["#FFFFFF" if i % 2 == 0 else "#000000" for i in range(len(summary_df))]

    bars = plt.bar(
        summary_df['product'],
        summary_df['Total_Profit'],
        color=colors,
        edgecolor="#555555"
    )

    # Add profit values on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2, 
            yval + 0.02*yval,  # slightly above bar
            f"€{yval:,.0f}",
            ha='center', va='bottom', color='#FFFFFF', fontsize=10, fontweight='bold'
        )

    # Axis labels
    plt.ylabel("Total Profit (€)", color="#FFFFFF", fontsize=12, fontweight='bold')
    plt.xlabel("Product", color="#FFFFFF", fontsize=12, fontweight='bold')
    plt.title("Profit by Product", color="#FFFFFF", fontsize=14, fontweight='bold')

    # Tick labels
    plt.xticks(rotation=45, ha="right", color="#FFFFFF")
    plt.yticks(color="#FFFFFF")

    # Grid lines for better readability
    plt.grid(axis='y', linestyle='--', alpha=0.4, color='#AAAAAA')

    # Tight layout to prevent clipping
    plt.tight_layout()

    # Save figure
    plt.savefig(chart_path, dpi=300, bbox_inches="tight", facecolor="#2F2F2F")
    plt.close()
