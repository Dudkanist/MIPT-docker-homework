import os
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# Папка для данных (внутри контейнера)
DATA_DIR = "/app/data"
DB_FILE = os.path.join(DATA_DIR, "genes.txt")

# Создаем папку, если её нет
os.makedirs(DATA_DIR, exist_ok=True)

class Gene(BaseModel):
    """
    Модель гена для сохранения в базу данных. 
    Используется для передачи имени и описания в genes.txt.
    """
    name: str = Field(
        default="BRCA",
        description="Название гена, который ходите сохранить в app/data/genes.txt"
        )

    description: Optional[str] = Field(
        default="Nothing",
        description="Описание гена, который ходите сохранить в app/data/genes.txt"
        )

@app.get("/")
def read_root():
    return {"message": "API is running from Docker!"}

@app.post("/genes/")
def add_gene(gene: Gene):
    with open(DB_FILE, "a") as f:
        f.write(f"{gene.name}: {gene.description}\n")
    return {"status": "saved", "gene": gene.name}

@app.get("/genes/")
def get_genes():
    if not os.path.exists(DB_FILE):
        return {"genes": []}
    with open(DB_FILE, "r") as f:
        lines = f.readlines()
    return {"genes": [line.strip() for line in lines]}

if __name__ == "__main__":
    import uvicorn
    # Берем порт из переменной окружения или ставим 8000 по умолчанию
    port = int(os.getenv("APP_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)