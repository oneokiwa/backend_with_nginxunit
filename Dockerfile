FROM unit:1.33.0-python3.11-slim

# 앱 파일 복사
WORKDIR /app
COPY app /app

# 파이썬 패키지 설치
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Unit 설정 주입 (docker-entrypoint가 자동 적용)
COPY unit/config.json /docker-entrypoint.d/config.json

EXPOSE 8000
# 엔트리포인트/커맨드는 base 이미지가 제공 (unitd + config 적용)
