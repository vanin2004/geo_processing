from src.services import AlgorithmAbstractFactory


def get_algorithm_factory() -> type[AlgorithmAbstractFactory]:
    """Зависимость для получения фабрики алгоритмов."""
    return AlgorithmAbstractFactory
