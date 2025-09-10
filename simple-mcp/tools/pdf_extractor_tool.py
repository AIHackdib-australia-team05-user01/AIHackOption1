import os
import time
import requests
from config.settings import AZURE_ENDPOINT, AZURE_KEY

def extract_pdf(params: dict) -> dict:
    file_path = params.get("file_path")
    if not file_path:
        return {"error": "Missing 'file_path' in parameters."}

    if not os.path.isfile(file_path):
        return {"error": f"File not found: {file_path}"}

    if not file_path.lower().endswith(".pdf"):
        return {"error": "Unsupported file type. Only PDF files are accepted."}

    url = f"{AZURE_ENDPOINT}/formrecognizer/documentModels/prebuilt-layout:analyze?api-version=2023-07-31"
    headers = {
        "Content-Type": "application/pdf",
        "Ocp-Apim-Subscription-Key": AZURE_KEY
    }

    try:
        with open(file_path, "rb") as f:
            response = requests.post(url, headers=headers, data=f)

        if response.status_code != 202:
            return {
                "error": "Azure API failed",
                "status_code": response.status_code,
                "response": response.text
            }

        operation_location = response.headers.get("operation-location")
        if not operation_location:
            return {"error": "Missing operation-location in Azure response headers."}

        # Poll for result
        poll_headers = {"Ocp-Apim-Subscription-Key": AZURE_KEY}
        for _ in range(10):  # Try for ~10 seconds
            poll_response = requests.get(operation_location, headers=poll_headers)
            result = poll_response.json()

            status = result.get("status")
            if status == "succeeded":
                return {
                    "summary": result.get("analyzeResult", {}).get("content", "No content found"),
                    "pages": result.get("analyzeResult", {}).get("pages", [])
                }
            elif status == "failed":
                return {"error": "Azure analysis failed", "details": result}

            time.sleep(1)  # Wait before retrying

        return {"error": "Azure analysis timed out"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
