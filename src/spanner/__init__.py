import logging
import sys

# Try to import Google Cloud Logging library.
try:
    from google.cloud import logging as google_logging
    from google.cloud.logging.handlers import CloudLoggingHandler

    GCP_LOGGING_AVAILABLE = True
except ImportError:
    GCP_LOGGING_AVAILABLE = False

# 1. Get the logger for the local package.
logger = logging.getLogger(__name__)

# 2. Set the default logging level.
logger.setLevel(logging.INFO)

# 3. Add handlers only if they haven't been added before.
if not logger.handlers:
    # 4. Create and add a console handler.
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 5. Create and add Google Cloud Logging handler if available.
    if GCP_LOGGING_AVAILABLE:
        client = google_logging.Client()
        gcp_handler = CloudLoggingHandler(client, name="spanner-service")
        logger.addHandler(gcp_handler)
        logger.info("Google Cloud Logging handler initialized.")
    else:
        logger.info("Google Cloud Logging library not found, logging to console only.")
