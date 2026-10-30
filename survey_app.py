import streamlit as st
import pandas as pd
from datetime import datetime
import os

EXCEL_FILE = "Tracker.xlsx"
RESULT_FILE = "Survey_Results.xlsx"

st.set_page_config(
    page_title="Resource Survey",
    layout="wide"
)

st.title("Manager Resource Survey")

# Load Master Data
master_df = pd.read_excel(
    EXCEL_FILE,
    sheet_name="Manager_Resources"
)

# Manager Login
manager_email = st.text_input(
    "Enter Your Manager Email"
)

if manager_email:

    team_df = master_df[
        master_df["ManagerEmail"].str.lower()
        == manager_email.lower()
    ]

    if team_df.empty:
        st.error("No resources found for this manager")
        st.stop()

    manager_name = team_df.iloc[0]["ManagerName"]

    st.success(f"Welcome {manager_name}")

    ratings = []

    for _, row in team_df.iterrows():

        resource = row["ResourceName"]

        st.markdown("---")
        st.subheader(resource)

        technical = st.selectbox(
            f"{resource} - Technical Skills",
            [1,2,3,4,5],
            key=f"tech_{resource}"
        )

        communication = st.selectbox(
            f"{resource} - Communication",
            [1,2,3,4,5],
            key=f"comm_{resource}"
        )

        ownership = st.selectbox(
            f"{resource} - Ownership",
            [1,2,3,4,5],
            key=f"own_{resource}"
        )

        teamwork = st.selectbox(
            f"{resource} - Teamwork",
            [1,2,3,4,5],
            key=f"team_{resource}"
        )

        overall = st.selectbox(
            f"{resource} - Overall Rating",
            [1,2,3,4,5],
            key=f"overall_{resource}"
        )

        comments = st.text_area(
            f"{resource} - Comments",
            key=f"comments_{resource}"
        )

        ratings.append({
            "ManagerName": manager_name,
            "ManagerEmail": manager_email,
            "ResourceName": resource,
            "TechnicalSkills": technical,
            "Communication": communication,
            "Ownership": ownership,
            "Teamwork": teamwork,
            "OverallRating": overall,
            "Comments": comments,
            "SurveyDate": datetime.now()
        })

    if st.button("Submit Survey"):

        result_df = pd.DataFrame(ratings)

        if os.path.exists(RESULT_FILE):

            existing = pd.read_excel(
                RESULT_FILE
            )

            result_df = pd.concat(
                [existing, result_df],
                ignore_index=True
            )

        result_df.to_excel(
            RESULT_FILE,
            index=False
        )

        st.success(
            "Survey Submitted Successfully"
        )
