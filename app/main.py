from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.api.v1 import Yiyan

# 创建 FastAPI 应用实例
app = FastAPI()

# 注册路由
app.include_router(Yiyan.router, prefix="/api/v1")

# 添加中间件以允许所有 HTTP 方法
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，您可以根据需求限制域名
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

# 全局异常处理：处理 HTTPException
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"msg": exc.detail if isinstance(exc.detail, str) else "发生错误"},
    )

# 全局异常处理：处理请求验证错误
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"msg": "请求参数验证失败", "errors": exc.errors()},
    )
