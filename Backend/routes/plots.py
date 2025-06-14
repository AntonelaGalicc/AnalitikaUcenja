from fastapi import APIRouter
import matplotlib.pyplot as plt  # type: ignore
import base64
from io import BytesIO
import shared

router = APIRouter()

@router.get("/math-histogram")
async def math_histogram():
    if shared.uploaded_df is None:
        return {"error": "No data uploaded"}

    plt.figure(figsize=(6, 4))
    shared.uploaded_df['math percentage'].hist(bins=20)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    return {"image": img_str}
