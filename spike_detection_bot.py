
import requests
import time

BOT_TOKEN = "7525402201:AAF7Qs_hz6nxjB-sL9Ah4xWLZEz6xPWohmI"
CHAT_ID = "5530345160"
SYMBOLS = ['BEL', 'ADANIGREEN', 'TORNTPHARM', 'GAIL', 'MAZDOCK', 'WAREEENERGY', 'NTPC', 'ATGL', 'INDUSINDBK', 'AJANTPHARM', 'GODIGIT', 'PPLPHARMA', 'MSUMI', 'KEC', 'FIVESTAR', 'PARADEEP', 'GRAVITA', 'RAILTEL', 'VIJAYA', 'IIFLSEC', 'TCI', 'CARTRADE', 'TTKPRESTIG', 'ACI', 'ARVINDFASN', 'JKPAPER', 'THANGAMAYL', 'LXCHEM', 'NACLIND', 'APOLLO', 'FEDFINA', 'QUESS', 'MANGCHEFER', 'FLAIR', 'ARVSMART', 'XPROINDIA', 'AEROFLEX', 'MOLDTKPAC', 'SHANKARA', 'VIDHIING', 'SANGHIIND', 'PUNJABCHEM', 'SYSTANGO', 'BAJAJHCARE']
CHECK_INTERVAL = 15
PRICE_CHANGE_THRESHOLD = 1.5
VOLUME_MULTIPLIER_THRESHOLD = 2

stock_data = {}

def send_telegram_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram error:", e)

def fetch_price_volume(symbol):
    url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            price = float(data['priceInfo']['lastPrice'])
            volume = int(data['securityWiseVolumes']['tradedQuantity'])
            return price, volume
    except Exception as e:
        print("Error fetching", symbol, ":", e)
    return None, None

def detect_spikes():
    for symbol in SYMBOLS:
        price, volume = fetch_price_volume(symbol)
        if price is None:
            continue

        if symbol not in stock_data:
            stock_data[symbol] = (price, volume)
            continue

        old_price, old_volume = stock_data[symbol]
        price_change = ((price - old_price) / old_price) * 100
        volume_ratio = (volume / old_volume) if old_volume > 0 else 0

        if price_change >= PRICE_CHANGE_THRESHOLD or volume_ratio >= VOLUME_MULTIPLIER_THRESHOLD:
            msg = f"🚀 Spike detected for {symbol}\nPrice: ₹{old_price:.2f} → ₹{price:.2f} ({price_change:.1f}%)\nVolume x{volume_ratio:.2f}"
            send_telegram_message(msg)

        stock_data[symbol] = (price, volume)

print("🔁 Monitoring started...")

while True:
    detect_spikes()
    time.sleep(CHECK_INTERVAL)
