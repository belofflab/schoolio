from fastapi import APIRouter


router = APIRouter(prefix='/api/v1/info', tags=['Информация'])



@router.get('/')
async def info(): return {"created_by": "Beloff Laboratory https://belofflab.com/"}