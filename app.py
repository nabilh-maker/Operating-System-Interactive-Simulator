import streamlit as st
import time
import pandas as pd

# 1️⃣ ضبط إعدادات الصفحة لتكون بعرض الشاشة الكامل وبثيم داكن متناسق
st.set_page_config(
    page_title="OS Simulator - Teaching Version",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص التصميم بالألوان الأصلية الداكنة عبر CSS مخصص لـ Streamlit
st.markdown("""
    <style>
    .stApp {
        background-color: #0b1020;
        color: #ffffff;
    }
    .main-title {
        color: #00d4ff;
        font-family: 'Arial', sans-serif;
        text-align: center;
        font-weight: bold;
    }
    .sub-title {
        color: #aaaaff;
        text-align: center;
    }
    .doctor-info {
        color: #cccccc;
        font-style: italic;
        text-align: center;
        background-color: #111a30;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #334466;
    }
    /* تحسين شكل الأزرار */
    div.stButton > button {
        background-color: #00d4ff;
        color: black;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
    }
    div.stButton > button:hover {
        background-color: #00b4dd;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# إدارة التنقل بين الشاشات باستخدام الـ Session State البديل لـ الميثودز في Tkinter
if 'screen' not in st.session_state:
    st.session_state.screen = 'first'

# =========================================================
# 1️⃣ FIRST SCREEN (شاشة البداية والترحيب)
# =========================================================
if st.session_state.screen == 'first':
    st.markdown("<h2 class='main-title' style='font-size: 28px;'>جامعة الخليل - Hebron University</h2>", unsafe_allow_html=True)
    st.markdown("<h4 class='sub-title'>College of Information Technology<br>Department of Computer Science</h4>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: white; margin-top: 30px;'>🧠 OPERATING SYSTEMS SIMULATOR</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #334466; width: 60%; margin: auto;'>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    
    doc_text = """
    This Operating Systems Simulation was developed for the Operating Systems course by:<br>
    <strong>Dr. Eng. Nabil Hasasneh</strong><br>
    Associate Professor<br>
    2026
    """
    st.markdown(f"<p class='doctor-info'>{doc_text}</p>", unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("▶ START SIMULATION", use_container_width=True):
            st.session_state.screen = 'dashboard'
            st.rerun()

# =========================================================
# 2️⃣ DASHBOARD & INTERNAL PAGES (لوحة التحكم والتنقل)
# =========================================================
else:
    # القائمة الجانبية كبديل لشريط التنقل العلوي والأزرار
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        if st.button("🏠 Home / Dashboard", use_container_width=True):
            st.session_state.screen = 'dashboard'
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🧠 Algorithms")
        if st.button("📄 PAGING", use_container_width=True):
            st.session_state.screen = 'paging'
            st.rerun()
        if st.button("💾 ALLOCATION", use_container_width=True):
            st.session_state.screen = 'allocation'
            st.rerun()
        if st.button("🔒 BANKER", use_container_width=True):
            st.session_state.screen = 'banker'
            st.rerun()
        if st.button("🔁 SWAPPING", use_container_width=True):
            st.session_state.screen = 'swapping'
            st.rerun()
            
        st.markdown("---")
        if st.button("⬅ Back to Welcome Screen", use_container_width=True):
            st.session_state.screen = 'first'
            st.rerun()

    # شاشة الـ Dashboard الرئيسية
    if st.session_state.screen == 'dashboard':
        st.markdown("<h1 class='main-title'>OS SIMULATOR DASHBOARD</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("### 📄 PAGING\nSimulate page replacement algorithms and view Page Table mapping updates.")
            if st.button("Go to Paging", key="nav_page"):
                st.session_state.screen = 'paging'
                st.rerun()
                
            st.success("### 💾 ALLOCATION\nVisualize First-Fit, Best-Fit, and Worst-Fit contiguous memory allocation policies.")
            if st.button("Go to Allocation", key="nav_alloc"):
                st.session_state.screen = 'allocation'
                st.rerun()
                
        with col2:
            st.warning("### 🔒 BANKER'S ALGORITHM\nStep-by-step avoidance and detection of system deadlocks via safe-state sequence.")
            if st.button("Go to Banker", key="nav_bank"):
                st.session_state.screen = 'banker'
                st.rerun()
                
            st.error("### 🔁 SWAPPING\nObserve dynamic process Swapping visualization between RAM and Backing Store.")
            if st.button("Go to Swapping", key="nav_swap"):
                st.session_state.screen = 'swapping'
                st.rerun()

        st.markdown("<br><hr>", unsafe_allow_html=True)
        info_text = """
        This Operating Systems Simulation was developed for the Operating Systems course by<br>
        <strong>Dr. Eng. Nabil Hasasneh</strong><br>
        Associate Professor<br>
        Department of Computer Science | College of Information Technology<br>
        Hebron University &nbsp;2026
        """
        st.markdown(f"<p style='text-align:center; color:#aaaaff;'>{info_text}</p>", unsafe_allow_html=True)

    # 📄 محاكي الـ PAGING
    elif st.session_state.screen == 'paging':
        st.markdown("## 📄 Paging Reference String Simulator")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            ref_str = st.text_input("Reference String (separated by space):", value="7 0 1 2 0 3 0 4")
        with col2:
            fsize = st.number_input("Frame Size:", min_value=1, max_value=10, value=3)
            
        if st.button("▶ RUN PAGING"):
            try:
                pages = list(map(int, ref_str.split()))
                memory = []
                frame_map = {}
                faults = 0
                
                st.markdown("### Execution Timeline:")
                cols = st.columns(len(pages))
                
                for idx, p in enumerate(pages):
                    is_fault = False
                    if p not in memory:
                        faults += 1
                        is_fault = True
                        if len(memory) < fsize:
                            memory.append(p)
                            frame_map[p] = len(memory) - 1
                        else:
                            old_p = memory.pop(0)
                            old_frame = frame_map.pop(old_p, 0)
                            memory.append(p)
                            frame_map[p] = old_frame
                    
                    with cols[idx]:
                        st.metric(label=f"Step {idx+1} (In: {p})", value=f"P: {p}", delta="Fault" if is_fault else "Hit", delta_color="inverse" if is_fault else "normal")
                
                st.error(f"### Total Page Faults: {faults}")
                
                st.markdown("### 📊 Final Page Table (Page → Frame Mapping)")
                pt_data = [{"Page": p, "Frame": f} for p, f in frame_map.items()]
                st.table(pd.DataFrame(pt_data))
                
            except ValueError:
                st.error("Please enter a valid space-separated integers string.")

    # 💾 محاكي الـ ALLOCATION
    elif st.session_state.screen == 'allocation':
        st.markdown("## 💾 Memory Allocation Simulator (Real-Time Status)")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            holes_str = st.text_input("Memory Holes (KB):", value="100 500 200 300 400")
        with col2:
            procs_str = st.text_input("Processes (KB):", value="212 417 112 426")
        with col3:
            algo = st.selectbox("Allocation Algorithm:", ["First Fit", "Best Fit", "Worst Fit"])
            
        if st.button("▶ RUN ALLOCATION"):
            try:
                holes = list(map(int, holes_str.split()))
                procs = list(map(int, procs_str.split()))
                temp_holes = holes[:]
                alloc_result = []
                
                for proc in procs:
                    idx = -1
                    if algo == "First Fit":
                        for i, h in enumerate(temp_holes):
                            if h >= proc: idx = i; break
                    elif algo == "Best Fit":
                        best = 10**9
                        for i, h in enumerate(temp_holes):
                            if h >= proc and h < best: best = h; idx = i
                    elif algo == "Worst Fit":
                        worst = -1
                        for i, h in enumerate(temp_holes):
                            if h >= proc and h > worst: worst = h; idx = i
                            
                    if idx != -1:
                        leftover = temp_holes[idx] - proc
                        alloc_result.append({"Process": f"Proc ({proc} KB)", "Status": f"Allocated to Hole {idx}", "Remaining Hole Size": f"{leftover} KB", "Color": "🟢"})
                        temp_holes[idx] -= proc
                    else:
                        alloc_result.append({"Process": f"Proc ({proc} KB)", "Status": "NO FIT (Waiting)", "Remaining Hole Size": "-", "Color": "🔴"})
                
                st.markdown(f"### 📊 Simulation Summary Using **{algo}**")
                st.table(pd.DataFrame(alloc_result))
                
            except ValueError:
                st.error("Invalid Input Values.")

    # 🔒 محاكي خوارزمية الـ BANKER
    elif st.session_state.screen == 'banker':
        st.markdown("## 🔒 Banker's Algorithm – Deadlock Avoidance")
        
        n_proc, n_res = 5, 3
        alloc = [[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]]
        maxm = [[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]]
        avail = [3,3,2]
        need = [[maxm[i][j]-alloc[i][j] for j in range(n_res)] for i in range(n_proc)]
        
        st.markdown(f"**Initial Available Resources (A B C):** `{avail}`")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("##### 📊 Allocation Matrix")
            st.dataframe(pd.DataFrame(alloc, columns=['A', 'B', 'C'], index=[f"P{i}" for i in range(n_proc)]))
        with c2:
            st.markdown("##### 📊 Maximum Matrix")
            st.dataframe(pd.DataFrame(maxm, columns=['A', 'B', 'C'], index=[f"P{i}" for i in range(n_proc)]))
        with c3:
            st.markdown("##### 📊 Need Matrix")
            st.dataframe(pd.DataFrame(need, columns=['A', 'B', 'C'], index=[f"P{i}" for i in range(n_proc)]))
            
        if st.button("▶ RUN BANKER SIMULATION"):
            work = avail[:]
            finish = [False] * n_proc
            safe_seq = []
            logs = []
            
            count = 0
            while count < n_proc:
                found = False
                for i in range(n_proc):
                    if not finish[i]:
                        if all(need[i][j] <= work[j] for j in range(n_res)):
                            old_work = work[:]
                            for j in range(n_res):
                                work[j] += alloc[i][j]
                            finish[i] = True
                            found = True
                            safe_seq.append(f"P{i}")
                            count += 1
                            logs.append(f"🟢 P{i} can execute safely. Need {need[i]} <= Work {old_work}. New Available Work: {work}")
                            break
                if not found:
                    break
                    
            st.markdown("### 📋 Simulation Log:")
            for log in logs:
                st.write(log)
                
            if len(safe_seq) == n_proc:
                st.success(f"🎉 **SYSTEM IS IN A SAFE STATE!** Safe Path Sequence: **{' ➔ '.join(safe_seq)}**")
            else:
                st.error("⚠️ **SYSTEM IS IN AN UNSAFE STATE (POTENTIAL DEADLOCK)!**")

    # 🔁 محاكي الـ SWAPPING
    elif st.session_state.screen == 'swapping':
        st.markdown("## 🔁 Memory Swapping Simulation Mode")
        
        if st.button("▶ TRIGGER SWAP ANIMATION"):
            status_box = st.empty()
            progress_bar = st.progress(0)
            
            status_box.warning("🔄 Swapping Out: Moving **Process P1** from Main Memory (RAM) to Backing Store (Disk)...")
            for percent in range(1, 51):
                time.sleep(0.02)
                progress_bar.progress(percent)
                
            status_box.info("🔄 Swapping In: Loading **Process P2** from Backing Store (Disk) into Main Memory (RAM)...")
            for percent in range(51, 101):
                time.sleep(0.02)
                progress_bar.progress(percent)
                
            status_box.success("✅ Swapping Completed Successfully!")