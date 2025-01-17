FROM python:3.13-slim

WORKDIR /memory_minder

COPY requirements.txt .
RUN python3 -m venv env && \
    /bin/bash -c "source env/bin/activate && pip install --no-cache-dir -r requirements.txt"

COPY backend ./backend
COPY frontend ./frontend
COPY shared ./shared

COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh


ENTRYPOINT ["/bin/bash", "-c", "./wait-for-it.sh ${DATABASE_HOST}:${DATABASE_PORT} -- /bin/bash -c 'source env/bin/activate && cd backend && alembic upgrade head && cd .. && python3 -m backend.app.db.data.script_filling && python3 -m frontend.bot.run'"]