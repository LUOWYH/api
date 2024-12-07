# app/api/v1/Yiyan.py
from fastapi import APIRouter, HTTPException
import requests
import random

router = APIRouter()

def getTextLink(t: str) -> str:
    baseUrl = 'https://cdn.s3.luoh-an.me/luoh-an-api/json/text/'
    return f"{baseUrl}{t}.txt"

async def getRandomLine(url: str) -> str | None:
    try:
        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.splitlines()
        lines = [line for line in lines if line.strip() != '']
        return random.choice(lines) if lines else None
    except requests.exceptions.RequestException as e:
        print('服务端错误', e)
        return None

@router.get("/yiyan")
async def getYiyan(t: str):
    if not t:
        raise HTTPException(status_code=400, detail="参数错误")

    textLink = getTextLink(t)
    randomLine = await getRandomLine(textLink)

    if randomLine:
        return randomLine
    else:
        raise HTTPException(status_code=400, detail="该类型不存在或无法获取数据")