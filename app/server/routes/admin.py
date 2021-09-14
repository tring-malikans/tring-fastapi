from fastapi import Body, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext

from server.database.database import *
#from app.server.auth.admin import validate_login
from server.auth.jwt_handler import signJWT
from server.database.database import add_admin
from server.models.admin import *

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

@router.post("/login")
async def admin_login(admin_credentials: HTTPBasicCredentials = Body(...)):
    # NEW CODE
    admin_user = admin_collection.find_one({"email": admin_credentials.username})
    if (admin_user):
        id=str(admin_user['_id'])
        password = hash_helper.verify(
            admin_credentials.password, admin_user["password"])
        if (password):
            return signJWT(admin_credentials.username,id)

        return "Incorrect email or password"

    return "Incorrect email or password"

    # OLD CODE 
    # if validate_login(admin):
    #     return {
    #         "email": admin.username,
    #         "access_token": signJWT(admin.username)
    #     }
    # return "Invalid Login Details!"

@router.post("/")
async def admin_signup(admin: AdminModel = Body(...)):
    # admin_exists = await admin_collection.find_one({"email":  admin.email}, {"_id": 0})
    # if(admin_exists):
    #     return "Email already exists"
    
    admin.password = hash_helper.encrypt(admin.password)
    new_admin = await add_admin(jsonable_encoder(admin))
    return new_admin


@router.get("/{id}", response_description="User data retrieved")
async def get_user_data(id):
    user = await retrieve_user(id)
    return ResponseModel(user, "User data retrieved successfully") \
        if user \
        else ErrorResponseModel("An error occured.", 404, "User doesn'exist.")


@router.put("/{id}")
async def update_user_fav_coin(id: str,req:UpdateAdminModel= Body(...)):
    print(req)
    updated_user = await update_fav_coin_user(id, req.dict(exclude_unset=True))
    user = await retrieve_user(id)
    return ResponseModel(user, "User data retrieved successfully") \
        if user \
        else ErrorResponseModel("An error occured.", 404, "User doesn'exist.")
    # return ResponseModel(updated_user, "orders data retrieved successfully") \
    #     if len(orders) > 0 \
    #     else ResponseModel(orders, "Empty list returned")
    # return ResponseModel("order with ID: {} status update is successful".format(id),
    #                      "order status updated successfully") \
    #     if updated_order \
    #     else ErrorResponseModel("An error occurred", 404, "There was an error updating the order.".format(id))
