from fastapi import FastAPI, Query
from signal_logic import get_signal
from export import export_to_csv
from telegram_bot import send_to_telegram

app = FastAPI()
collected_signals = []

@app.get("/generate")
def generate(pair: str, timeframe: str, direction: str = "both", minAcc: int = 75, maxAcc: int = 95, source: str = "twelve", telegram: bool = False):
    signal = get_signal(pair, timeframe, direction, minAcc, maxAcc, source)
    if "direction" in signal:
        collected_signals.append(signal)
        if telegram:
            msg = f"📊 {signal['pair']} → {signal['direction']} ({signal['accuracy']}%) | Price: {signal['price']}"
            send_to_telegram(msg)
    return signal

@app.get("/export")
def export():
    filename = export_to_csv(collected_signals)
    return {"file": filename}