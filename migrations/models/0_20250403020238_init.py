from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "order" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "type" VARCHAR(6) NOT NULL,
    "side" VARCHAR(4) NOT NULL,
    "instrument" VARCHAR(12) NOT NULL,
    "limit_price" DECIMAL(10,2),
    "quantity" INT NOT NULL
);
COMMENT ON COLUMN "order"."type" IS 'MARKET: market\nLIMIT: limit';
COMMENT ON COLUMN "order"."side" IS 'BUY: buy\nSELL: sell';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "order";
        """
