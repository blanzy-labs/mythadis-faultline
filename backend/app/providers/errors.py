class ProviderError(Exception):
    """Base exception for controlled provider failures."""


class ProviderConfigError(ProviderError):
    """Raised when a provider is not configured for use."""


class ProviderCallError(ProviderError):
    """Raised when a provider request fails or returns unusable content."""


class UnsupportedProviderError(ProviderError):
    """Raised when a requested provider is not supported."""
