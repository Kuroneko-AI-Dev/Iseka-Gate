from live.manager import LiveManager


manager = LiveManager()

manager.connect(
    "kurotempestx"
)

manager.run()