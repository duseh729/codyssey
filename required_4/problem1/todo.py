# todo.py
from fastapi import FastAPI, APIRouter
from typing import Dict, List

app = FastAPI()
router = APIRouter()

# 메모리상 Todo 리스트
todo_list: List[Dict[str, str]] = []


@router.post("/add_todo")
def add_todo(item: Dict[str, str]):
    """
    새로운 todo 항목을 추가한다.
    예: {"task": "공부하기"}
    """
    todo_list.append(item)
    return {"message": "추가 완료", "todo_list": todo_list}


@router.get("/retrieve_todo")
def retrieve_todo() -> Dict[str, List[Dict[str, str]]]:
    """
    현재 todo 리스트를 반환한다.
    """
    return {"todo_list": todo_list}


# 라우터 등록
app.include_router(router)

# (직접 실행할 때만 작동)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("todo:app", host="0.0.0.0", port=8000, reload=True)
