from sqlalchemy.orm import Session
from app.src.schemas.mhp_details_schemas import MhpDetails_schema,Graph,MhpContact_schema,ParkDetails_Contact,Response_model_park_pdf
from app.src.models.mhpdetails_model import MhpDetails,Mhpcontact
from sqlalchemy import and_,func
import pandas as pd
import asyncio
import io
from fastapi import UploadFile,HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse,FileResponse,JSONResponse
from typing import Dict,Type
import matplotlib.pyplot as plt
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import gold,violet

def create_mhp_data(db: Session,mhpdata: MhpDetails_schema):
    mhp_data=mhpdata.dict()
    addres=mhp_data['address']
    new_data=MhpDetails(park_name=mhp_data['parkname'],
                        city=mhp_data['city'],
                        state=mhp_data['state'],
                        zip=mhp_data['zip'],
                        address_line_1=addres['address_line1'],
                        address_line_2=addres['address_line2'])
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

def get_mhp_data(db:Session):
    data=db.query(MhpDetails).all()
    return data

def get_mhp_data_id(db:Session,id):
    data=db.query(MhpDetails).filter(MhpDetails.id==id).first()
    print(type(data))
    if data:
        return {"name":data.park_name}
    else:
        return FileResponse('app/src/static/2904.png',status_code=404)

def generate_pdf(data,schema:Response_model_park_pdf):

    for dataa in data:
        sc_vali = schema(**dataa['park_details'])

        c=canvas.Canvas("report.pdf",pagesize=letter)
        c.drawImage('app/src/static/2904.png',50,70,width=50,height=70)
        c.setFillColor(violet)
        c.drawString(50,720,sc_vali.parkname)
        c.drawString(50, 700, sc_vali.city)
        c.drawString(50, 680, sc_vali.state)
        c.setFillColor(gold)
        c.drawString(50, 660, str(sc_vali.zip))
        c.drawString(50, 640, sc_vali.address.address_line1)
        c.drawImage('app/src/static/reded.png',width=150,height=300,x=50,y=100)
        c.save()
    return FileResponse("report.pdf", media_type="application/pdf")




def remove_dups_record(db:Session):
    distinct_records=db.query(MhpDetails).distinct().all()
    dups=[]
    try:
        for rec in distinct_records:
            match_rec=db.query(MhpDetails).filter(and_(MhpDetails.park_name==rec.park_name,
                                                      MhpDetails.address_line_1==rec.address_line_1)).all()
            if len(match_rec)>1:
                for recs in match_rec[1:]:
                    dups.append(recs.park_name)
                    db.delete(recs)
        db.commit()
    except Exception as e:
        print(f"Error occurred{e}")
        db.rollback()
    return dups

def remove_rec(db:Session,parkname):
    record = db.query(MhpDetails).filter(MhpDetails.park_name == parkname).first()
    try:
        if record:
            db.delete(record)
        db.commit()
    except Exception as e:
        print(f'Error {e}')
        db.rollback()
    return {"message":"Data deleted"}




async def csv_read(file: UploadFile, db: Session) -> Dict[str, str]:
    if not file.filename.endswith('csv'):
        raise ValueError('Allowed file type is csv')

    contents = await file.read()
    data = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    data_to_add=[]
    try:
        for index,row in data.iterrows():
            record_dict = {
                "parkname": row['park_name'],
                "address":{
                "address_line1": row['address_line1'],
                "address_line2": row['address_line2']},
                "city": row['city'],
                "zip": row['zip'],
                "state": row['state']
            }

            data_add = MhpDetails_schema(**record_dict)
            data_add_addr=data_add.address

            new_data = MhpDetails(park_name=data_add.parkname,
                                  city=data_add.city,
                                  state=data_add.state,
                                  zip=data_add.zip,
                                  address_line_1=data_add_addr.address_line1,
                                  address_line_2=data_add_addr.address_line2)
            data_to_add.append(new_data)

        if data_to_add:
            for data in data_to_add:
                db.add(data)
                # db.refresh(data)
            db.commit()


        return {"Message": "Data imported successfully"}

    except Exception as e:
        db.rollback()
        print(f"Please see the error message here: {e}")
        raise

    finally:
        db.close()

def park_count(db:Session):
    statewise_count=db.query(MhpDetails.state, func.count(MhpDetails.state)).group_by(MhpDetails.state).all()
    total_count=db.query(MhpDetails.park_name).count()
    state_count=db.query(MhpDetails.state).distinct().count()
    statewise_count=dict(statewise_count)
    # statewise_count = [{column: value for column, value in row.items()} for row in statewise_count]
    return {"Park Summary":[{'Total_Parks':total_count,
                             'Total_state':state_count,
                             'Parks_by_state':statewise_count}]}

def bar_plot(data,title,xlabel,ylable,sort_order):
    if sort_order=='asc':
        data=dict(sorted(data.items(),key=lambda x:x[1]))
    elif sort_order=='desc':
        data=dict(sorted(data.items(),key=lambda x:x[1],reverse=True))
    elif sort_order=='bell':
        n=len(data)//2
        first_group=dict(sorted(list(data.items())[:n],key=lambda x:x[1]))
        second_group=dict(sorted(list(data.items())[n:],key=lambda x:x[1],reverse=True))
        data={**first_group,**second_group}
    plt.figure(figsize=(len(data) * 0.3, 6))
    bars=plt.bar(data.keys(),data.values())
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylable)
    for bar in bars:
        bar.set_edgecolor("black")
    image=io.BytesIO()
    plt.savefig(image,format='png')
    image.seek(0)
    return StreamingResponse(image, media_type="image/png")

def bar_graph(db:Session,name:Graph):

    statewise_count=db.query(MhpDetails.state, func.count(MhpDetails.park_name)).group_by(MhpDetails.state).all()
    data = {state: count for state, count in statewise_count}
    return bar_plot(data,title=name.title,xlabel=name.xlable,ylable=name.ylable,sort_order=name.sort_ord)

def download_data(data):
    file_obj=io.StringIO()
    writer = csv.writer(file_obj, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(['park_name', 'address_line_1', 'address_line_2', 'city', 'zip', 'state'])
    for row in data:
        writer.writerow([
            row.park_name,
            row.address_line_1,
            row.address_line_2,
            row.city,
            row.zip,
            row.state
        ])
    file_obj.seek(0)
    data=file_obj.getvalue()

    return StreamingResponse(io.BytesIO(data.encode('utf-8')), media_type='text/csv',
                             headers={'Content-Disposition': 'attachment; filename=data.csv'})
    # data_.headers['Content-Disposition']="attachment; filename=data.csv"



def del_db_records(db:Session):
    data= db.query(MhpDetails).all()
    if data:
        for records in data:
            db.delete(records)
        db.commit()
        return {"Message" : "Data removed successfully"}
    else:
        return {"Message": "Data removal unsuccessfull"}





def converter(new_data):
    return {
        "parkname": new_data.park_name,
        "address": {
            "address_line1": new_data.address_line_1,
            "address_line2": new_data.address_line_2
        },
        "city": new_data.city,
        "state": new_data.state,
        "zip": new_data.zip
    }

def converterfrom_db(data):
    l=[]
    for new_data in data:
        l.append({
        "parkname": new_data.park_name,
        "address": {
            "address_line1": new_data.address_line_1,
            "address_line2": new_data.address_line_2
        },
        "city": new_data.city,
        "state": new_data.state,
        "zip": new_data.zip
        })
    return l

def add_contact_data_service(data,db:Session):
    new_data=data.dict()
    data_db={
        'address_fk':new_data['address_fk'],
        'website':new_data['website'],
        'contact_person':new_data['contact_person'],
        'email':new_data['email'],
        'phone':new_data['phone']
    }
    try:
        data_chk=db.query(Mhpcontact).filter(Mhpcontact.address_fk==data_db['address_fk']).first()
        if data_chk:
            raise HTTPException(status_code=400,detail="Address exist in the db")
        else:
            db.add(Mhpcontact(**data_db))
            db.commit()
            db.refresh(Mhpcontact)
            return data_db
    except HTTPException as e:
        print(f"An error occurred {e}")

def converter_contact(data):
    return{'address_fk':data['address_fk'],
           'website':data['website'],
           'contact_person':data['contact_person'],
           'email':data['email'],
           'phone':data['phone']}


async def bulkupload(file:UploadFile,db:Session):
    if not file.filename.endswith('.csv'):
        raise TypeError("Incorrect File extension")
    content=await file.read()
    df=pd.read_csv(io.StringIO(content.decode('utf-8')))
    df = df.where(pd.notna(df), None)
    if not df.empty:
        existing_data=[]
        for index, records in df.iterrows():
            new_record=records.to_dict()
            validated_info=MhpContact_schema(**new_record)
            # adding it to db model before add it to db
            db_data = {
                'address_fk': validated_info.address_fk,
                'website': validated_info.website,
                'contact_person': validated_info.contact_person,
                'email': validated_info.email,
                'phone': validated_info.phone
            }
            db_model_data=Mhpcontact(**db_data)
            # check for exisiting data
            db_query=db.query(Mhpcontact).filter(Mhpcontact.address_fk==db_data['address_fk']).first()
            if db_query:
                existing_data.append(db_data)
            else:
                db.add(db_model_data)
        db.commit()
        if existing_data:
            return {"data": existing_data, 'status': 'existing records found'}
        else:
            return {'status': 'all records successfully added'}
    else:
        raise HTTPException(status_code=400,detail="No data found in the csv")


def query_parkname(name, db:Session):
    db_query=db.query(MhpDetails).filter(MhpDetails.park_name==name).first()
    # if db_query:
    #     print(f"park_name:{db_query.park_name}")
    #     for con in db_query.park_details_rel:
    #         cont_per=con.contact_person if con.contact_person is not None else "Not found "
    #         print(f"park_rel: {cont_per}")
    return [db_query]

def converter_parkname(data):
    l=[]
    for new_data in data:
        contact=new_data.park_details_rel[0] if new_data.park_details_rel else None
        contact_person_ = contact.contact_person if contact.contact_person is not None else "Not provided "
        email = contact.email if contact.email is not None else " Not provided "
        phone = contact.phone if contact.phone is not None  else "Not provided "
        website = contact.website if contact.website is not None else "Not provided "

        l.append({"park_details":{
            "parkname": new_data.park_name,
            "address": {
                "address_line1": new_data.address_line_1,
                "address_line2": new_data.address_line_2
            },
            "city": new_data.city,
            "state": new_data.state,
            "zip": new_data.zip},
            "contacts": {
                'contact_person': contact_person_,
                'email': email,
                'phone': phone,
                'website': website
            }
        })
    return l



async def csv_data_reader_handler(file: UploadFile,db:Session,schema:Type[BaseModel],model: Type,
                                  uniqueField: str):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400,detail="Accepted only csv")
    content=await file.read()
    df=pd.read_csv(io.StringIO(content.decode('utf-8')))
    df=df.where(pd.notna(df),None)
    existing_data=[]

    if df.empty:
        raise HTTPException(status_code=400,detail="Empty csv file")
    for row in df.itertuples():
        data_to_add=row._asdict() if hasattr(row,'_asdict') else row._fields
        validate_data=schema(**data_to_add)

        if hasattr(validate_data,'dict'):
            validate_data=validate_data.dict()

        db_query=db.query(model).filter(getattr(model,uniqueField)==validate_data[uniqueField]).first()
        if not db_query:
            db.add(model(**validate_data))
        else:
            existing_data.append(validate_data)
    db.commit()
    return {"Data_added_status":{"Stat":[{'New_records':len(df[uniqueField])-len(existing_data),
                                         'Old_records':len(existing_data)}]}}








