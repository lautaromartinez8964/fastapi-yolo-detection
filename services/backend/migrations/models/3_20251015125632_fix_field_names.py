from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "detection_history" RENAME COLUMN "detected_objets_count" TO "detected_objects_count";
        ALTER TABLE "detection_history" RENAME COLUMN "conf_threshld" TO "conf_threshold";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "detection_history" RENAME COLUMN "conf_threshold" TO "conf_threshld";
        ALTER TABLE "detection_history" RENAME COLUMN "detected_objects_count" TO "detected_objets_count";"""
