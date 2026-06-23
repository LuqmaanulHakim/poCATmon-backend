from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from rembg import remove

# ✅ ADD THIS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS CONFIG (IMPORTANT FIX)
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

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    input_image = await file.read()
    output = remove(input_image)
    return Response(content=output, media_type="image/png")