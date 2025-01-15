import csv
import asyncio
from backend.app.db.gateway.image import ImageGateway
from backend.app.db.connection import get_session


async def fill_image(csv_file_path: str):
    async for session in get_session():
        stat = ImageGateway()

        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader)
            rows = list(csv_reader)

        sorted_rows = sorted(rows, key=lambda row: len(row[-1]))

        for row in sorted_rows:
            key = row[1]
            name_image = row[2]

            await stat.add_image(session=session, key=key, name_image=name_image)


if __name__ == "__main__":
    csv_file_path = 'backend/app/db/data/images.csv'
    asyncio.run(fill_image(csv_file_path))
