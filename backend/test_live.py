from live.manager import LiveManager


manager = LiveManager()

manager.connect(
    "kuroaidev"
)

manager.run()