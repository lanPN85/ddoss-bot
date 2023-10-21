"""
Initial migration
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        CREATE TABLE user_message_stats (
            date_ DATE,
            chat_name VARCHAR(256),
            user_name VARCHAR(256),
            topic_name VARCHAR(256),
            type_ VARCHAR(32),
            message_count INTEGER DEFAULT 1,
            PRIMARY KEY(date_, chat_name, user_name, topic_name, type_)
        )
        """,
        "DROP TABLE user_message_stats"
    ),
    step(
        "CREATE INDEX idx_user_message_stats_date ON user_message_stats (date_ DESC)",
        "DROP INDEX idx_user_message_stats_date"
    ),
    step(
        "CREATE INDEX idx_user_message_stats_chat_name ON user_message_stats (chat_name DESC)",
        "DROP INDEX idx_user_message_stats_chat_name"
    ),
    step(
        "CREATE INDEX idx_user_message_stats_user_name ON user_message_stats (user_name DESC)",
        "DROP INDEX idx_user_message_stats_user_name"
    ),
    step(
        "CREATE INDEX idx_user_message_stats_topic_name ON user_message_stats (topic_name DESC)",
        "DROP INDEX idx_user_message_stats_topic_name"
    ),
    step(
        "CREATE INDEX idx_user_message_stats_type ON user_message_stats (type_ DESC)",
        "DROP INDEX idx_user_message_stats_type"
    ),
    step(
        "CREATE INDEX idx_user_message_stats_message_count ON user_message_stats (message_count DESC)",
        "DROP INDEX idx_user_message_stats_message_count"
    ),
]
