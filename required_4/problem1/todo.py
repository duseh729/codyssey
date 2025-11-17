from fastapi import FastAPI, APIRouter, HTTPException
from typing import Dict, List
from model import TodoItem

app = FastAPI()
router = APIRouter()

# 메모리상 Todo 리스트 (id, task)
todo_list: List[Dict[str, str]] = []

@router.post("/add_todo")
def add_todo(item: TodoItem):
    """
    새로운 todo 항목을 추가한다.
    예: {"task": "공부하기"}
    """
    print("DEBUG ITEM:", item)
    print("DICT:", item.dict())
    new_id = len(todo_list)
    todo_list.append({"id": new_id, "task": item.task})
    return {"message": "추가 완료", "todo_list": todo_list}


@router.get("/retrieve_todo")
def retrieve_todo():
    """
    전체 todo 리스트를 반환한다.
    """
    return {"todo_list": todo_list}

@router.get("/get_single_todo/{todo_id}")
def get_single_todo(todo_id: int):
    """
    개별 todo 조회
    """
    for todo in todo_list:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@router.put("/update_todo/{todo_id}")
def update_todo(todo_id: int, updated_item: TodoItem):
    """
    todo 항목 수정
    """
    for todo in todo_list:
        if todo["id"] == todo_id:
            todo["task"] = updated_item.task
            return {"message": "수정 완료", "todo": todo}
    raise HTTPException(status_code=404, detail="Todo not found")


@router.delete("/delete_single_todo/{todo_id}")
def delete_single_todo(todo_id: int):
    """
    todo 항목 삭제
    """
    for i, todo in enumerate(todo_list):
        if todo["id"] == todo_id:
            del todo_list[i]
            return {"message": "삭제 완료", "todo_list": todo_list}
    raise HTTPException(status_code=404, detail="Todo not found")


# 라우터 등록
app.include_router(router)

# (직접 실행할 때만 작동)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("todo:app", host="0.0.0.0", port=8000, reload=True)
