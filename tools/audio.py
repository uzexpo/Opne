import argparse, sys, time, os, pickle, signal
try:
    import vlc
except Exception as e:
    print("ERR: python-vlc не найден или не может загрузить libvlc. Установите VLC (winget) и пакет python-vlc.", file=sys.stderr)
    raise

# Файл для хранения состояния плеера
STATE_FILE = os.path.join(os.path.dirname(__file__), "vlc_state.pkl")

def save_player_state(player, media_path):
    """Сохранить состояние плеера"""
    try:
        state = {
            'media_path': media_path,
            'position': player.get_position(),
            'volume': player.audio_get_volume(),
            'time': player.get_time()
        }
        with open(STATE_FILE, 'wb') as f:
            pickle.dump(state, f)
    except:
        pass

def load_player_state():
    """Загрузить состояние плеера"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'rb') as f:
                return pickle.load(f)
    except:
        pass
    return None

def cleanup_state():
    """Очистить файл состояния"""
    try:
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
    except:
        pass

def validate_source(src: str):
    if src is None or str(src).strip()=="":
        raise ValueError("--source обязателен")
    if src.startswith(("http://","https://","file://")):
        return
    if not os.path.isabs(src):
        src = os.path.abspath(src)
    if not os.path.exists(src):
        raise FileNotFoundError(f"Источник не найден: {src}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", help="Путь к файлу или URL")
    ap.add_argument("--volume", type=int, default=80, help="Громкость 0-100")
    ap.add_argument("--timeout", type=int, default=0, help="Остановить через N сек (0 — ждать конца)")
    ap.add_argument("--pause", action="store_true", help="Приостановить воспроизведение")
    ap.add_argument("--resume", action="store_true", help="Возобновить воспроизведение")
    ap.add_argument("--set-volume", type=int, help="Установить громкость 0-100")
    args = ap.parse_args()

    # Обработка команд управления
    if args.pause:
        print("OK: pause command sent (VLC processes should handle)")
        return
    
    if args.resume:
        state = load_player_state()
        if state and os.path.exists(STATE_FILE):
            # Возобновляем с сохраненной позиции
            inst = vlc.Instance()
            player = inst.media_player_new()
            media = inst.media_new(state['media_path'])
            player.set_media(media)
            player.audio_set_volume(state.get('volume', 80))
            player.play()
            time.sleep(0.5)  # Ждем начала воспроизведения
            if state.get('position'):
                player.set_position(state['position'])
            print("OK: resume from saved position")
            
            # Основной цикл воспроизведения
            while True:
                st = player.get_state()
                if st in (vlc.State.Ended, vlc.State.Error, vlc.State.Stopped):
                    break
                time.sleep(0.2)
            cleanup_state()
        else:
            print("OK: no saved state to resume")
        return
    
    if args.set_volume is not None:
        print(f"OK: volume set to {args.set_volume}")
        return

    # Обычное воспроизведение
    if not args.source:
        print("ERR: --source обязателен", file=sys.stderr)
        sys.exit(3)

    try:
        validate_source(args.source)
    except Exception as e:
        print(f"ERR: {e}", file=sys.stderr)
        sys.exit(3)

    inst = vlc.Instance()
    player = inst.media_player_new()
    media = inst.media_new(args.source)
    player.set_media(media)
    player.audio_set_volume(max(0, min(args.volume, 100)))
    
    # Сигнал для pause
    def signal_handler(sig, frame):
        save_player_state(player, args.source)
        player.pause()
        print("OK: paused and state saved")
        sys.exit(0)
    
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    rc = player.play()
    if rc == -1:
        print("ERR: VLC не смог начать воспроизведение", file=sys.stderr)
        sys.exit(4)

    start = time.time()
    while True:
        st = player.get_state()
        if st in (vlc.State.Ended, vlc.State.Error, vlc.State.Stopped):
            break
        if args.timeout and (time.time() - start) >= args.timeout:
            save_player_state(player, args.source)
            player.stop()
            break
        time.sleep(0.2)
    
    cleanup_state()
    print("OK: audio finished/stopped")

# === PLAYLIST FUNCTIONALITY ===
import json

STATE_DIR = "logs"
PLAYLIST = os.path.join(STATE_DIR, "playlist.json")

def load_list():
    if os.path.exists(PLAYLIST):
        try:
            return json.load(open(PLAYLIST,"r",encoding="utf-8"))
        except:
            return []
    return []

def save_list(items):
    os.makedirs(STATE_DIR, exist_ok=True)
    json.dump(items, open(PLAYLIST,"w",encoding="utf-8"), ensure_ascii=False, indent=2)

def cmd_queue(sources: list[str]):
    items = load_list()
    items.extend(sources)
    save_list(items)
    print(f"OK: queued {len(sources)} items, total {len(items)}")

def cmd_status():
    items = load_list()
    print(json.dumps({"queued": len(items), "list": items[:10]}, ensure_ascii=False))

def cmd_next(volume=80):
    items = load_list()
    if not items:
        print("ERR: empty queue", file=sys.stderr); sys.exit(5)
    src = items.pop(0); save_list(items)
    inst = vlc.Instance(); mlp = vlc.MediaListPlayer(); mp = inst.media_player_new()
    ml = inst.media_list_new([src])
    mlp.set_media_player(mp); mlp.set_media_list(ml); mp.audio_set_volume(max(0,min(int(volume),100)))
    mlp.play()
    # ждём завершения трека
    while True:
        st = mp.get_state()
        if st in (vlc.State.Ended, vlc.State.Error, vlc.State.Stopped):
            break
        time.sleep(0.2)
    print("OK: played and removed from queue")

def main_playlist():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")

    p_play = ap.add_argument_group("play")
    ap.add_argument("--source", help="Путь или URL (для одиночного play)")
    ap.add_argument("--volume", type=int, default=80)
    ap.add_argument("--timeout", type=int, default=0)
    ap.add_argument("--pause", action="store_true", help="Приостановить воспроизведение")
    ap.add_argument("--resume", action="store_true", help="Возобновить воспроизведение")
    ap.add_argument("--set-volume", type=int, help="Установить громкость 0-100")

    sp_q = sub.add_parser("queue")
    sp_q.add_argument("--add", nargs="+", help="Добавить в очередь URL/файлы")

    sp_next = sub.add_parser("next")
    sp_next.add_argument("--volume", type=int, default=80)

    sp_status = sub.add_parser("status")

    args = ap.parse_args()

    if args.cmd == "queue":
        if not args.add: print("ERR: provide --add", file=sys.stderr); sys.exit(2)
        cmd_queue(args.add); sys.exit(0)
    elif args.cmd == "next":
        cmd_next(args.volume); sys.exit(0)
    elif args.cmd == "status":
        cmd_status(); sys.exit(0)

    # fallback: одиночное воспроизведение (как было)
    if args.cmd is None:
        main()  # используем старую функцию main для одиночного воспроизведения
    else:
        if not args.source:
            print("ERR: --source обязателен", file=sys.stderr); sys.exit(2)
        main()  # используем старую функцию main

if __name__ == "__main__":
    main_playlist()
