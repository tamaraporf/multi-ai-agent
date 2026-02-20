import subprocess
import threading
import time
from dotenv import load_dotenv
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger=get_logger(__name__)

load_dotenv()

def run_backend():
    try:
        logger.info("starting backend service..")
        subprocess.run(
            ["uvicorn", "app.backend.api:app", "--host", "127.0.0.1", "--port", "9999"],
            check=True
        )
    except subprocess.CalledProcessError as e:
        logger.exception(
            "Backend service exited with non-zero status",
            extra={"returncode": e.returncode, "cmd": e.cmd}
        )
        raise CustomException("Failed to start backend", e)
    except Exception as e:
        logger.exception("Unexpected error while starting backend")
        raise CustomException("Failed to start backend", e)
    
def run_frontend():
    try:
        logger.info("Starting Frontend service")
        subprocess.run(["streamlit", "run", "app/frontend/ui.py"], check=True)
    except subprocess.CalledProcessError as e:
        logger.exception(
            "Frontend service exited with non-zero status",
            extra={"returncode": e.returncode, "cmd": e.cmd}
        )
        raise CustomException("Failed to start frontend", e)
    except Exception as e:
        logger.exception("Unexpected error while starting frontend")
        raise CustomException("Failed to start frontend", e)
    
if __name__=="__main__":
    try:
        threading.Thread(target=run_backend).start()
        time.sleep(2)
        run_frontend()
    
    except CustomException as e:
        logger.exception(f"CustomException occured : {str(e)}")


    
