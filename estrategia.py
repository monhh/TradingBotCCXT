import ccxt
import pandas as pd
import time
import subprocess
import warnings
from urllib3.exceptions import NotOpenSSLWarning

# Suppress urllib3 v2 OpenSSL warning
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

# --- CONFIGURACIÓN ---
SIMBOLO_CCXT = 'BTC/USDT'
TEMPORALIDAD = '1m'
VENTANA_EMA = 7
# ---------------------

estado_actual = None

def enviar_notificacion_mac(titulo, mensaje):
    try:
        # Use subprocess to avoid shell quoting issues with "BTC"
        script = f'display notification "{mensaje}" with title "{titulo}"'
        subprocess.run(['osascript', '-e', script], check=True)
    except Exception as e:
        print(f"Error enviando notificación: {e}")

def ejecutar_estrategia():
    global estado_actual
    
    # Instanciar exchange (Binance public)
    exchange = ccxt.binance()
    
    try:
        # Descargar OHLCV (Open, High, Low, Close, Volume)
        ohlcv = exchange.fetch_ohlcv(SIMBOLO_CCXT, timeframe=TEMPORALIDAD, limit=100)
        
        if not ohlcv:
            return

        # Convertir a DataFrame
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # Calcular EMA 7
        df['EMA_7'] = df['close'].ewm(span=VENTANA_EMA, adjust=False).mean()
        
        precio = float(df['close'].iloc[-1])
        ema = float(df['EMA_7'].iloc[-1])
        
        hora = time.strftime('%H:%M:%S')
        print(f"[{hora}] {SIMBOLO_CCXT} | Precio: {precio:.2f} | EMA 7: {ema:.2f}")
        
        nuevo_estado = 'ARRIBA' if precio > ema else 'DEBAJO'
        
        if estado_actual is not None and nuevo_estado != estado_actual:
            if nuevo_estado == 'ARRIBA':
                print(f"--- ¡CRUCE ALCISTA DETECTADO! ---")
                enviar_notificacion_mac(f"ALERTA ALCISTA", f"{SIMBOLO_CCXT} cruzó arriba de EMA 7")
            else:
                print(f"--- ¡CRUCE BAJISTA DETECTADO! ---")
                enviar_notificacion_mac(f"ALERTA BAJISTA", f"{SIMBOLO_CCXT} cruzó debajo de EMA 7")
                
        estado_actual = nuevo_estado

    except Exception as e:
        print(f"Error ccxt: {e}")

if __name__ == "__main__":
    print(f"*** INICIANDO MONITOR CCXT {SIMBOLO_CCXT} (EMA 7 / {TEMPORALIDAD}) ***")
    while True:
        try:
            ejecutar_estrategia()
            time.sleep(20)
        except KeyboardInterrupt:
            print("\nBot apagado.")
            break
        except Exception as e:
            time.sleep(10)
