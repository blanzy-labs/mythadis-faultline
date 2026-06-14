from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.config import Settings, get_settings
from app.faultline.schemas import ScanRequest, ScanResponse
from app.faultline.service import ProviderFactory, run_faultline
from app.providers import (
    ProviderCallError,
    ProviderConfigError,
    ProviderError,
    UnsupportedProviderError,
    get_provider,
)

router = APIRouter(prefix="/faultline", tags=["faultline"])


def get_provider_factory() -> ProviderFactory:
    return get_provider


@router.post("/run", response_model=ScanResponse)
async def run_faultline_endpoint(
    request: ScanRequest,
    settings: Annotated[Settings, Depends(get_settings)],
    provider_factory: Annotated[ProviderFactory, Depends(get_provider_factory)],
) -> ScanResponse:
    try:
        return await run_faultline(request, settings, provider_factory)
    except (UnsupportedProviderError, ProviderConfigError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from None
    except ProviderCallError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from None
    except ProviderError:
        raise HTTPException(
            status_code=500,
            detail="Faultline workflow failed.",
        ) from None
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Faultline workflow failed.",
        ) from None
