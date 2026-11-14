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

st.markdown("""<style>
[data-testid="stAppViewContainer"]{background:#faf7f2}
.block-container{max-width:460px;padding:1.2rem 1rem 1.5rem}
[data-testid="stHeader"]{background:transparent}
h1{font-size:30px!important;letter-spacing:-1.8px;margin:0!important}
.stButton>button{border-radius:18px;min-height:54px;font-size:18px;font-weight:700}
.stButton>button[kind="primary"]{background:#f26445;border:0;color:white}
.stTextInput input{border-radius:14px}
.card{background:white;border:1px solid #eee6dc;border-radius:26px;padding:24px 18px;text-align:center;margin:8px 0 14px;box-shadow:0 8px 26px #52361b08;color:#302b26}
.eyebrow{font-size:12px;letter-spacing:2px;color:#9b7960;font-weight:700}
.food{font-size:58px;line-height:1.3;margin:12px 0 4px}
.menu{font-size:30px;font-weight:800;letter-spacing:-1px}
.chips{display:flex;justify-content:center;gap:7px;margin:15px 0 0;flex-wrap:wrap}
.chip{background:#f6f1e9;border-radius:999px;padding:6px 12px;font-size:13px}
.sub{font-size:14px;color:#81786d;margin-top:8px}
[data-testid="stLinkButton"] a{border-radius:14px;min-height:46px;background:white}
@media(max-width:480px){.block-container{padding-top:.8rem}.card{padding:16px}.food{font-size:48px;margin-top:6px}}
</style>""",unsafe_allow_html=True)
st.title('우리 뭐먹지? 🍽️')
st.caption('아무거나 말고, 오늘은 이걸로!')
region=st.text_input('식당을 찾을 동네', placeholder='📍 동네 입력 · 예: 연남동',label_visibility='collapsed',max_chars=80)
if st.button('🎲 다시 골라줘!' if st.session_state.get('result') else '🎲 오늘 뭐 먹을까?',type='primary',use_container_width=True):
    st.session_state.result=draw(['실내','실외'],['외식','해먹기'],['양식','중식','일식'],[])
r=st.session_state.get('result')
if r:
    emoji={'양식':'🍝','중식':'🥡','일식':'🍱'}[r['cuisine']]
    st.markdown(f"""<div class="card"><div class="eyebrow">TODAY’S PICK</div><div class="food">{emoji}</div><div class="menu">{r['menu']}</div><div class="chips"><span class="chip">{'🏠' if r['space']=='실내' else '🌿'} {r['space']}</span><span class="chip">{'🍴' if r['way']=='외식' else '🍳'} {r['way']}</span><span class="chip">{r['cuisine']}</span></div><div class="sub">{'도시락으로 챙겨 피크닉 어때요?' if r['space']=='실외' and r['way']=='해먹기' else '가족과 함께 맛있게 먹어요.'}</div></div>""",unsafe_allow_html=True)
    if r['way']=='외식':
        query=' '.join(x for x in [region.strip(),r['menu'],'야외 테라스' if r['space']=='실외' else ''] if x)
        if not region.strip():
            st.caption('동네를 입력하면 그 지역으로 검색해요.')
        left,right=st.columns(2)
        left.link_button('네이버지도 ↗','https://map.naver.com/p/search/'+quote(query,safe=''),use_container_width=True)
        right.link_button('카카오맵 ↗','https://map.kakao.com/?q='+quote(query,safe=''),use_container_width=True)
        st.caption('지도 검색으로 연결돼요. 영업시간과 실내·야외 좌석은 식당에 확인해 주세요.')
    else:
        st.caption('🧺 재료 예시 · '+' · '.join(MENUS[r['cuisine']][r['menu']]))
        query=r['menu']+(' 도시락 레시피' if r['space']=='실외' else ' 레시피')
        st.link_button('이 메뉴 만드는 법 ↗','https://search.naver.com/search.naver?query='+quote(query,safe=''),use_container_width=True)
else:
    st.markdown('<div class="card"><div class="eyebrow">FAMILY FOOD PICKER</div><div class="food">🎲</div><div class="menu">고민은 짧게,<br>식사는 즐겁게.</div><div class="sub">버튼 한 번으로 식사 공간·방법·메뉴를 골라요.</div><div class="chips"><span class="chip">실내 / 실외</span><span class="chip">외식 / 해먹기</span><span class="chip">양식 / 중식 / 일식</span></div></div>',unsafe_allow_html=True)
st.caption('🥜 알레르기와 식이 제한은 직접 확인해 주세요. 무작위 결과는 안전한 식사를 보장하지 않아요.')
st.caption('위치는 자동 수집하지 않아요. 지도 버튼을 누르면 입력한 동네가 지도 서비스에 전달돼요.')
