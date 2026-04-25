CREATE TABLE IF NOT EXISTS welcome(
    guild_id BIGINT PRIMARY KEY,
    channel_id BIGINT NOT NULL,
    message TEXT NOT NULL
)