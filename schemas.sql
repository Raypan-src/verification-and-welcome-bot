CREATE TABLE IF NOT EXISTS welcome(
    guild_id BIGINT PRIMARY KEY,
    channel_id BIGINT NOT NULL,
    message TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS verification(
    guild_id BIGINT PRIMARY KEY,
    channel_id BIGINT NOT NULL,
    message TEXT NOT NULL
);