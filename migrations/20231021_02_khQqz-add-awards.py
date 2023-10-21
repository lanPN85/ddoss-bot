"""
Add awards
"""

from yoyo import step

__depends__ = {'20231021_01_cEq2L-initial-migration'}

steps = [
    step(
        """
        CREATE TABLE awards (
            id SERIAL PRIMARY KEY,
            from_user VARCHAR(256),
            to_user VARCHAR(256),
            type_ VARCHAR(32),
            chat_name VARCHAR(256),
            message TEXT,
            awarded_at TIMESTAMP
        )
        """,
        "DROP TABLE awards",
    ),
    step(
        "CREATE INDEX idx_awards_from_user ON awards(from_user ASC)",
        "DROP_INDEX idx_awards_from_user",
    ),
    step(
        "CREATE INDEX idx_awards_to_user ON awards(to_user ASC)",
        "DROP_INDEX idx_awards_to_user",
    ),
    step(
        "CREATE INDEX idx_awards_type ON awards(type_ ASC)",
        "DROP_INDEX idx_awards_type",
    ),
    step(
        "CREATE INDEX idx_awards_chat_name ON awards(chat_name ASC)",
        "DROP_INDEX idx_awards_chat_name",
    ),
    step(
        "CREATE INDEX idx_awards_awarded_at ON awards(awarded_at DESC)",
        "DROP_INDEX idx_awards_awarded_at",
    ),
]
