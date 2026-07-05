from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Memory
from security import get_current_user
from schemas import MemoryCreate
from schemas import MemoryUpdate

router = APIRouter()


@router.post("/memories")
def create_memory(

    data: MemoryCreate,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    memory = Memory(

        user_id=current_user.id,

        memory_key=data.memory_key,

        memory_value=data.memory_value

    )

    db.add(memory)

    db.commit()

    db.refresh(memory)

    return memory


@router.put("/memories/{id}")
def update_memory(

    id:int,

    data:MemoryUpdate,

    db:Session=Depends(get_db),

    current_user=Depends(get_current_user)

):

    memory=db.query(

        Memory

    ).filter(

        Memory.id==id,

        Memory.user_id==current_user.id

    ).first()

    if not memory:

        return {"success":False}

    memory.memory_key=data.memory_key

    memory.memory_value=data.memory_value

    db.commit()

    db.refresh(memory)

    return memory


@router.delete("/memories/{id}")
def delete_memory(

    id:int,

    db:Session=Depends(get_db),

    current_user=Depends(get_current_user)

):

    memory=db.query(

        Memory

    ).filter(

        Memory.id==id,

        Memory.user_id==current_user.id

    ).first()

    if not memory:

        return {"success":False}

    db.delete(memory)

    db.commit()

    return {"success":True}

@router.delete("/memories")
def delete_all_memories(

    db:Session=Depends(get_db),

    current_user=Depends(get_current_user)

):

    db.query(

        Memory

    ).filter(

        Memory.user_id==current_user.id

    ).delete()

    db.commit()

    return {"success":True}