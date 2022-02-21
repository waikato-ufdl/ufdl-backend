import importlib
import re
from typing import Dict, List, NoReturn, Optional, Tuple

from ufdl.jobcontracts.initialise import initialise_server as initialise_contracts

from ufdl.jobtypes.initialise import (
    initialise_server as initialise_types,
    ListFunction,
    DownloadFunction
)

from ufdl.json.core.filter import FilterSpec

from wai.json.raw import RawJSONElement

from ..filter import filter_list_request
from ..views._UFDLBaseViewSet import UFDLBaseViewSet


def err(*args, **kwargs) -> NoReturn:
    raise Exception(
        f"Attempted to call database function when not initialised\n"
        f"{args}\n"
        f"{kwargs}"
    )


def get_cls(cls: str):
    mod, cls_name = cls.rsplit(".", 1)
    mod = importlib.import_module(mod)
    return getattr(mod, cls_name)


VIEWSET_FINDER: Optional[Tuple[Tuple[re.Pattern, UFDLBaseViewSet], ...]] = None
FOUND_VIEWSETS: Dict[str, UFDLBaseViewSet] = {}


def find_viewset(table_name: str) -> Optional[UFDLBaseViewSet]:
    global VIEWSET_FINDER, FOUND_VIEWSETS

    if table_name in FOUND_VIEWSETS:
        return FOUND_VIEWSETS[table_name]

    if VIEWSET_FINDER is not None:
        for pattern, viewset in VIEWSET_FINDER:
            if pattern.fullmatch(table_name):
                FOUND_VIEWSETS[table_name] = viewset
                return viewset
        return None

    from ..urls import router
    VIEWSET_FINDER = tuple(
        (re.compile(prefix), viewset)
        for prefix, viewset, _ in router.registry
    )

    return find_viewset(table_name)


def list_function(table_name: str, filter_spec: FilterSpec) -> List[RawJSONElement]:
    viewset = find_viewset(table_name)
    if viewset is None:
        raise Exception(f"Could not find view-set for '{table_name}'")
    queryset = filter_list_request(viewset.queryset, filter_spec)
    serialiser = viewset.serializer_class()
    return [
        serialiser.to_representation(value)
        for value in queryset.all()
    ]


def download_function(table_name: str, pk: int) -> bytes:
    raise NotImplementedError()


def initialise(
        job_type_model,
        job_contract_model,
        list_function: ListFunction = list_function,
        download_function: DownloadFunction = download_function
):
    initialise_types(
        list_function,
        download_function,
        {
            job_type.name: get_cls(job_type.cls)
            for job_type in job_type_model.objects.all()
        }
    )

    initialise_contracts({
        job_contract.name: get_cls(job_contract.cls)
        for job_contract in job_contract_model.objects.all()
    })