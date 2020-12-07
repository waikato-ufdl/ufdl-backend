"""
Defines the settings for the UFDL HTML client.
"""
from ufdl.core_app.settings import UFDLSettings, UFDLBoolSetting


class UFDLHTMLClientSettings(UFDLSettings):
    """
    The settings for the core UFDL app.
    """
    @classmethod
    def namespace(cls) -> str:
        return "UFDL_HTML_CLIENT"

    # Whether to actually serve the client
    SERVE_CLIENT: bool = UFDLBoolSetting(True)


# Create a singleton instance to export
html_client_settings: UFDLHTMLClientSettings = UFDLHTMLClientSettings()
