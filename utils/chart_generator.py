import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO)

def create_sales_chart(df_summary, output_path):
    """
    Створює бар-діаграму продажів у професійному темному стилі з валютою та відсотками.
    """
    logging.info("📈 Creating professional dark chart (Teal Gray Executive)...")

    # --- Очистка даних ---
    df_summary['total_profit'] = (
        df_summary['total_profit']
        .replace(r'[\$,]', '', regex=True)

        .astype(float)
    )

    df_summary['avg_profit_margin'] = (
        df_summary['avg_profit_margin']
        .replace('%','', regex=True)
        .astype(float)
    )

    # --- Групування по продукту ---
    df_plot = df_summary.groupby('product', as_index=False).agg({
        'total_profit': 'sum',
        'total_sales': 'sum',
        'units_sold': 'sum',
        'avg_profit_margin': 'mean'
    })

    # --- Сортування за total_profit для кольорів ---
    df_plot = df_plot.sort_values('total_profit', ascending=False).reset_index(drop=True)

    # --- Визначення кольорів ---
    max_profit_idx = df_plot['total_profit'].idxmax()
    min_profit_idx = df_plot['total_profit'].idxmin()
    colors_list = ['#00BFA5'] * len(df_plot)  # базовий Teal для всіх
    colors_list[max_profit_idx] = 'green'
    colors_list[min_profit_idx] = 'red'

    # --- Малювання графіка ---
    plt.figure(figsize=(10,6))
    fig, ax = plt.subplots(figsize=(10,6))
    fig.patch.set_facecolor('#2E2E2E')  # темно-сірий фон
    ax.set_facecolor('#2E2E2E')

    bars = sns.barplot(
        data=df_plot, 
        x='product', 
        y='total_profit', 
        palette=colors_list, 
        ax=ax
    )

    ## --- Додаємо підписи на барах ---
    for p, profit in zip(bars.patches, df_plot['total_profit']):
     bars.annotate(
        f"${profit:,.0f}", 
        (p.get_x() + p.get_width()/2., p.get_height()),
        ha='center', va='bottom', color='white', fontsize=10
     )


    # --- Легенда ---
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='green', label='Max Profit'),
        Patch(facecolor='red', label='Min Profit'),
        Patch(facecolor='#00BFA5', label='Other Products')
    ]
    ax.legend(handles=legend_elements, frameon=True, facecolor='#2E2E2E', edgecolor='white', labelcolor='white')

    # --- Стиль осей ---
    ax.set_xlabel("Product", color='white', fontsize=12)
    ax.set_ylabel("Total Profit ($)", color='white', fontsize=12)
    ax.tick_params(colors='white', labelsize=10)
    ax.set_title("Total Profit by Product", color='white', fontsize=14)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # --- Збереження ---
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    logging.info(f"✅ Chart saved to {output_path}")
