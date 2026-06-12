"""Home Assistant-verktyg för Reachy Minis conversation-app.

Bryggar robotens röst-agent till Home Assistants **Assist** (conversation-API),
så talade önskemål som "släck lamporna i köket" hanteras av HA med de entiteter,
områden och intents användaren redan exponerat för röststyrning.

Körs inuti en Home Assistant add-on → når HA-kärnan via Supervisor-proxyn
(http://supervisor/core/api/...) autentiserad med SUPERVISOR_TOKEN. Add-onen
måste ha `homeassistant_api: true` i config.yaml.

Laddas automatiskt av conversation-appen via REACHY_MINI_EXTERNAL_TOOLS_DIRECTORY
+ AUTOLOAD_EXTERNAL_TOOLS=true.
"""

from __future__ import annotations

import os
import logging
from typing import Any

from reachy_mini_conversation_app.tools.core_tools import Tool, ToolDependencies

logger = logging.getLogger(__name__)

# Supervisor-proxyn till HA-kärnan. conversation/process = HA:s Assist-pipeline.
_HA_CONVERSATION_URL = "http://supervisor/core/api/conversation/process"
# Språk för Assist (kan överstyras med env). HA matchar intents/entiteter per språk.
_ASSIST_LANGUAGE = os.getenv("HA_ASSIST_LANGUAGE", "sv")


class HomeAssistant(Tool):
    """Styr och fråga användarens smarta hem via Home Assistant Assist."""

    name = "home_assistant"
    description = (
        "Control or query the user's smart home through Home Assistant. Pass a single "
        "natural-language command in the user's own language — e.g. 'släck lamporna i köket', "
        "'sätt vardagsrummet till 21 grader', 'är ytterdörren låst?', 'spela musik i köket', "
        "'aktivera scenen kväll'. Home Assistant decides what to do using only the devices and "
        "areas the user has exposed to voice control, and returns a short result that you should "
        "speak back. Use this whenever the user wants to control or check anything in their home "
        "(lights, heating, locks, covers, sensors, scenes, media players, vacuums, etc.). "
        "Do NOT use it for general conversation."
    )
    parameters_schema = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": (
                    "The home-control request as one natural-language sentence in the user's "
                    "language, phrased exactly as an instruction to a voice assistant."
                ),
            },
        },
        "required": ["command"],
    }

    async def __call__(self, deps: ToolDependencies, **kwargs: Any) -> dict[str, Any]:
        """Skicka kommandot till HA:s Assist och returnera svaret att tala upp."""
        command = kwargs.get("command")
        if not isinstance(command, str) or not command.strip():
            return {"ok": False, "result": "Tomt kommando."}

        token = os.getenv("SUPERVISOR_TOKEN")
        if not token:
            logger.error("home_assistant: SUPERVISOR_TOKEN saknas")
            return {"ok": False, "result": "Home Assistant går inte att nå (ingen Supervisor-token)."}

        payload = {"text": command.strip(), "language": _ASSIST_LANGUAGE}
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        try:
            import httpx

            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(_HA_CONVERSATION_URL, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
        except Exception as e:  # noqa: BLE001
            logger.exception("home_assistant: anrop misslyckades")
            return {"ok": False, "result": f"Home Assistant-anropet misslyckades: {e}"}

        response = data.get("response", {}) if isinstance(data, dict) else {}
        speech = (
            response.get("speech", {}).get("plain", {}).get("speech")
            if isinstance(response, dict)
            else None
        )
        resp_type = response.get("response_type") if isinstance(response, dict) else None
        logger.info("home_assistant: command=%r response_type=%s", command[:120], resp_type)

        if resp_type == "error":
            return {"ok": False, "result": speech or "Home Assistant kunde inte hantera det."}
        return {"ok": True, "result": speech or "Klart."}
