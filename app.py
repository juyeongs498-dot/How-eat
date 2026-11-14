"""우리 뭐먹지? | GitHub + Streamlit Community Cloud
app.py와 requirements.txt를 같은 폴더에 올리고 app.py를 배포하세요.
별도 키나 Secrets 불필요. 식당은 지도 검색으로 연결하며 실제 목록을 수집하지 않습니다.
실내/실외는 식사 공간 선호입니다. 실외+해먹기는 도시락/피크닉으로 해석합니다.
"""
import random
import time
from urllib.parse import quote
import streamlit as st

st.set_page_config(page_title='우리 뭐먹지?', page_icon='🍽️', layout='centered')
MENUS = {
 '양식': {'파스타':['면','소스','채소'], '샌드위치':['빵','채소','원하는 속재료'], '리소토':['쌀','육수','채소'], '피자':['도우','소스','치즈']},
 '중식': {'볶음밥':['밥','채소','간장'], '마파두부':['두부','마파 소스','밥'], '중국식 볶음면':['면','채소','볶음 소스'], '토마토 달걀볶음':['토마토','달걀','식용유']},
 '일식': {'카레라이스':['밥','카레','채소'], '우동':['우동면','육수','고명'], '주먹밥':['밥','김','원하는 속재료'], '돈가스':['돈가스','밥','소스']},
 '한식': {'비빔밥':['밥','나물','양념'], '김치볶음밥':['밥','김치','식용유'], '불고기':['고기','불고기 양념','채소'], '된장찌개':['된장','두부','채소']},
}

# 메뉴별 준비 재료는 예시이며 실제 조리법/알레르기 정보가 아닙니다.
MENUS['양식'].update({'토마토 파스타': ['파스타면', '토마토 소스', '마늘'], '크림 파스타': ['파스타면', '크림', '버섯'], '알리오 올리오': ['파스타면', '마늘', '올리브유'], '라자냐': ['라자냐면', '토마토 소스', '치즈'], '햄버거': ['버거빵', '패티', '채소'], '스테이크': ['스테이크용 고기', '소금', '곁들임 채소'], '오므라이스': ['밥', '달걀', '케첩'], '감바스': ['새우', '마늘', '올리브유'], '치킨 샐러드': ['닭고기', '샐러드 채소', '드레싱'], '프렌치토스트': ['식빵', '달걀', '우유'], '포크커틀릿': ['돼지고기', '빵가루', '달걀'], '뇨키': ['뇨키', '소스', '치즈'], '퀘사디아': ['토르티야', '치즈', '속재료'], '치킨 랩': ['토르티야', '닭고기', '채소'], '크림 수프': ['크림', '채소', '육수'], '미트볼': ['다진 고기', '토마토 소스', '양파']})
MENUS['중식'].update({'짜장면': ['중화면', '춘장', '양파'], '짬뽕': ['중화면', '해산물', '채소'], '탕수육': ['돼지고기', '전분', '탕수 소스'], '유린기': ['닭고기', '채소', '소스'], '깐풍기': ['닭고기', '고추', '깐풍 소스'], '고추잡채': ['고기', '피망', '꽃빵'], '잡채밥': ['밥', '당면', '채소'], '새우볶음밥': ['밥', '새우', '채소'], '마라탕': ['마라 소스', '육수', '원하는 재료'], '마라샹궈': ['마라 소스', '채소', '고기'], '볶음우동': ['우동면', '채소', '소스'], '군만두': ['만두', '식용유'], '물만두': ['물만두', '간장'], '가지볶음': ['가지', '마늘', '소스'], '팔보채': ['해산물', '채소', '전분'], '누룽지탕': ['누룽지', '육수', '해산물']})
MENUS['일식'].update({'규동': ['밥', '소고기', '양파'], '오야코동': ['밥', '닭고기', '달걀'], '가츠동': ['밥', '돈가스', '달걀'], '텐동': ['밥', '튀김', '덮밥 소스'], '라멘': ['라멘면', '육수', '고명'], '미소라멘': ['라멘면', '미소 육수', '고명'], '소바': ['메밀면', '쯔유', '김'], '야키소바': ['볶음면', '양배추', '야키소바 소스'], '오코노미야키': ['양배추', '부침 반죽', '소스'], '치킨 가라아게': ['닭고기', '전분', '양념'], '일본식 달걀말이': ['달걀', '육수', '설탕'], '유부초밥': ['밥', '유부', '초밥 양념'], '연어구이': ['연어', '소금', '곁들임 채소'], '나베': ['육수', '채소', '고기'], '오차즈케': ['밥', '차 또는 육수', '김'], '니쿠자가': ['감자', '소고기', '양파']})

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

# One screen per stage; random animation advances to its own result screen.
st.markdown("""<style>
[data-testid="stAppViewContainer"]{background:#faf7f2}
[data-testid="stHeader"]{background:transparent}
.block-container{max-width:460px;padding:1.3rem 1rem}
h1{font-size:29px!important;letter-spacing:-1.4px}
.stButton>button{border-radius:18px;min-height:52px;font-size:17px;font-weight:700}
.stButton>button[kind="primary"]{background:#f26445;border:0;color:white}
.card{background:white;border:1px solid #eee3d7;border-radius:28px;padding:32px 16px;text-align:center;margin:16px 0;color:#302b26;min-height:245px}
.icon{font-size:64px;margin:12px}.big{font-size:32px;font-weight:800}.sub{font-size:15px;color:#81786d;margin-top:14px}
.pill{text-align:center;color:#a46d4e;font-size:14px;margin:6px 0}
.roll{animation:pulse .28s infinite alternate}@keyframes pulse{from{transform:scale(.94);opacity:.65}to{transform:scale(1.06);opacity:1}}
</style>""",unsafe_allow_html=True)
STAGES=[('어디에서 먹을까?',['실내','실외']),('어떻게 먹을까?',['집밥','외식']),('어떤 음식을 먹을까?',['양식','중식','일식']),('오늘의 메뉴는?',[])]
ICONS={'실내':'🏠','실외':'🌳','집밥':'🍳','외식':'🍴','양식':'🍝','중식':'🥡','일식':'🍱'}
if 'wizard_step' not in st.session_state:
    st.session_state.wizard_step=0
    st.session_state.wizard_results=[]
    st.session_state.wizard_revealed=False
    st.session_state.wizard_busy=False

def reset():
    st.session_state.wizard_step=0
    st.session_state.wizard_results=[]
    st.session_state.wizard_revealed=False
    st.session_state.wizard_busy=False

step=st.session_state.wizard_step
results=st.session_state.wizard_results
st.title('우리 뭐먹지? 🍽️')
st.caption('한 단계씩 뽑아 보는 우리 가족의 한 끼')
if not st.session_state.get('food_started', False):
    st.markdown('<div class="card"><div class="sub">우리 가족 메뉴 결정 도우미</div><div class="icon">🍽️</div><div class="big">우리 뭐먹지?</div><div class="sub">“아무거나”는 이제 그만!<br>한 단계씩 뽑아 오늘의 한 끼를 정해요.</div><div class="pill" style="margin-top:24px">🏠 식사 공간 → 🍳 식사 방법<br>🍝 음식 종류 → 🎉 오늘의 메뉴</div></div>',unsafe_allow_html=True)
    if st.button('시작하기 →',type='primary',use_container_width=True):
        reset()
        st.session_state.food_started=True
        st.rerun()
    st.caption('양식·중식·일식 60개 메뉴 · 회원가입 없이 바로 시작')
    st.stop()
if step<4:
    title,options=STAGES[step]
    if step==3:
        options=list(MENUS[results[2]])
    st.progress(step/4,text=f'{step+1} / 4 단계')
    st.subheader(title)
    if results:
        st.markdown('<div class="pill">'+' → '.join(results)+'</div>',unsafe_allow_html=True)
    if st.session_state.wizard_busy:
        # Chosen once, independently of decorative animation frames.
        chosen=pick(options)
        slot=st.empty()
        for index in range(14):
            preview=options[index%len(options)]
            slot.markdown(f'<div class="card"><div class="sub">두근두근, 고르는 중…</div><div class="roll"><div class="icon">{ICONS.get(preview,"🍽️")}</div><div class="big">{preview}</div></div></div>',unsafe_allow_html=True)
            time.sleep(.08+index*.009)
        st.session_state.wizard_results.append(chosen)
        st.session_state.wizard_revealed=True
        st.session_state.wizard_busy=False
        st.rerun()
    elif st.session_state.wizard_revealed:
        chosen=results[-1]
        note='실외에서 집밥은 도시락·피크닉으로 즐겨요.' if step==1 and results[:2]==['실외','집밥'] else '이번 단계의 결과예요!'
        st.markdown(f'<div class="card"><div class="sub">선택 완료!</div><div class="icon">{ICONS.get(chosen,"🍽️")}</div><div class="big">{chosen}</div><div class="sub">{note}</div></div>',unsafe_allow_html=True)
        if st.button('최종 결과 보기 →' if step==3 else '다음 단계 →',type='primary',use_container_width=True):
            st.session_state.wizard_step+=1
            st.session_state.wizard_revealed=False
            st.rerun()
    else:
        st.markdown('<div class="card"><div class="icon">🎲</div><div class="big">이번 선택은?</div><div class="sub">'+' · '.join(options)+'</div></div>',unsafe_allow_html=True)
        if st.button('🎲 랜덤으로 뽑기',type='primary',use_container_width=True):
            st.session_state.wizard_busy=True
            st.rerun()
    st.button('처음부터 다시',on_click=reset,use_container_width=True)
else:
    space,way,cuisine,menu=results
    st.progress(1.0,text='오늘의 한 끼 결정 완료!')
    st.markdown(f'<div class="card"><div class="sub">오늘 우리 가족은</div><div class="icon">{ICONS[cuisine]}</div><div class="big">{menu}</div><div class="sub">{space} · {way} · {cuisine}</div></div>',unsafe_allow_html=True)
    if space=='실외':
        st.caption('🌿 '+('도시락으로 챙겨 피크닉 어때요?' if way=='집밥' else '야외 좌석이나 포장 후 식사를 고려해 보세요.'))
    if way=='외식':
        region=st.text_input('📍 식당을 찾을 동네',placeholder='예: 서울 연남동',max_chars=80)
        if region.strip():
            query=region.strip()+' '+menu+(' 야외 테라스' if space=='실외' else '')
            a,b=st.columns(2)
            a.link_button('네이버지도 ↗','https://map.naver.com/p/search/'+quote(query,safe=''),use_container_width=True)
            b.link_button('카카오맵 ↗','https://map.kakao.com/?q='+quote(query,safe=''),use_container_width=True)
            st.caption('실제 식당 목록이 아니라 지도 검색 연결이에요. 영업시간·야외 좌석은 식당에 확인하세요.')
    else:
        st.caption('🧺 재료 예시 · '+' · '.join(MENUS[cuisine][menu]))
        query=menu+(' 도시락 레시피' if space=='실외' else ' 레시피')
        st.link_button('만드는 법 찾아보기 ↗','https://search.naver.com/search.naver?query='+quote(query,safe=''),use_container_width=True)
    st.button('🎲 처음부터 다시 뽑기',type='primary',on_click=reset,use_container_width=True)
    st.caption('알레르기·세부 재료·날씨는 직접 확인해 주세요. 위치 자동 수집은 없으며 지도 검색 시 입력 동네가 지도 서비스로 전달돼요.')

if st.button('⌂ 시작 화면으로',use_container_width=True):
    reset()
    st.session_state.food_started=False
    st.rerun()
