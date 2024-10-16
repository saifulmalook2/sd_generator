import streamlit as st
import requests
import json
import pandas as pd

# Set the URL of the FastAPI backend
API_URL = "http://localhost:8000/generate"  # Adjust this as needed

def main():
    st.title("SD Generator")
    
    # Input fields for company details
    company_name = st.text_input("Enter Company Name:")
    company_website = st.text_input("Enter Company Website:")
    company_type = st.selectbox(
                                "Select Report Type",
                                    ["SOC 2 Type I: Security", "SOC 2 Type II: Security"]
                                )
    # company_vendors = st.text_input("Enter Vendors List:")
    company_product_name = st.text_input("Enter System Name")

    company_hire_days = st.text_input("Enter the number of business days to complete policy review and security training after hire:")
    company_revoke_days = st.text_input("Enter the number of business days for deprovisioning system access after employee termination:")
    company_provider = st.text_input("Enter Service Provider")
    incidents = st.checkbox("Please check this Box if any Security Incidents have occured in the past 12 months")
    changes = st.checkbox("Please check this Box if any Significant Changes to services have occured in the past 12 months")

    file1 = st.file_uploader("Upload Policy Packet", type=[ "pdf", "docx"])
    file2 = st.file_uploader("Upload Vendor Data", type=["xlsx"])
    file3 = st.file_uploader("Upload Data Management Policy", type=[ "pdf", "docx"])

    # Initialize the session state for document upload and generation
    if 'docs_uploaded' not in st.session_state:
        st.session_state['docs_uploaded'] = False

    if st.button("Upload Documents"):
        if file1 and file2 and file3:
            files = {
                "policy_packet": (file1.name, file1, file1.type),
                "vendors_list": (file2.name, file2, file2.type),
                "data_policy": (file3.name, file3, file3.type)
            }

            with st.spinner("Uploading Documents..."):
                response = requests.post("http://localhost:8000/upload_files", files=files, data={"company_name": company_name})
                if response.status_code == 200:
                    st.success("Documents uploaded successfully!")
                    # Set docs_uploaded to True once the documents are uploaded successfully
                    st.session_state['docs_uploaded'] = True
                else:
                    st.error("Error uploading documents.")

    # Only show the "Generate!" button after documents have been uploaded successfully
    if st.session_state['docs_uploaded']:
        if st.button("Generate!"):
            if company_name and company_website and company_type:
                # Prepare the data to send to the FastAPI backend
                company_data = {
                    "name": company_name,
                    "website": company_website,
                    "report": company_type,
                    "system_name": company_product_name,
                    "hire_days": company_hire_days,
                    "revoke_days": company_revoke_days,
                    "provider": company_provider,
                    "incidents": incidents,
                    "changes": changes
                }

                # Send a POST request to the FastAPI backend
                with st.spinner("Generating a description for given system. This might take a couple of minutes..."):
                    response = requests.post(API_URL, json=company_data, stream=True)

                    # Check if the request was successful
                    if response.status_code == 200:
                        # Process the streamed response
                        for chunk in response.iter_lines():
                            if chunk:
                                # Decode the chunk and load it as JSON
                                result = json.loads(chunk.decode('utf-8'))

                                # Display heading, paragraphs, and points
                                if "heading" in result and result["heading"]:
                                    st.header(result["heading"])

                                for paragraph in result.get("paragraphs", []):
                                    st.write(paragraph)

                                if "points" in result:
                                    for point in result["points"]:
                                        st.markdown(f"- {point}")

                                if result.get("table") is not None:
                                    df = pd.DataFrame(result["table"])
                                    st.table(df)
                    else:
                        st.error("Error: Unable to generate information.")
            else:
                st.warning("Please fill in all fields.")

if __name__ == "__main__":
    main()
