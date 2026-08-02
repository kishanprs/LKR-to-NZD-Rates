#!/usr/bin/env python3
"""
Checks the live NZD -> LKR exchange rate and sends a free WhatsApp
(or Telegram) message via CallMeBot when the rate crosses a threshold.

Env vars used (set as GitHub Actions secrets):
  THRESHOLD           - optional, defaults to 190
  CALLMEBOT_PHONE      - your WhatsApp number incl. country code, e.g. +64211618855
  CALLMEBOT_APIKEY     - your CallMeBot WhatsApp apikey
  TELEGRAM_USERNAME    - optional alternative: your CallMeBot Telegram username
                          (only used if CALLMEBOT_PHONE/APIKEY are not set)

You only need to set up ONE of WhatsApp or Telegram, not both.
"""

import os
import json
import urllib.request
import urllib.parse

STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "state.json")
RATE_API_URL = "https://open.er-api.com/v6/latest/NZD"
THRESHOLD = float(os.environ.get("THRESHOLD", "190"))


def get_rate():
    with urllib.request.urlopen(RATE_API_URL, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    if data.get("result") != "success":
        raise RuntimeError(f"Rate API returned an error: {data}")
    return data["rates"]["LKR"]


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"alerted": False}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def send_whatsapp(message):
    phone = os.environ["CALLMEBOT_PHONE"]
    apikey = os.environ["CALLMEBOT_APIKEY"]
    text = urllib.parse.quote(message)
    url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={text}&apikey={apikey}"
    with urllib.request.urlopen(url, timeout=15) as resp:
        print("CallMeBot WhatsApp response:", resp.read().decode())


def send_telegram(message):
    username = os.environ["TELEGRAM_USERNAME"]
    text = urllib.parse.quote(message)
    url = f"https://api.callmebot.com/text.php?user={username}&text={text}"
    with urllib.request.urlopen(url, timeout=15) as resp:
        print("CallMeBot Telegram response:", resp.read().decode())


def send_alert(message):
    if os.environ.get("CALLMEBOT_PHONE") and os.environ.get("CALLMEBOT_APIKEY"):
        send_whatsapp(message)
    elif os.environ.get("TELEGRAM_USERNAME"):
        send_telegram(message)
    else:
        print("No CallMeBot credentials configured — skipping actual send.")
        print("Message would have been:", message)


def main():
    rate = get_rate()
    print(f"Current NZD -> LKR rate: {rate:.4f} (threshold: {THRESHOLD})")

    state = load_state()

    if rate >= THRESHOLD:
        if not state.get("alerted"):
            message = (
                f"NZD/LKR alert: 1 NZD = {rate:.2f} LKR, "
                f"above your {THRESHOLD:.0f} target. Might be a good time to transfer."
            )
            send_alert(message)
            state["alerted"] = True
            save_state(state)
            print("Alert sent, state updated.")
        else:
            print("Already alerted since the last time it dropped below threshold — skipping.")
    else:
        if state.get("alerted"):
            print("Rate dropped back below threshold — resetting so the next crossing re-alerts.")
        state["alerted"] = False
        save_state(state)


if __name__ == "__main__":
    main()
