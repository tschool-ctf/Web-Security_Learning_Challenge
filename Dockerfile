FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 避免以root用戶運行容器
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# 設置環境變數
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=runaway_ctf

# 對外開放5000端口
EXPOSE 5000

# 運行Flask應用
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
