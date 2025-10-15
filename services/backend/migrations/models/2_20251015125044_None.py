from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "full_name" VARCHAR(50),
    "password" VARCHAR(128),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "detection_history" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "detection_type" VARCHAR(5) NOT NULL,
    "model_used" VARCHAR(50) NOT NULL,
    "file_count" INT NOT NULL,
    "conf_threshld" DOUBLE PRECISION NOT NULL,
    "detected_objets_count" INT NOT NULL,
    "processing_time" DOUBLE PRECISION NOT NULL,
    "file_names" JSONB NOT NULL,
    "output_files" JSONB NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "detection_history"."detection_type" IS 'detection type:image or video';
COMMENT ON COLUMN "detection_history"."model_used" IS 'model used name';
COMMENT ON COLUMN "detection_history"."file_count" IS 'numbers of files processed one-time, image may many, video only one';
COMMENT ON COLUMN "detection_history"."conf_threshld" IS 'confidence threshold';
COMMENT ON COLUMN "detection_history"."detected_objets_count" IS 'detected objects count';
COMMENT ON COLUMN "detection_history"."processing_time" IS 'processing time in seconds';
COMMENT ON COLUMN "detection_history"."file_names" IS 'list of processed file names';
COMMENT ON COLUMN "detection_history"."output_files" IS 'list of output file names';
COMMENT ON TABLE "detection_history" IS '用户检测记录模型';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
