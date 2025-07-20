import streamlit as st
from response import get_response  # Assuming get_response is a function in response.py that handles API calls

def main():
    st.title("Chat with Munna")
    st.write("Enter your prompt below:")

    user_input = st.text_input("Prompt:")

    if st.button("Submit"):
        if user_input:
            response = get_response(user_input)
            st.write("Response from GPT-4o-mini:")
            st.write(response)
        else:
            st.warning("Please enter a prompt.")

if __name__ == "__main__":
    main()