import streamlit as st
import pandas as pd
from utils import load_data, save_data

data = load_data()

df_signiture_items = pd.DataFrame(data["시그풍"]["품목"])
df_signiture_options = pd.DataFrame(data["시그풍"]["옵션"])
df_signiture_deadline = pd.DataFrame(data["시그풍"]["작업기한"])

df_poster_items = pd.DataFrame(data["포스터"]["품목"])
df_poster_options = pd.DataFrame(data["포스터"]["옵션"])
df_poster_deadline = pd.DataFrame(data["포스터"]["작업기한"])

df_general_items = pd.DataFrame(data["일반"]["품목"])
df_general_options = pd.DataFrame(data["일반"]["옵션"])
df_general_deadline = pd.DataFrame(data["일반"]["작업기한"])


# 시그풍 섹션
st.markdown("##### 시그풍")
with st.expander("### 시그풍 품목"):
    edited_df_signiture_items = st.data_editor(
        df_signiture_items,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "이름": st.column_config.TextColumn("이름", required=True),
            "가격": st.column_config.NumberColumn("가격", required=True, format="%d"),
        },
    )

with st.expander("### 시그풍 옵션"):
    edited_df_signiture_options = st.data_editor(
        df_signiture_options,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "이름": st.column_config.TextColumn("이름", required=True),
            "가격": st.column_config.NumberColumn("가격", required=True, format="%d"),
        },
    )

with st.expander("### 시그풍 작업기한"):
    edited_df_signiture_deadline = st.data_editor(
        df_signiture_deadline,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "이름": st.column_config.TextColumn("이름", required=True),
            "추가금": st.column_config.NumberColumn(
                "추가금", required=True, format="%d"
            ),
            "배수": st.column_config.NumberColumn("배수", required=True, format="%d"),
        },
    )

# 포스터 섹션
st.markdown("##### 포스터")
with st.expander("### 포스터 품목"):
    edited_df_poster_items = st.data_editor(
        df_poster_items,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "이름": st.column_config.TextColumn("이름", required=True),
            "가격": st.column_config.NumberColumn("가격", required=True, format="%d"),
        },
    )

with st.expander("### 포스터 옵션"):
    edited_df_poster_options = st.data_editor(
        df_poster_options,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "이름": st.column_config.TextColumn("이름", required=True),
            "가격": st.column_config.NumberColumn("가격", required=True, format="%d"),
        },
    )

with st.expander("### 포스터 작업기한"):
    edited_df_poster_deadline = st.data_editor(
        df_poster_deadline,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "이름": st.column_config.TextColumn("이름", required=True),
            "추가금": st.column_config.NumberColumn(
                "추가금", required=True, format="%d"
            ),
            "배수": st.column_config.NumberColumn("배수", required=True, format="%d"),
        },
    )

# 일반 섹션
st.markdown("##### 일반")
with st.expander("### 일반 품목"):
    edited_df_general_items = st.data_editor(
        df_general_items,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "이름": st.column_config.TextColumn("이름", required=True),
            "가격": st.column_config.NumberColumn("가격", required=True, format="%d"),
        },
    )

with st.expander("### 일반 옵션"):
    edited_df_general_options = st.data_editor(
        df_general_options,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "이름": st.column_config.TextColumn("이름", required=True),
            "가격": st.column_config.NumberColumn("가격", required=True, format="%d"),
        },
    )

with st.expander("### 일반 작업기한"):
    edited_df_general_deadline = st.data_editor(
        df_general_deadline,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "이름": st.column_config.TextColumn("이름", required=True),
            "추가금": st.column_config.NumberColumn(
                "추가금", required=True, format="%d"
            ),
            "배수": st.column_config.NumberColumn("배수", required=True, format="%d"),
        },
    )

# 저장 버튼
if st.button("변경사항 저장", use_container_width=True, type="primary"):
    # 데이터프레임을 딕셔너리로 변환
    updated_data = {
        "시그풍": {
            "품목": edited_df_signiture_items.to_dict("records"),
            "옵션": edited_df_signiture_options.to_dict("records"),
            "작업기한": edited_df_signiture_deadline.to_dict("records"),
        },
        "포스터": {
            "품목": edited_df_poster_items.to_dict("records"),
            "옵션": edited_df_poster_options.to_dict("records"),
            "작업기한": edited_df_poster_deadline.to_dict("records"),
        },
        "일반": {
            "품목": edited_df_general_items.to_dict("records"),
            "옵션": edited_df_general_options.to_dict("records"),
            "작업기한": edited_df_general_deadline.to_dict("records"),
        },
    }

    # 데이터 저장
    save_data(updated_data)
    st.success("변경사항이 저장되었습니다!")
