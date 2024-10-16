import logging
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os
import aiofiles
import json
from helpers import (
    dc_1,
    dc_2,
    dc_3,
    dc_3_1,
    dc_3_2,
    dc_3_3,
    dc_3_4,
    dc_3_4_ending,
    dc_3_5,
    dc_3_5_1,
    dc_3_5_2,
    dc_3_5_3,
    dc_3_5_4,
    dc_3_5_5,
    dc_3_5_6,
    dc_3_6,
    dc_4,
    dc_5,
    dc_5_1,
    dc_5_2,
    dc_5_3,
    dc_5_4,
    dc_5_5,
    dc_5_6,
    dc_5_7,
    dc_5_8,
    dc_5_9,
    dc_5_9_1,
    dc_5_10,
    dc_6,
    dc_7,
    dc_7_ending,
    dc_8,
    dc_9
)


logging.basicConfig(format="%(levelname)s     %(message)s", level=logging.INFO)
# hack to get rid of langchain logs
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)

app = FastAPI()


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIRECTORY = "uploads"  # Make sure this directory exists

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@app.get("/")
async def root():
    return {"msg": "OK"}

@app.post("/upload_files")
async def upload_files( 
    policy_packet: UploadFile = File(...),
    vendors_list: UploadFile = File(...),
    data_policy: UploadFile = File(...),
    company_name: str = Form(...)
):
    # Save policy packet
    try:
        # Save policy packet
        policy_packet_path = os.path.join(UPLOAD_DIRECTORY, f"{company_name}_policy_packet.pdf")
        async with aiofiles.open(policy_packet_path, "wb") as buffer:
            await buffer.write(await policy_packet.read())  # Read in binary mode

        # Save vendors list
        vendors_list_path = os.path.join(UPLOAD_DIRECTORY, f"{company_name}_vendors.xlsx")
        async with aiofiles.open(vendors_list_path, "wb") as buffer:
            await buffer.write(await vendors_list.read())  # Read in binary mode

        # # Save data policy
        data_policy_path = os.path.join(UPLOAD_DIRECTORY, f"{company_name}_data_policy.pdf")
        async with aiofiles.open(data_policy_path, "wb") as buffer:
            await buffer.write(await data_policy.read())  # Read in binary mode



        return {"message": "Files uploaded successfully!"}

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return {"message": "An error occurred while uploading the files."}


class CompanyData(BaseModel):
    name: str
    website: str
    report: str
    system_name: str
    hire_days: str
    revoke_days: str
    provider: str
    incidents: bool
    changes : bool


async def generate_response(company: CompanyData) -> AsyncGenerator[dict, None]:
    # Simulate some async processing
    response_1 = await dc_1(company.name, company.website)
    yield json.dumps(response_1) + "\n"  # Yield first response

    response_2 = dc_2(company.name, company.report)
    yield json.dumps(response_2) + "\n"

    response_3 = dc_3()
    yield json.dumps(response_3) + "\n"

    # Do no have enough information to Generate DC 3.1, need to get filled by client
    response_3_1 = dc_3_1(company.name)
    yield json.dumps(response_3_1) + "\n"

    # Need to pass list of vendors from vanta
    response_3_2 = await dc_3_2(company.name, company.system_name)
    yield json.dumps(response_3_2) + "\n"

    # Do no have enough information to Generate DC 3.3, need to get filled by client
    response_3_3 = dc_3_3()
    yield json.dumps(response_3_3) + "\n"

    # Will have to pass file of CC 5.2 data management policy
    response_3_4 = await dc_3_4(company.name)
    yield json.dumps(response_3_4) + "\n"

    response_3_4_ending = dc_3_4_ending(company.name)
    yield json.dumps(response_3_4_ending) + "\n"

    # Will have to pass file of Policy packet
    response_3_5 = await dc_3_5(company.name)
    yield json.dumps(response_3_5) + "\n"

    response_3_5_1 = dc_3_5_1(company.name, company.provider)
    yield json.dumps(response_3_5_1) + "\n"

    response_3_5_2 = dc_3_5_2(company.name, company.hire_days, company.revoke_days)
    yield json.dumps(response_3_5_2) + "\n"

    response_3_5_3 = dc_3_5_3(company.provider)
    yield json.dumps(response_3_5_3) + "\n"

    response_3_5_4 = dc_3_5_4(company.name)
    yield json.dumps(response_3_5_4) + "\n"

    response_3_5_5 = dc_3_5_5(company.name)
    yield json.dumps(response_3_5_5) + "\n"

    response_3_5_6 = dc_3_5_6(company.name)
    yield json.dumps(response_3_5_6) + "\n"

    response_3_6 = dc_3_6(company.system_name, company.provider)
    yield json.dumps(response_3_6) + "\n"

    response_4 = dc_4(company.incidents)
    yield json.dumps(response_4) + "\n"

    response_5 = dc_5()
    yield json.dumps(response_5) + "\n"

    response_5_1 = dc_5_1(company.name)
    yield json.dumps(response_5_1) + "\n"

    response_5_2 = dc_5_2(company.name)
    yield json.dumps(response_5_2) + "\n"

    response_5_3 = dc_5_3(company.name)
    yield json.dumps(response_5_3) + "\n"

    response_5_4 = dc_5_4(company.name)
    yield json.dumps(response_5_4) + "\n"

    # # Pass the Policy Packet
    response_5_5 = await dc_5_5(company.name)
    yield json.dumps(response_5_5) + "\n"

    response_5_6 = dc_5_6(company.name)
    yield json.dumps(response_5_6) + "\n"

    response_5_7 = dc_5_7(company.name)
    yield json.dumps(response_5_7) + "\n"

    response_5_8 = dc_5_8(company.name)
    yield json.dumps(response_5_8) + "\n"

    response_5_9 = dc_5_9(company.name)
    yield json.dumps(response_5_9) + "\n"

    response_5_9_1 = dc_5_9_1(company.name)
    yield json.dumps(response_5_9_1) + "\n"

    response_5_10 = dc_5_10()
    yield json.dumps(response_5_10) + "\n"

    response_6 = dc_6(company.name, company.report)
    yield json.dumps(response_6) + "\n"

    response_7 = dc_7(company.name,  company.provider, company.report)
    yield json.dumps(response_7) + "\n"

    response_7_ending = dc_7_ending(company.name)
    yield json.dumps(response_7_ending) + "\n"

    response_8 = dc_8(company.name, company.system_name)
    yield json.dumps(response_8) + "\n"

    response_9 = dc_9(company.changes)
    yield json.dumps(response_9) + "\n"

@app.post("/generate")
async def generate(company: CompanyData,
                   ):
    return StreamingResponse(generate_response(company), media_type="application/json")
