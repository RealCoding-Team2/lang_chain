from multiprocessing import Pool
from typing import Callable, List, Dict, Any, Optional, Tuple


def run_parallel_jobs(
    func: Callable[[Any], Optional[Dict[str, str]]],
    data_list: List[Any],
    num_workers: int = 4,
) -> Tuple[List[Dict[str, str]], List[Any]]:
    """
    병렬 처리로 작업을 수행하고 성공/실패 결과를 분리해서 반환합니다.

    :param func: 처리할 함수 (예: get_article_body)
    :param data_list: 처리할 데이터 목록 (예: 뉴스 URL 리스트)
    :param num_workers: 병렬 워커 수
    :return: (성공한 결과 리스트, 실패한 입력값 리스트)
    """
    success_list = []
    failed_list = []

    with Pool(processes=num_workers) as pool:
        # 함수와 인자를 함께 전달
        wrapped_inputs = [(func, item) for item in data_list]
        for result, original in zip(pool.imap_unordered(_wrapped_worker, wrapped_inputs), data_list):
            if result is not None:
                success_list.append(result)
            else:
                failed_list.append(original)

    return success_list, failed_list


def _wrapped_worker(pair: Tuple[Callable[[Any], Optional[Dict[str, str]]], Any]) -> Optional[Dict[str, str]]:
    """
    Pickle-safe 최상위 함수로, multiprocessing에서 안전하게 동작.
    """
    func, item = pair
    try:
        return func(item)
    except Exception:
        return None
