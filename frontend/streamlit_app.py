
"""Streamlit frontend for the ICT RAG Study Assistant."""

import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="ICT Study Assistant",
    page_icon="🎓",
    layout="centered",
)


st.title("🎓 ICT Study Assistant")
st.write(
    "Ask questions about the Secondary 2 ICT lesson "
    "and get answers grounded in the lesson content."
)


question = st.text_area(
    "Your question",
    placeholder="Example: What is the possession factor?",
    height=120,
)


if st.button(
    "Ask",
    type="primary",
    use_container_width=True,
):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Searching the lesson..."):
                response = requests.post(
                    f"{API_URL}/query",
                    json={
                        "question": question.strip(),
                    },
                    timeout=120,
                )

            if response.status_code == 200:
                data = response.json()

                st.subheader("Answer")
                st.write(data["answer"])

                sources = data.get(
                    "sources",
                    [],
                )

                if sources:
                    st.subheader("Sources")

                    for source in sources:
                        st.caption(source)

            elif response.status_code == 422:
                st.error(
                    "The question is invalid. "
                    "Please enter a non-empty question."
                )

            else:
                st.error(
                    f"The backend returned an error "
                    f"(HTTP {response.status_code})."
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to the FastAPI backend. "
                "Make sure the backend is running on "
                f"{API_URL}."
            )

        except requests.exceptions.Timeout:
            st.error(
                "The request took too long to complete. "
                "Please try again."
            )

        except requests.exceptions.RequestException as exc:
            st.error(
                f"An unexpected network error occurred: {exc}"
            )
