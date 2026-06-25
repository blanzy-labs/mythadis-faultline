from collections.abc import Callable

from app.config import Settings
from app.faultline.modes import ScanModeId, get_scan_mode
from app.faultline.parser import parse_audit_report, parse_scanner_report
from app.faultline.prompts import build_auditor_prompt, build_scanner_prompt
from app.faultline.schemas import (
    AuditReport,
    ModelsUsed,
    ProviderName,
    ScanRequest,
    ScanResponse,
    ScannerReport,
)
from app.providers import BaseProvider, get_provider

ProviderFactory = Callable[[str, Settings], BaseProvider]


async def run_primary_scanner(
    user_input: str,
    scan_mode_id: str | ScanModeId,
    scanner_provider_name: str | ProviderName,
    settings: Settings,
    provider_factory: ProviderFactory = get_provider,
) -> ScannerReport:
    scan_mode = get_scan_mode(scan_mode_id)
    provider = provider_factory(str(scanner_provider_name), settings)
    raw_response = await provider.generate(
        build_scanner_prompt(user_input, scan_mode)
    )
    return parse_scanner_report(raw_response)


async def run_auditor(
    user_input: str,
    scan_mode_id: str | ScanModeId,
    scanner_report: ScannerReport,
    auditor_provider_name: str | ProviderName,
    settings: Settings,
    provider_factory: ProviderFactory = get_provider,
) -> AuditReport:
    scan_mode = get_scan_mode(scan_mode_id)
    provider = provider_factory(str(auditor_provider_name), settings)
    raw_response = await provider.generate(
        build_auditor_prompt(user_input, scan_mode, scanner_report)
    )
    return parse_audit_report(raw_response)


async def run_faultline(
    request: ScanRequest,
    settings: Settings,
    provider_factory: ProviderFactory = get_provider,
) -> ScanResponse:
    scanner_report = await run_primary_scanner(
        user_input=request.input,
        scan_mode_id=request.scan_mode,
        scanner_provider_name=request.scanner_provider,
        settings=settings,
        provider_factory=provider_factory,
    )
    audit_report = await run_auditor(
        user_input=request.input,
        scan_mode_id=request.scan_mode,
        scanner_report=scanner_report,
        auditor_provider_name=request.auditor_provider,
        settings=settings,
        provider_factory=provider_factory,
    )

    return ScanResponse(
        input=request.input,
        scan_mode=request.scan_mode,
        scanner_report=scanner_report,
        audit_report=audit_report,
        models_used=ModelsUsed(
            scanner_provider=request.scanner_provider,
            scanner_model=_model_for_provider(request.scanner_provider, settings),
            auditor_provider=request.auditor_provider,
            auditor_model=_model_for_provider(request.auditor_provider, settings),
        ),
    )


def _model_for_provider(provider_name: ProviderName, settings: Settings) -> str:
    if provider_name == ProviderName.OPENAI:
        return settings.OPENAI_MODEL
    if provider_name == ProviderName.OPENAI_COMPATIBLE:
        return settings.LOCAL_LLM_MODEL
    return settings.GEMINI_MODEL
