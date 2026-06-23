from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy-load rembg so the port binds BEFORE the model downloads/loads
_remover = None

def get_remover():
    global _remover
    if _remover is None:
        from rembg import new_session
        _remover = new_session()
    return _remover

@app.get("/")
def home():
    return {"message": "API running"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    from rembg import remove
    input_image = await file.read()
    output = remove(input_image, session=get_remover())
    return Response(content=output, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)