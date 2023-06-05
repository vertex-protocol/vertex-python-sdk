import os
from dotenv import load_dotenv

load_dotenv()

SIGNER_PRIVATE_KEY = os.getenv("SIGNER_PRIVATE_KEY")
LINKED_SIGNER_PRIVATE_KEY = os.getenv("LINKED_SIGNER_PRIVATE_KEY")
