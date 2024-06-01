from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.src.db_setup import Base,session,engine
from app.src.routes.mhpdetails_routes import router,router_new,router2
import uvicorn
from contextlib import asynccontextmanager
from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):
    db=session()
    app.state.var=db
    try:
        db.execute(text("SELECT 1"))
        print("DB established")
    except Exception as e:
        print(f"connection failed {e}")
        db.rollback()

    yield
    try:
        db.close()
        print("connection closed")
    except Exception as e:
        print("failed to close")


def get_application():
    application=FastAPI(lifespan=lifespan)
    application.mount('/static',StaticFiles(directory='app/src/static'),name='static')
    Base.metadata.create_all(bind=engine)
    application.include_router(router)
    application.include_router(router2)
    application.include_router(router_new)
    return application

if __name__=="__main__":
    uvicorn.run(get_application())

