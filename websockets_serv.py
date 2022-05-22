import asyncio
import websockets
import json
from models import User, Products, Categories, Comment
from create_app import db

active_users = []


def start_websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    main_coro = main()
    loop.run_until_complete(main_coro)
    loop.run_forever()


def get_user_name(id):
    return User.query.get(int(id)).name


async def main():
    async with websockets.serve(ws_handler, "localhost", 5050, ping_interval=None):
        await asyncio.Future()


async def ws_handler(websocket):
    prod_id = None
    user_id = None
    while True:
        try:
            async for message in websocket:
                data = json.loads(message)
                try:
                    product = Products.query.filter_by(id=int(data["product_id"])).first()
                    user = User.query.filter_by(id=int(data["user_id"])).first()
                except KeyError:
                    new_comm = Comment(text=data["comment"])
                    user.comments.append(new_comm)
                    product.comments.append(new_comm)
                    db.session.add(user)
                    db.session.add(product)
                    db.session.commit()
                    a = 0
                await add_active_user(websocket, user.id, product.id)
        except websockets.ConnectionClosedOK:
            await remove_active_user(websocket, user_id, prod_id)
        finally:
            break


async def add_active_user(websocket, user_id, prod_id):
    active_users.append((websocket, user_id, prod_id))
    await show_comments(prod_id)


async def remove_active_user(websocket, user_id, prod_id):
    try:
        del active_users[active_users.index((websocket, user_id, prod_id))]
    except Exception:
        pass


async def show_comments(prod_id):
    product = Products.query.filter_by(id=int(prod_id)).first()
    to_send = dict()
    for com in product.comments:
        username = get_user_name(com.user_id)
        try:
            to_send[username].append(com.text)
        except KeyError:
            to_send[username] = list()
            to_send[username].append(com.text)
    await asyncio.wait([user[0].send(json.dumps(to_send)) for user in active_users if user[2] == prod_id])
