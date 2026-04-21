import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

def run_ui() -> None:
    """
    Renders a simple Streamlit UI that allows users to upload an
    image of a banana, preview it, and request a ripeness prediction from
    the backend FastAPI service. The uploaded image is sent as multipart
    form data to the `/banana_ripeness_classifier` endpoint, and the
    resulting classification is displayed to the user.
    """
    st.title("Banana Ripeness Classifier")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.image(uploaded_file, caption="Uploaded Image", width=400)

        if st.button("Predict"):

            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}

            try:
                response = requests.post(
                    f"{BACKEND_URL}/banana_ripeness_classifier",
                    files=files,
                    timeout=30
                )

                # 🚨 This will raise if backend returns 4xx/5xx
                response.raise_for_status()

                result = response.json()

                # 🚨 Catch missing key issues
                if "result" not in result:
                    st.error(f"Unexpected response format: {result}")
                else:
                    prediction = result["result"]
                    st.success(f"{prediction}")

            except requests.exceptions.HTTPError as http_err:
                st.error(f"HTTP error from backend: {http_err}")
                st.text(response.text)  # 👈 shows backend error body

            except requests.exceptions.ConnectionError as conn_err:
                st.error(f"Connection error: {conn_err}")

            except requests.exceptions.Timeout:
                st.error("Request timed out")

            except requests.exceptions.RequestException as req_err:
                st.error(f"Request failed: {req_err}")

            except Exception as e:
                st.error(f"Unexpected error: {e}")

            # try:
            #     response = requests.post(
            #         f"{BACKEND_URL}/banana_ripeness_classifier", files=files
            #     )

            #     response.raise_for_status()

            #     result = response.json()
            #     prediction = result["result"]

            #     st.success(f"{prediction}")

            # except Exception as e:
            #     st.error(e)


if __name__ == "__main__":
    run_ui()
