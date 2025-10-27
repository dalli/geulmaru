"""Shutdown signal handler for graceful termination."""
import signal
import logging

logger = logging.getLogger(__name__)

# Global flag for shutdown
_shutdown_requested = False


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    global _shutdown_requested
    signal_names = {signal.SIGINT: "SIGINT", signal.SIGTERM: "SIGTERM"}
    signal_name = signal_names.get(signum, "UNKNOWN")
    
    logger.info(f"Received {signal_name}. Initiating graceful shutdown...")
    _shutdown_requested = True
    
    # Allow the application to finish current operation
    # Exit gracefully on next iteration or completion


def setup_signal_handlers():
    """Setup signal handlers for graceful shutdown."""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    logger.debug("Signal handlers registered for graceful shutdown")


def is_shutdown_requested() -> bool:
    """Check if shutdown has been requested.
    
    Returns:
        True if shutdown was requested via signal, False otherwise
    """
    return _shutdown_requested

