"""
New Plugin for RotorHazard
"""
import logging
from eventmanager import Evt

logger = logging.getLogger(__name__)

def initialize(rhapi):
    """Called by RotorHazard during server startup.

    Register event handlers here — do NOT add behaviors directly.
    The rhapi object provides full access to the timer's API.
    See: RotorHazard/doc/RHAPI.md
    """
    logger.info("New Plugin: Initializing...")

    # --- Register event handlers ---
    # Synchronous (priority < 100) — blocks until complete
    rhapi.events.on(Evt.STARTUP, on_startup)

    # Asynchronous (priority >= 100) — runs in gevent greenlet
    # rhapi.events.on(Evt.RACE_START, on_race_start, priority=200)
    # rhapi.events.on(Evt.RACE_LAP_RECORDED, on_lap_recorded, priority=200)
    # rhapi.events.on(Evt.RACE_STOP, on_race_stop, priority=200)
    # rhapi.events.on(Evt.LAPS_SAVE, on_laps_save, priority=200)
    # rhapi.events.on(Evt.HEAT_SET, on_heat_set, priority=200)

    # --- Register UI panels (optional) ---
    # rhapi.ui.register_panel("new_plugin_panel", "New Plugin", "format")
    # rhapi.fields.register_option(UIField(...), "new_plugin_panel")

    # --- Register Flask blueprint for custom pages (optional) ---
    # try:
    #     from .blueprint import create_blueprint
    #     bp = create_blueprint(rhapi)
    #     rhapi.ui.blueprint_add(bp)
    # except Exception as e:
    #     logger.error(f"New Plugin: failed to register blueprint: {e}")

    logger.info("New Plugin: Initialization complete")


def on_startup(args):
    """Runs after the server is fully booted.

    Good place to:
    - Validate configuration
    - Initialize connections to external services
    - Log plugin status
    """
    logger.info("New Plugin: Server startup complete")
