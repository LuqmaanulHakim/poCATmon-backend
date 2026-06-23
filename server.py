from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import new_session, remove
import gc
import os

app = FastAPI()

# -----------------------------
# CORS (safe for dev + prod)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://pocatmon-backend.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Load LIGHTWEIGHT model
# IMPORTANT: reduces memory usage
# -----------------------------
session = new_session("u2netp")

# -----------------------------
# Health check
# -----------------------------
@app.get("/")
def home():
    return {"message": "API running 🚀"}

# -----------------------------
# Remove background endpoint
# -----------------------------
@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    try:
        # Read image
        input_image = await file.read()

        # Run AI background removal
        output = remove(input_image, session=session)

        # Free memory (important for Render free tier)
        gc.collect()

        return Response(content=output, media_type="image/png")

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

# -----------------------------
# Run locally only
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)