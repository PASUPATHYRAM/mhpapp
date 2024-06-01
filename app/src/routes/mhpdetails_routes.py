from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,UploadFile,Body
from fastapi.responses import StreamingResponse,FileResponse, Response,JSONResponse
from app.src.schemas.mhp_details_schemas import (MhpDetails_schema,Graph,MhpContact_schema,ParkDetails_Contact,
                                                 Response_model,Response_model_park_pdf)
from app.src.service.mhpdetails_service import (create_mhp_data,get_mhp_data,converter,converterfrom_db,
                                                remove_dups_record,csv_read,del_db_records,
                                                park_count,bar_graph,converter_contact,
                                                download_data,get_mhp_data_id,remove_rec,
                                                add_contact_data_service,bulkupload,query_parkname,
                                                converter_parkname,csv_data_reader_handler,generate_pdf)
from app.src.models.mhpdetails_model import Mhpcontact
from ..dependency import get_db
from typing import List,Dict,Union
import asyncio


router=APIRouter(prefix='/mhpdata',tags=['MHPDATA'])

@router.post('/add-data',response_model=MhpDetails_schema)
def add_data(data: MhpDetails_schema,db:Session=Depends(get_db)):
    return converter(create_mhp_data(db,data))

@router.get('/all',response_model=List[MhpDetails_schema])
def get_data(db: Session=Depends(get_db)):
    return converterfrom_db(get_mhp_data(db))

@router.get('/removeduplicates',response_model=List[str])
def remove_dups(db: Session=Depends(get_db)):
    return remove_dups_record(db)

@router.post('/bulkupload',response_model=Dict[str, str])
async def bulk_upload(file: UploadFile,db:Session=Depends(get_db)):
    return await csv_read(file, db)

@router.delete('/deleteall',response_model=Dict)
def del_records(db:Session=Depends(get_db)):
    return del_db_records(db)

@router.get('/metrics',response_model=Dict)
def metrics_1(db:Session=Depends(get_db)):
    return park_count(db)

@router.post('/graph')
def plot_graphs(name:Graph,db:Session=Depends(get_db)):
    return bar_graph(db,name)

@router.get('/data.csv',response_class=StreamingResponse)
def get_data_download(db:Session=Depends(get_db)):
    return download_data(get_mhp_data(db))

@router.get('/parks/{id}',response_model=None)
def get_by_id(id: int,db:Session=Depends(get_db)):
    return get_mhp_data_id(db,id)

@router.delete('/parks/{parkname}',response_model=Dict)
def del_by_pname(parkname:str,db:Session=Depends(get_db)):
    return remove_rec(db,parkname)

router_new=APIRouter(prefix='/mhpcontact',tags=['MHPCONTACT'])

@router_new.post('/add_contact',response_model=MhpContact_schema)
def add_contact_data(data:MhpContact_schema,db:Session=Depends(get_db)):
    return converter_contact(add_contact_data_service(data,db))

@router_new.post('/bulkupload',response_model=Response_model)
async def bulk_upload_data(file: UploadFile,db:Session=Depends(get_db)):
    return await csv_data_reader_handler(file,db,MhpContact_schema,Mhpcontact,'address_fk')

@router_new.get('/parkname/{name}')
def get_parkdetails_by_name(name: str,db:Session=Depends(get_db)):
    return generate_pdf(converter_parkname(query_parkname(name,db)),Response_model_park_pdf)


router2=APIRouter(prefix='/user',tags=['Registration'])

@router2.post('/createuser',response_model=Dict)
def create_user(userdata: UserRegisterSchema=Body(...),db:Session=Depends(get_db)):
    return newusercreation(userdata,db)


