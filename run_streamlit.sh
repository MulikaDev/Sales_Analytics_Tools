#!/bin/bash

# Переходимо в директорію проєкту
cd ~/Documents/sales_analytics || exit

# Активуємо віртуальне середовище
source venv_streamlit/bin/activate

# Оновлюємо pip, setuptools, wheel
pip install --upgrade pip setuptools wheel

# Масив потрібних пакетів
REQUIRED_PKG=("pandas" "streamlit")

# Перевіряємо і встановлюємо відсутні пакети
for pkg in "${REQUIRED_PKG[@]}"; do
    if ! python -c "import $pkg" &> /dev/null; then
        echo "Installing missing package: $pkg"
        pip install "$pkg"
    fi
done

# Запускаємо Streamlit
echo "Запуск Streamlit..."
streamlit run main.py
