"""우리 뭐먹지? | GitHub + Streamlit Community Cloud
app.py와 requirements.txt를 같은 폴더에 올리고 app.py를 배포하세요.
별도 키나 Secrets 불필요. 식당은 지도 검색으로 연결하며 실제 목록을 수집하지 않습니다.
실내/실외는 식사 공간 선호입니다. 실외+해먹기는 도시락/피크닉으로 해석합니다.
"""
import random
from urllib.parse import quote
import streamlit as st

st.set_page_config(page_title='우리 뭐먹지?', page_icon='🍽️', layout='centered')
MENUS = {
 '양식': {'파스타':['면','소스','채소'], '샌드위치':['빵','채소','원하는 속재료'], '리소토':['쌀','육수','채소'], '피자':['도우','소스','치즈']},
 '중식': {'볶음밥':['밥','채소','간장'], '마파두부':['두부','마파 소스','밥'], '중국식 볶음면':['면','채소','볶음 소스'], '토마토 달걀볶음':['토마토','달걀','식용유']},
 '일식': {'카레라이스':['밥','카레','채소'], '우동':['우동면','육수','고명'], '주먹밥':['밥','김','원하는 속재료'], '돈가스':['돈가스','밥','소스']},
 '한식': {'비빔밥':['밥','나물','양념'], '김치볶음밥':['밥','김치','식용유'], '불고기':['고기','불고기 양념','채소'], '된장찌개':['된장','두부','채소']},
}

def pick(options, rng=None):
    if not options:
        raise ValueError('선택 가능한 항목이 없습니다.')
    return (rng or random).choice(list(options))

def draw(spaces, ways, cuisines, excluded, rng=None):
    available = {c: [m for m in MENUS[c] if m not in excluded] for c in cuisines}
    available = {c: ms for c, ms in available.items() if ms}
    if not available:
        raise ValueError('제외하지 않은 메뉴가 있는 음식 종류를 선택해 주세요.')
    space, way, cuisine = pick(spaces,rng), pick(ways,rng), pick(available,rng)
    return dict(space=space, way=way, cuisine=cuisine, menu=pick(available[cuisine],rng))

st.markdown('''<style>
.block-container{max-width:620px;padding-top:1.2rem;padding-bottom:1rem}
h1{font-size:2rem!important;letter-spacing:-1.5px}
.stButton>button{border-radius:14px;min-height:44px}
.result{background:linear-gradient(120deg,#fff1dc,#ffe6df);color:#33251d;padding:22px;border-radius:22px;text-align:center;margin:12px 0}
.result .big{font-size:30px;font-weight:800;margin:10px 0}
.result .small{font-size:15px}
</style>''', unsafe_allow_html=True)
st.title('🍽️ 우리 뭐먹지?')
st.caption('“아무거나” 대신, 우리 가족의 오늘 한 끼를 뽑아 봐요!')

with st.expander('⚙️ 뽑기 조건 · 싫어하는 메뉴 제외', expanded=False):
    spaces=st.multiselect('① 식사 공간', ['실내','실외'], default=['실내','실외'])
    ways=st.multiselect('② 식사 방법', ['외식','해먹기'], default=['외식','해먹기'])
    cuisines=st.multiselect('③ 음식 종류', list(MENUS), default=['양식','중식','일식'])
    excluded=st.multiselect('제외할 메뉴', [m for c in MENUS.values() for m in c])
    st.caption('각 단계의 선택지에서 같은 확률로 뽑아요. 한식은 선택하면 추가돼요. 실외+해먹기는 도시락·피크닉이에요.')
region=st.text_input('📍 식당을 찾을 동네', placeholder='예: 서울 마포구 연남동', max_chars=80)
if 'history' not in st.session_state:
    st.session_state.history=[]
if st.button('🎲 오늘 한 끼 뽑기', type='primary', use_container_width=True):
    try:
        result=draw(spaces,ways,cuisines,excluded)
        st.session_state.result=result
        st.session_state.history.insert(0,result.copy())
        st.session_state.history=st.session_state.history[:8]
    except ValueError as e:
        st.error(str(e))

r=st.session_state.get('result')
if r:
    # All result strings are selected from fixed server-side lists.
    st.markdown(f'''<div class="result"><div class="small">① {r['space']}　→　② {r['way']}　→　③ {r['cuisine']}</div><div class="big">{r['menu']}</div><div>오늘은 이 메뉴 어때요? 😋</div></div>''', unsafe_allow_html=True)
    if r['space']=='실외':
        st.caption('🌿 야외 좌석·포장 후 피크닉을 고려해 보세요. 날씨와 이용 가능 여부는 직접 확인해 주세요.')
    if r['way']=='외식':
        if region.strip():
            query=f"{region.strip()} {r['menu']}"+(' 야외 테라스' if r['space']=='실외' else '')
            c1,c2=st.columns(2)
            c1.link_button('📍 네이버지도 식당 찾기','https://map.naver.com/p/search/'+quote(query,safe=''),use_container_width=True)
            c2.link_button('📍 카카오맵 식당 찾기','https://map.kakao.com/?q='+quote(query,safe=''),use_container_width=True)
            st.caption('입력한 동네와 뽑힌 메뉴로 지도 검색을 열어요. 실제 식당 추천·예약 기능은 아니며, 영업시간·실내외 좌석·알레르기 대응은 식당에 확인하세요.')
        else:
            st.info('위에 동네를 입력하면 해당 메뉴의 식당 지도 검색 버튼이 나타나요.')
    else:
        st.write('🧺 **준비 재료 예시** · '+' · '.join(MENUS[r['cuisine']][r['menu']]))
        query=quote(r['menu']+' 도시락 레시피' if r['space']=='실외' else r['menu']+' 레시피',safe='')
        st.link_button('📖 조리법 검색하기','https://search.naver.com/search.naver?query='+query,use_container_width=True)
        st.caption('재료는 예시이며 완전한 조리법이 아니에요. 실제 레시피의 재료와 조리 방법을 확인하세요.')
    st.warning('알레르기·식이 제한이 있다면 메뉴를 제외하고, 소스와 세부 재료도 반드시 확인해 주세요.',icon='🥜')
else:
    st.info('조건을 정하고 뽑기 버튼을 눌러 보세요. 마음에 안 들면 다시 뽑을 수 있어요.')
with st.expander('🕘 이번 접속의 뽑기 기록'):
    for i,h in enumerate(st.session_state.history,1):
        st.write(f"{i}. {h['space']} · {h['way']} · {h['cuisine']} → **{h['menu']}**")
    if not st.session_state.history:
        st.caption('아직 기록이 없어요.')
st.caption('개인정보·위치를 자동 수집하지 않아요. 동네는 지도 검색 시 해당 지도 서비스로 전달돼요. 기록은 접속 세션 내 임시 기록이에요.')
