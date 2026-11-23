import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from database import (
    get_dashboard_metrics,
    get_feedback_items,
    init_db,
    save_feedback,
)
from llm_service import AnalysisError, analyze_feedback

load_dotenv()

ALLOWED_SOURCES = {"Review", "Support Ticket", "Survey"}
MAX_FEEDBACK_LENGTH = 10_000


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY", "dev-only-change-me"),
        DATABASE=os.getenv("DATABASE_PATH", "feedback.db"),
    )

    if test_config:
        app.config.update(test_config)

    init_db(app.config["DATABASE"])

    @app.get("/")
    def home():
        return render_template("home.html", sources=sorted(ALLOWED_SOURCES))

    @app.post("/analyze")
    def analyze():
        feedback = request.form.get("feedback", "").strip()
        source = request.form.get("source", "").strip()

        if not feedback:
            flash("Please enter customer feedback.", "error")
            return redirect(url_for("home"))
        if len(feedback) > MAX_FEEDBACK_LENGTH:
            flash(
                f"Feedback must be {MAX_FEEDBACK_LENGTH:,} characters or fewer.",
                "error",
            )
            return redirect(url_for("home"))
        if source not in ALLOWED_SOURCES:
            flash("Please select a valid feedback source.", "error")
            return redirect(url_for("home"))

        try:
            analysis = analyze_feedback(feedback)
            save_feedback(app.config["DATABASE"], feedback, source, analysis)
        except AnalysisError as exc:
            app.logger.warning("Feedback analysis failed: %s", exc)
            flash(str(exc), "error")
            return redirect(url_for("home"))
        except Exception:
            app.logger.exception("Unexpected error while saving feedback")
            flash("Something went wrong. Please try again.", "error")
            return redirect(url_for("home"))

        flash("Feedback analyzed and saved.", "success")
        return redirect(url_for("dashboard"))

    @app.get("/dashboard")
    def dashboard():
        sort_by = request.args.get("sort", "newest")
        theme = request.args.get("theme", "").strip()
        sentiment = request.args.get("sentiment", "").strip()

        items = get_feedback_items(
            app.config["DATABASE"],
            sort_by=sort_by,
            theme=theme,
            sentiment=sentiment,
        )
        metrics = get_dashboard_metrics(app.config["DATABASE"])

        return render_template(
            "dashboard.html",
            items=items,
            metrics=metrics,
            selected_theme=theme,
            selected_sentiment=sentiment,
            selected_sort=sort_by,
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
