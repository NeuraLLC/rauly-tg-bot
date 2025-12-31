import os
import asyncio
from telethon import TelegramClient, events, functions, types
from telethon.tl.functions.channels import JoinChannelRequest, GetParticipantRequest
from telethon.tl.types import ChannelParticipantCreator, ChannelParticipantAdmin
from dotenv import load_dotenv
from db import get_session, Group, User, AdminRole
from logger import logger
from telethon.errors import FloodWaitError
import datetime

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE_NUMBER')
SESSION_PATH = os.getenv('SESSION_PATH', 'rauly_session')

client = TelegramClient(SESSION_PATH, API_ID, API_HASH)

async def join_group(group_link):
    try:
        entity = await client.get_entity(group_link)
        await client(JoinChannelRequest(entity))
        logger.info(f"Successfully joined {group_link}")
        return entity
    except FloodWaitError as e:
        logger.warning(f"FloodWait tracking: Must wait for {e.seconds} seconds")
        await asyncio.sleep(e.seconds)
        return await join_group(group_link)
    except Exception as e:
        logger.error(f"Error joining group {group_link}: {e}")
        return None

async def scan_admins(group_entity):
    session = get_session()
    
    # Store/Update Group
    db_group = session.query(Group).filter_by(tg_id=str(group_entity.id)).first()
    if not db_group:
        db_group = Group(
            tg_id=str(group_entity.id),
            title=group_entity.title,
            username=getattr(group_entity, 'username', None)
        )
        session.add(db_group)
    
    db_group.last_scanned = datetime.datetime.now()
    session.commit()

    try:
        async for participant in client.iter_participants(group_entity, filter=types.ChannelParticipantsAdmins):
            user = participant.user
            
            # Store/Update User
            db_user = session.query(User).filter_by(tg_id=str(user.id)).first()
            if not db_user:
                db_user = User(
                    tg_id=str(user.id),
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name
                )
                session.add(db_user)
            else:
                db_user.username = user.username
                db_user.first_name = user.first_name
                db_user.last_name = user.last_name
            
            session.commit()

            # Store Role
            role_str = 'admin'
            if isinstance(participant, ChannelParticipantCreator):
                role_str = 'creator'
            
            db_role = session.query(AdminRole).filter_by(group_id=db_group.id, user_id=db_user.id).first()
            if not db_role:
                db_role = AdminRole(
                    group_id=db_group.id,
                    user_id=db_user.id,
                    role=role_str,
                    custom_title=getattr(participant, 'rank', None)
                )
                session.add(db_role)
                logger.info(f"Added new admin {db_user.username or db_user.tg_id} for {db_group.title}")
            else:
                db_role.role = role_str
                db_role.custom_title = getattr(participant, 'rank', None)
            
            session.commit()
            
    except FloodWaitError as e:
        logger.warning(f"FloodWait during scan: Waiting {e.seconds} seconds")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        logger.error(f"Error scanning admins for {group_entity.title}: {e}")
    finally:
        session.close()

async def main():
    await client.start(phone=PHONE)
    # Testing logic can go here
    
if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
