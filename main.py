import streamlit as st


pages = {
    "뇽작가": [
        st.Page("./pages/estimate.py", title="견적 계산", icon="💰"),
        st.Page("./pages/edit.py", title="견적 수정", icon="🔍"),
    ]
}


pg = st.navigation(pages)
pg.run()
