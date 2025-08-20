from fastapi import FastAPI
from fastapi.responses import JSONResponse
import csv
from pathlib import Path

app = FastAPI(title="Simple CSV API", version="1.0.0")

CSV_PATH = Path(__file__).parent / "data" / "items.csv"

def to_int_safe(v, default=0):
    try:
        if v is None or str(v).strip() == "":
            return default
        return int(float(str(v).strip()))
    except Exception:
        return default

@app.get("/api/items")
def read_items():
    rows = []
    with CSV_PATH.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        try:
            raw_headers = next(reader)
        except StopIteration:
            return JSONResponse([])

        # 헤더 정규화 (공백/개행/BOM 제거)
        headers = [h.strip() for h in raw_headers]
        # 필드 인덱스 맵
        try:
            idx_id = headers.index("id")
            idx_name = headers.index("name")
            idx_category = headers.index("category")
            idx_stock = headers.index("stock")
            idx_price = headers.index("price")
        except ValueError:
            # 헤더가 예상과 다르면 그대로 DictReader로 반환 (디버그용)
            f.seek(0)
            dict_reader = csv.DictReader(f)
            safe = [{k.strip(): v for k, v in row.items()} for row in dict_reader]
            return JSONResponse(safe)

        for row in reader:
            # 행 길이가 모자라면 스킵
            if len(row) < 5:
                continue
            try:
                item = {
                    "id": to_int_safe(row[idx_id]),
                    "name": row[idx_name].strip(),
                    "category": row[idx_category].strip(),
                    "stock": to_int_safe(row[idx_stock]),
                    "price": to_int_safe(row[idx_price]),
                }
                rows.append(item)
            except Exception:
                # 개별 행 오류는 스킵
                continue

    return JSONResponse(rows)
