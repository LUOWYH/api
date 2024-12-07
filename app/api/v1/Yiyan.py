from fastapi import APIRouter, HTTPException
import requests
import random

router = APIRouter()

# 获取远程文本文件的 URL
def getTextLink(t: str) -> str:
    base_url = "https://cdn.s3.luoh-an.me/luoh-an-api/json/text/"
    return f"{base_url}{t}.txt"

# 从远程 URL 获取文件内容，并随机返回一行
async def getRandomLine(url: str) -> str | None:
    try:
        response = requests.get(url, timeout=5)  # 增加超时时间，避免请求卡住
        response.raise_for_status()
        lines = response.text.splitlines()
        lines = [line.strip() for line in lines if line.strip()]  # 去除空行和两端空格
        return random.choice(lines) if lines else None
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="请求超时，请稍后重试")
    except requests.exceptions.RequestException as e:
        print("服务端错误:", e)
        return None

# 根据类型返回随机文本
@router.get("/Yiyan", response_class=str)  # 设置返回值为纯文本
async def getYiyan(t: str):
    # 参数校验
    if not t:
        raise HTTPException(status_code=400, detail="参数 t 不能为空")

    # 获取文本链接并读取内容
    text_link = getTextLink(t)
    random_line = await getRandomLine(text_link)

    if random_line:
        return random_line  # 直接返回字符串
    else:
        raise HTTPException(status_code=400, detail="无法获取该类型的内容或内容为空")