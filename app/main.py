from fastapi import FastAPI
from app.core.config import settings
from app.core.middleware import setup_middleware
from app.core.exceptions import setup_exception_handlers
from app.api.v1.router import api_router


def create_app() -> FastAPI:
    """Создание и настройка приложения FastAPI."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        openapi_url="/openapi.json" if settings.ENVIRONMENT != "production" else None,
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
        
    )
    
    # Настройка middleware
    setup_middleware(app)
    
    # Настройка обработчиков исключений
    setup_exception_handlers(app)
    
    # Базовый health check
    @app.get("/", tags=["Health"])
    async def root():
        return {
            "message": "API работает!",
            "version": settings.VERSION,
            "documentation": {
                "swagger": "/docs",
                "redoc": "/redoc", 
                "scalar": "/scalar",
                "rapidoc": "/rapidoc"
            },
            "api": settings.API_V1_STR
        }
    
    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "healthy", "version": settings.VERSION}
    
    # Подключение роутеров
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    # Добавляем альтернативные документации
    if settings.ENVIRONMENT != "production":
        
        # Scalar - современная красивая документация с кастомными стилями
        @app.get("/scalar", include_in_schema=False)
        async def scalar_html():
            from fastapi.responses import HTMLResponse
            
            # Создаем кастомный HTML с расширенными модальными окнами
            html_content = f"""
            <!doctype html>
            <html>
            <head>
                <title>{settings.PROJECT_NAME} - API Documentation</title>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <style>

                    body {{
                        font-family: 'JetBrains Mono', monospace;
                    }}

                    .scalar-app-layout[data-v-45e9730e] {{
                        max-width: 80vw !important;
                    }}

                    .scalar-app:nth-child(1) {{
                        flex: 1 !important;
                    }}

                    .scalar-app:nth-child(2) {{
                        flex: 2 !important;
                    }}

                    @media (min-width: 1200px) {{
                         :is(.scalar-app .\*\:first\:xl\:border-l-0>*):first-child {{
                            flex: 1 !important;
                         }}
                    }}

                    @media (min-width: 1200px) {{
                          :is(.scalar-app .\*\:xl\:border-l>*) {{
                            flex: 2 !important;
                          }}
                    }}

                </style>
            </head>
            <body>
                <script
                    id="api-reference"
                    data-url="{app.openapi_url}"
                    data-configuration='{{"theme": "purple", "layout": "modern", "showSidebar": true, "darkMode": true}}'
                ></script>
                <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
            </body>
            </html>
            """
            return HTMLResponse(content=html_content)
    
    return app


app = create_app()
