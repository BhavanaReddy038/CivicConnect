from sqlalchemy import select

from database.database import SessionLocal
from database.models.issue_category import IssueCategory


CATEGORIES = [
    "Garbage & Waste Management",
    "Roads & Potholes",
    "Drainage & Sewage",
    "Streetlights",
    "Water Supply",
    "Public Toilets",
    "Traffic & Signals",
    "Parks & Public Spaces",
    "Stray Animals",
    "Electricity",
    "Pollution",
    "Public Safety",
    "Old Age Support",
    "Orphan Support",
    "Other",
]


def seed_issue_categories():
    db = SessionLocal()

    try:
        for category_name in CATEGORIES:
            existing_category = db.scalar(
                select(IssueCategory).where(
                    IssueCategory.name == category_name
                )
            )

            if not existing_category:
                category = IssueCategory(
                    name=category_name
                )
                db.add(category)

        db.commit()

        print("✅ Issue categories seeded successfully.")

        categories = db.scalars(
            select(IssueCategory).order_by(IssueCategory.id)
        ).all()

        for category in categories:
            print(f"{category.id}: {category.name}")

    except Exception as exc:
        db.rollback()
        print(f"❌ Error while seeding categories: {exc}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_issue_categories()