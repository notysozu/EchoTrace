import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import AsyncSessionLocal, engine, Base
from models.models import Era, Event, AudioFile

async def seed_data():
    async with AsyncSessionLocal() as db:
        
        # 1. Eras
        era1 = Era(id="era-space-race", label="Space Race", start_year=1955, end_year=1975, color_hex="#1a202c")
        era2 = Era(id="era-ww1", label="World War I", start_year=1914, end_year=1918, color_hex="#2d3748")
        era3 = Era(id="era-ancient-greece", label="Ancient Greece", start_year=-800, end_year=-146, color_hex="#4a5568")

        db.add_all([era1, era2, era3])
        await db.commit()

        # 2. Events & Audio
        event1 = Event(id="ev-1", title="Apollo 11 Moon Landing", year=1969, era_id="era-space-race", is_published=True)
        event2 = Event(id="ev-2", title="Assassination of Archduke Franz Ferdinand", year=1914, era_id="era-ww1", is_published=True)
        event3 = Event(id="ev-3", title="Death of Alexander the Great", year=-323, era_id="era-ancient-greece", is_published=True)

        db.add_all([event1, event2, event3])
        await db.commit()

        audio1 = AudioFile(id="audio-1", event_id="ev-1", perspective_type="narrator", 
                           s3_key="science_fiction/spaceship_interior.ogg", format="ogg", duration_seconds=120)
        audio2 = AudioFile(id="audio-2", event_id="ev-2", perspective_type="narrator", 
                           s3_key="weapons/artillery_explosion.ogg", format="ogg", duration_seconds=45)
        audio3 = AudioFile(id="audio-3", event_id="ev-3", perspective_type="narrator", 
                           s3_key="water/rain_on_roof.ogg", format="ogg", duration_seconds=60)

        db.add_all([audio1, audio2, audio3])
        await db.commit()

        print("Database seeded successfully with dummy events!")

if __name__ == "__main__":
    asyncio.run(seed_data())
