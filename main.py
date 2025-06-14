import streamlit as st
from utils import load_data, save_data

data = load_data()
tab_names = list(data.keys())

st.set_page_config(page_title="견적서", page_icon=":tada:")

st.title("견적서")

tabs = st.tabs(tab_names)

for i, tab in enumerate(tabs):
    with tab:
        st.markdown(f"#### {tab_names[i]} 견적서")

        # 품목 선택
        items = data[tab_names[i]]["품목"]
        item_names = [item["이름"] for item in items]
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("###### 선택 품목")
                selected_item = st.selectbox(
                    "품목 선택",
                    item_names,
                    index=0,
                    key=f"item_{tab_names[i]}",
                    label_visibility="collapsed",
                )
            with col2:
                selected_item_price = next(
                    item["가격"] for item in items if item["이름"] == selected_item
                )
                st.markdown("###### 선택 품목 가격")
                st.button(
                    f"{selected_item_price:,}원",
                    key=f"add_{tab_names[i]}",
                    disabled=True,
                )

        # 옵션 선택
        options = data[tab_names[i]]["옵션"]
        option_names = [option["이름"] for option in options]
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("###### 선택 옵션")
                selected_options = st.multiselect(
                    "선택 옵션",
                    option_names,
                    key=f"option_{tab_names[i]}",
                    label_visibility="collapsed",
                )
            with col2:
                st.markdown("###### 선택 옵션 가격")
                selected_option_prices = []
                for o in selected_options:
                    option_price = next(
                        opt["가격"] for opt in options if opt["이름"] == o
                    )
                    st.text(f"{option_price:,}원")
                    selected_option_prices.append(option_price)
            col1, col2 = st.columns(2)
            with col1:
                pass
            with col2:
                option_sum = sum(selected_option_prices)
                st.button(
                    f"{option_sum:,}원",
                    key=f"add_option_{tab_names[i]}",
                    disabled=True,
                )

        # 수량 선택
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("###### 수량")
            with col2:
                selected_quantity = st.number_input(
                    "수량",
                    value=1,
                    min_value=1,
                    max_value=100,
                    step=1,
                    label_visibility="collapsed",
                    key=f"option_count_{tab_names[i]}",
                )

        # 작업기한 선택
        work_periods = data[tab_names[i]]["작업기한"]
        work_period_names = [work_period["이름"] for work_period in work_periods]
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("###### 선택 작업기한")
                selected_work_period = st.selectbox(
                    "작업기한 선택",
                    work_period_names,
                    key=f"work_period_{tab_names[i]}",
                    label_visibility="collapsed",
                )
            with col2:
                st.markdown("###### 선택 작업기한 추가금 / 배수")
                selected_work_period_price = next(
                    work_period["추가금"]
                    for work_period in work_periods
                    if work_period["이름"] == selected_work_period
                )
                selected_work_period_multiplier = next(
                    work_period["배수"]
                    for work_period in work_periods
                    if work_period["이름"] == selected_work_period
                )
                st.button(
                    f"추가금 {selected_work_period_price:,}원 / 총액의 {selected_work_period_multiplier}% 추가",
                    key=f"add_work_period_{tab_names[i]}",
                    disabled=True,
                )
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("###### 총 금액")
                pass
            with col2:
                total_price = (
                    (
                        selected_item_price
                        + sum(selected_option_prices)
                        + selected_work_period_price
                    )
                    * selected_quantity
                    * (1 + selected_work_period_multiplier * 0.01)
                )
                total_price = int(total_price)
                st.button(f"{total_price:,}원", key=f"add_total_{tab_names[i]}")
        st.markdown(
            "> 총 금액 = ( 품목 + 옵션 + 작업기한추가금 ) x 수량 x (1 + 작업기한배수)"
        )

        st.divider()
