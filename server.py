from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
import os

app = FastAPI()

# ======================
# CORS CONFIG
# ======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# HEALTH CHECK ROUTE
# ======================
@app.get("/")
def home():
    return {"message": "API is running 🚀"}

# ======================
# REMOVE BACKGROUND API
# ======================
@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    input_image = await file.read()

    output = remove(input_image)

    return Response(content=output, media_type="image/png")


# ======================
# RENDER ENTRY POINT
# ======================
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )