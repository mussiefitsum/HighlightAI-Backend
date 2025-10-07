from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/api/health")
    def health():
        return {"ok": True, "service": "HighlightAI", "version": "0.1.0"}

    return app
