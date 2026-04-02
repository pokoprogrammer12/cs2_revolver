from flask import Flask, request
import threading
import time


from audio import play_yehaw

app = Flask(__name__)

last_kills = 0
last_weapon = None
last_trigger = 0

COOLDOWN = 1.0


def trigger_sound():
    threading.Thread(target=play_yehaw, daemon=True).start()


@app.route('/', methods=['POST'])
def receive():
    global last_kills, last_weapon, last_trigger

    data = request.get_json(silent=True)
    if not data:
        return '', 200

    try:
        player = data.get("player", {})
        stats = player.get("match_stats", {})
        weapons = player.get("weapons", {})

        kills = stats.get("kills", 0)

        # fallback weapon logic
        active_weapon = last_weapon

        for w in weapons:
            weapon = weapons[w]
            if weapon.get("state") == "active":
                active_weapon = weapon.get("name")
                break

        if active_weapon:
            last_weapon = active_weapon

        # KILL DETECTION
        if kills > last_kills:

            print(f"🔥 KILL detected | total: {kills} | weapon: {last_weapon}")

            now = time.time()

            # cooldown (ważne!)
            if now - last_trigger > COOLDOWN:

                if last_weapon == "weapon_revolver":
                    print("🤠 YEEHAW - REVOLVER KILL!")
                    trigger_sound()


                else:
                    print(f"🔫 Kill with: {last_weapon}")

                last_trigger = now

        last_kills = kills

    except Exception as e:
        print("ERROR:", e)

    return '', 200


def start_server():
    print("🚀 Yeehaw system running on http://127.0.0.1:3000")
    app.run(host="127.0.0.1", port=3000, debug=False, threaded=True)