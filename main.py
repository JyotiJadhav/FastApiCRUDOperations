import firebase_admin
from firebase_admin import credentials, db
from fastapi import FastAPI

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fastapi-test-d62a8-default-rtdb.firebaseio.com/'
})

app = FastAPI()

@app.post("/users/")
async def create_user(first_name: str, last_name: str):
    users_ref = db.reference('users')

    new_user_id = users_ref.push().key

    user_data = {
        'id': new_user_id,
        'first_name': first_name,
        'last_name': last_name
    }

    users_ref.child(new_user_id).set(user_data)

    return {"message": "User created successfully"}


@app.get("/users/")
async def get_users():
    users_ref = db.reference('users')
    users = users_ref.get()
    return users or {}

@app.delete("/users/{user_id}/")
async def delete_user(user_id: str):
    users_ref = db.reference('users')

    # Check if the user exists
    user = users_ref.child(user_id).get()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user
    users_ref.child(user_id).delete()
    return {"message": f"User with ID {user_id} has been deleted"}


@app.put("/users/{user_id}/")
async def update_user(user_id: str, first_name: str, last_name: str):
    users_ref = db.reference('users')

    # Check if the user exists
    user = users_ref.child(user_id).get()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user data
    updated_data = {
        'id': user_id,
        'first_name': first_name,
        'last_name': last_name
    }
    users_ref.child(user_id).update(updated_data)

    return {"message": f"User with ID {user_id} has been updated"}
