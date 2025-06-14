import streamlit as st
from utils import load_data, save_data

# 레이아웃 설정
TITLE_WIDTH = "80px"
CONTENT_WIDTH = "150px"

data = load_data()
tab_names = list(data.keys())

st.set_page_config(page_title="뇽작가 견적서", page_icon=":tada:")

st.title("뇽작가 견적서")

selected_item = None
selected_item_price = 0
selected_options = []
selected_option_prices = []
selected_work_period = None
selected_work_period_price = 0
selected_work_period_multiplier = 0

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
            st.markdown("")
            st.markdown("##### 뇽작가 견적 금액")

            st.markdown(
                f'<div style="display: flex; justify-content: space-between;"><span style="width: {TITLE_WIDTH}"><strong>품목</strong></span><span style="width: {CONTENT_WIDTH}">{selected_item}</span><span>{selected_item_price:,} 원</span></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div style="display: flex; justify-content: space-between;"><span style="width: {TITLE_WIDTH}"><strong>옵션</strong></span><span style="width: {CONTENT_WIDTH}"></span><span></span></div>',
                unsafe_allow_html=True,
            )
            for option in selected_options:
                st.markdown(
                    f'<div style="display: flex; justify-content: space-between;"><span style="width: {TITLE_WIDTH}"></span><span style="width: {CONTENT_WIDTH}">{option}</span><span>{option_price:,} 원</span></div>',
                    unsafe_allow_html=True,
                )
            st.markdown("")
            item_sum = selected_item_price + sum(selected_option_prices)
            st.markdown(
                f'<div style="display: flex; justify-content: space-between;"><span style="width: {TITLE_WIDTH}"><strong>품목 계</strong></span><span style="width: {CONTENT_WIDTH}"></span><span>{item_sum:,} 원</span></div>',
                unsafe_allow_html=True,
            )
            st.divider()

            st.markdown(
                f'<div style="display: flex; justify-content: space-between;"><span style="width: {TITLE_WIDTH}"><strong>수량</strong></span><span style="width: {CONTENT_WIDTH}"></span><span>{selected_quantity}개</span></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div style="display: flex; justify-content: space-between;"><span style="width: {TITLE_WIDTH}"><strong>작업기한</strong></span><span style="width: {CONTENT_WIDTH}">{selected_work_period}</span><span>{selected_work_period_price:,} 원 / {selected_work_period_multiplier}%</span></div>',
                unsafe_allow_html=True,
            )
            st.divider()

            multiplier_print = 1 + selected_work_period_multiplier * 0.01
            total_price = int(
                (item_sum + selected_work_period_price)
                * selected_quantity
                * multiplier_print
            )
            total_print_price = f"{item_sum:,} 원 x {selected_quantity} 개 x {int(multiplier_print*100)}%"
            st.markdown(
                f'<div style="display: flex; justify-content: space-between;"><span style="width: {TITLE_WIDTH}"><strong>총액</strong></span><span style="width: {CONTENT_WIDTH}">{total_print_price}</span><span>{total_price:,} 원</span></div>',
                unsafe_allow_html=True,
            )
            st.markdown("")

        st.divider()
