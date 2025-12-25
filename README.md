# TradingBotCCXT

Un bot de trading simple escrito en Python que utiliza la librería [CCXT](https://github.com/ccxt/ccxt) para conectarse a Binance (datos públicos) y monitorear el par **BTC/USDT**.

El bot calcula una **EMA (Exponenital Moving Average) de 7 periodos** en gráficos de 1 minuto y envía notificaciones nativas en macOS cuando el precio cruza la media móvil.

## Requisitos

-   Python 3.9+
-   Una terminal en macOS (para las notificaciones `osascript`)
-   [Git](https://git-scm.com/)

## Instalación

1.  **Clonar el repositorio:**

    ```bash
    git clone <TU_URL_DEL_REPOSITORIO>
    cd TradingBotCCXT
    ```

2.  **Crear un entorno virtual (recomendado):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install ccxt pandas
    ```

## Uso

Ejecuta el script principal:

```bash
python3 estrategia.py
```

El bot comenzará a imprimir el precio y la EMA cada 20 segundos. Si detecta un cruce (el precio pasa por encima o por debajo de la EMA), enviará una notificación de escritorio.

Para detenerlo, presiona `Ctrl+C`.

## Notas

-   Este bot **no ejecuta órdenes reales**, solo monitorea precios.
-   Las notificaciones utilizan AppleScript, por lo que solo funcionan en **macOS**.
