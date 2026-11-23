import sqlite3
from contextlib import closing
from pathlib import Path


def _connect(database_path):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(database_path):
    """Create the database table in Python; the LLM never touches persistence."""
    Path(database_path).parent.mkdir(parents=True, exist_ok=True)
    with closing(_connect(database_path)) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                feedback TEXT NOT NULL,
                source TEXT NOT NULL,
                theme TEXT NOT NULL,
                sentiment TEXT NOT NULL,
                urgency TEXT NOT NULL,
                priority TEXT NOT NULL,
                summary TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(feedback)").fetchall()
        }
        if "priority" not in columns:
            # Preserve existing MVP history when upgrading an older database.
            connection.execute(
                "ALTER TABLE feedback ADD COLUMN priority TEXT NOT NULL DEFAULT ''"
            )
        connection.commit()


def save_feedback(database_path, feedback, source, analysis):
    with closing(_connect(database_path)) as connection:
        connection.execute(
            """
            INSERT INTO feedback
                (feedback, source, theme, sentiment, urgency, priority, summary)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                feedback,
                source,
                analysis["theme"],
                analysis["sentiment"],
                analysis["urgency"],
                analysis["priority"],
                analysis["summary"],
            ),
        )
        connection.commit()


def get_feedback_items(
    database_path, sort_by="newest", theme="", sentiment=""
):
    # Filtering and sorting are deterministic application logic, not AI work.
    sort_options = {
        "newest": "created_at DESC, id DESC",
        "oldest": "created_at ASC, id ASC",
        "urgency": (
            "CASE urgency WHEN 'Critical' THEN 1 WHEN 'High' THEN 2 "
            "WHEN 'Medium' THEN 3 ELSE 4 END, created_at DESC"
        ),
    }
    order_by = sort_options.get(sort_by, sort_options["newest"])
    clauses = []
    parameters = []

    if theme:
        clauses.append("theme = ?")
        parameters.append(theme)
    if sentiment:
        clauses.append("sentiment = ?")
        parameters.append(sentiment)

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    query = f"SELECT * FROM feedback {where} ORDER BY {order_by}"

    with closing(_connect(database_path)) as connection:
        return connection.execute(query, parameters).fetchall()


def get_dashboard_metrics(database_path):
    with closing(_connect(database_path)) as connection:
        total = connection.execute(
            "SELECT COUNT(*) FROM feedback"
        ).fetchone()[0]
        by_theme = connection.execute(
            """
            SELECT theme, COUNT(*) AS count
            FROM feedback
            GROUP BY theme
            ORDER BY count DESC, theme ASC
            """
        ).fetchall()
        by_sentiment = connection.execute(
            """
            SELECT sentiment, COUNT(*) AS count
            FROM feedback
            GROUP BY sentiment
            ORDER BY count DESC, sentiment ASC
            """
        ).fetchall()
        themes = connection.execute(
            "SELECT DISTINCT theme FROM feedback ORDER BY theme"
        ).fetchall()

    return {
        "total": total,
        "by_theme": by_theme,
        "by_sentiment": by_sentiment,
        "themes": [row["theme"] for row in themes],
    }
