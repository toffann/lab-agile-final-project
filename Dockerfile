FROM python:3.11-slim

# Pembuatan user non-root demi keamanan klaster sesuai instruksi uji IBM
RUN useradd -u 1001 -r -g 0 -d /app -s /sbin/nologin -c "Default Application User" appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh komponen berkas aplikasi secara utuh
COPY . .

# Mengubah hak kepemilikan folder ke user non-root
RUN chown -R 1001:0 /app && chmod -R g=u /app

EXPOSE 8080

USER 1001

ENV FLASK_APP=service:app
ENV PORT=8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "service:app"]