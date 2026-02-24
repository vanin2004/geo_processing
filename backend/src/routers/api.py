import uuid

from fastapi import HTTPException
from fastapi.routing import APIRouter

from src.injectors.services import get_task_service
from src.models.schemas import TaskCreate, TaskRead
from src.services import (
    AlgorithmAbstractFactory,
    InvalidAlgorithmParamsError,
    TaskNotFoundError,
)

router = APIRouter(prefix="/api")


@router.get(
    "/tasks/available-algorithms",
)
def get_available_algorithms() -> dict[str, dict]:
    """Возвращает словарь {имя_алгоритма: JSON-схема параметров}."""
    return {
        name: algo_cls.get_pydantic_model().model_json_schema()
        for name, algo_cls in AlgorithmAbstractFactory.registry.items()
    }


@router.get("/tasks/")
def list_tasks() -> list[TaskRead]:

    with get_task_service() as task_service:
        """Возвращает список всех задач из базы данных."""
        return [TaskRead.model_validate(task) for task in task_service.list_tasks()]


@router.get("/tasks/{task_id}")
def get_task(
    task_id: uuid.UUID,
) -> TaskRead:
    """Возвращает информацию о задаче: статус, время выполнения, результат."""

    with get_task_service() as task_service:
        try:
            return TaskRead.model_validate(task_service.get_task(task_id))
        except TaskNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))


@router.post("/task")
def create_task(
    body: TaskCreate,
) -> TaskRead:
    try:
        algorithm = AlgorithmAbstractFactory.get_algorithm(body.algorithm)
        params = algorithm.get_pydantic_model().model_validate(body.params)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        with get_task_service() as task_service:
            task = task_service.create_task(
                algorithm=algorithm, input_file_id=body.input_file_id, params=params
            )

    except InvalidAlgorithmParamsError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return TaskRead.model_validate(task)
