import tkinter as tk
from tkinter import ttk
import random
import time

class OSSimulator:

    def __init__(self, root):
        self.root = root
        self.root.title("OS Simulator - Teaching Version")
        
        # ضبط حجم افتراضي وتفعيل خاصية ملء الشاشة تلقائياً لتظهر النافذة فوراً
        self.root.geometry("1200x700")
        try:
            self.root.state('zoomed') # لنظام ويندوز لجعل الشاشة كاملة
        except:
            try:
                self.root.attributes('-fullscreen', True) # للأنظمة الأخرى كـ الماك إذا لم يدعم الزوم
            except:
                pass
                
        self.root.configure(bg="#0b1020")

        self.main = tk.Frame(root, bg="#0b1020")
        self.main.pack(fill="both", expand=True)

        self.reset_state()
        self.first_screen()

# ================= STATE =================

    def reset_state(self):
        self.safe_seq = []
        self.finished = []
        self.bank_canvas = None
        self._swap_anim_id = None
        self._alloc_anim_id = None

# ================= CLEAR =================

    def clear(self):
        if self._swap_anim_id:
            self.root.after_cancel(self._swap_anim_id)
            self._swap_anim_id = None
        if self._alloc_anim_id:
            self.root.after_cancel(self._alloc_anim_id)
            self._alloc_anim_id = None
        for w in self.main.winfo_children():
            w.destroy()

# ================= NAV =================

    def nav(self, reset_func):
        bar = tk.Frame(self.main, bg="#0b1020")
        bar.pack(fill="x")
        tk.Button(bar, text="⬅ Back",   bg="#ff4d4d", fg="white",
                  command=self.dashboard).pack(side="left", padx=5)
        tk.Button(bar, text="🏠 Home",   bg="#00d4ff",
                  command=self.dashboard).pack(side="left", padx=5)
        tk.Button(bar, text="🔄 Reset",  bg="orange",
                  command=lambda: [reset_func(), self.dashboard()]
                  ).pack(side="left", padx=5)
        # زر الخروج السريع من شريط التنقل العلوي في الشاشات الداخلية
        tk.Button(bar, text="❌ Exit Simulation", bg="#b30000", fg="white", font=("Arial", 9, "bold"),
                  command=self.root.destroy).pack(side="right", padx=10, pady=2)

# =========================================================
# 1️⃣ FIRST SCREEN (شاشة البداية والترحيب)
# =========================================================

    def first_screen(self):
        self.clear()
        f = tk.Frame(self.main, bg="#0b1020")
        f.pack(expand=True)
        
        # 1. اسم جامعة الخليل والكلية والقسم
        tk.Label(f, text="جامعة الخليل - Hebron University",
                 font=("Arial", 18, "bold"), fg="#00d4ff", bg="#0b1020").pack(pady=2)
        tk.Label(f, text="College of Information Technology\nDepartment of Computer Science",
                 font=("Arial", 12), fg="#aaaaff", bg="#0b1020", justify="center").pack(pady=5)
                 
        # 2. اسم المشروع الرئيسي
        tk.Label(f, text="🧠 OPERATING SYSTEMS SIMULATOR",
                 font=("Arial", 28, "bold"), fg="#ffffff", bg="#0b1020").pack(pady=15)
        
        # خط فاصل جمالي رفيع
        tk.Frame(f, bg="#334466", height=2, width=400).pack(pady=15)

        # 3. بيانات مساق أنظمة التشغيل والدكتور المشرف نبيل حساسنة
        course_info = (
            "This Operating Systems Simulation was developed for the Operating Systems course by:\n"
            "Dr. Eng. Nabil Hasasneh\n"
            "Associate Professor\n"
            "2026"
        )
        tk.Label(f, text=course_info, font=("Arial", 12, "italic"), fg="#cccccc", bg="#0b1020", justify="center").pack(pady=10)
        
        # 4. زر بدء المحاكاة فقط
        tk.Button(f, text="▶ START SIMULATION", font=("Arial", 16, "bold"),
                  bg="#00d4ff", fg="black", activebackground="#00b4dd", bd=0, padx=20, pady=10,
                  command=self.dashboard).pack(pady=25)

# =========================================================
# 2️⃣ DASHBOARD
# =========================================================

    def dashboard(self):
        self.clear()
        
        # شريط علوي خاص بلوحة التحكم لإضافة زر الخروج بشكل متناسق بعد بدء البرنامج
        top_bar = tk.Frame(self.main, bg="#0b1020")
        top_bar.pack(fill="x", padx=10)
        tk.Button(top_bar, text="❌ Exit Simulation", bg="#b30000", fg="white", font=("Arial", 10, "bold"),
                  command=self.root.destroy).pack(side="right", pady=5)
                  
        tk.Label(self.main, text="OS SIMULATOR DASHBOARD",
                 font=("Arial", 26, "bold"), fg="white", bg="#0b1020").pack(pady=20)
        grid = tk.Frame(self.main, bg="#0b1020")
        grid.pack()
        self.card(grid, "📄 PAGING",     self.paging,     0, 0)
        self.card(grid, "💾 ALLOCATION", self.allocation, 0, 1)
        self.card(grid, "🔒 BANKER",     self.banker,     1, 0)
        self.card(grid, "🔁 SWAPPING",   self.swapping,   1, 1)

        # النص التعريفي الخاص بالدكتور في واجهة الـ Dashboard
        info_text = (
            "This Operating Systems Simulation was developed for the Operating Systems course by\n"
            "Dr. Eng. Nabil Hasasneh\n"
            "Associate Professor\n"
            "Department of Computer Science\n"
            "College of Information Technology\n"
            "Hebron University   2026"
        )
        tk.Label(self.main, text=info_text, font=("Arial", 13), fg="#aaaaff", bg="#0b1020", justify="center").pack(pady=30)

    def card(self, parent, text, cmd, r, c):
        colors = {"📄 PAGING":"#1e2a4a","💾 ALLOCATION":"#1b3b2f",
                  "🔒 BANKER":"#3b1b2f","🔁 SWAPPING":"#2f2f1b"}
        tk.Button(parent, text=text, font=("Arial", 18, "bold"),
                  width=18, height=3, bg=colors.get(text,"#1e2a4a"),
                  fg="white", command=cmd).grid(row=r, column=c, padx=15, pady=15)

# =========================================================
# 📄 PAGING
# =========================================================

    def paging(self):
        self.clear()
        self.nav(self.paging)
        frame = tk.Frame(self.main, bg="#0b1020")
        frame.pack(pady=10)
        
        tk.Label(frame, text="Reference String:", fg="white", bg="#0b1020").grid(row=0, column=0, padx=5)
        ref = tk.Entry(frame, width=40)
        ref.insert(0, "7 0 1 2 0 3 0 4")
        ref.grid(row=0, column=1, padx=5)
        
        tk.Label(frame, text="Frame Size:", fg="white", bg="#0b1020").grid(row=1, column=0, padx=5)
        size = tk.Entry(frame, width=10)
        size.insert(0, "3")
        size.grid(row=1, column=1, padx=5)
        
        canvas = tk.Canvas(self.main, bg="white", height=150)
        canvas.pack(fill="x", expand=False, padx=20, pady=10)
        
        table = tk.Frame(self.main, bg="white")
        table.pack(pady=10)
        tk.Label(table, text="PAGE TABLE (Page → Frame)",
                 bg="white", font=("Arial", 12, "bold")).pack()
        table_canvas = tk.Canvas(table, width=400, height=150, bg="white")
        table_canvas.pack()

        def run():
            try:
                pages  = list(map(int, ref.get().split()))
                fsize  = int(size.get())
            except ValueError:
                return
            
            memory = []
            frame_map = {}
            faults = 0
            canvas.delete("all")
            table_canvas.delete("all")
            
            for i, p in enumerate(pages):
                if p not in memory:
                    faults += 1
                    if len(memory) < fsize:
                        memory.append(p)
                        frame_map[p] = len(memory) - 1
                    else:
                        old_p = memory.pop(0)
                        if old_p in frame_map:
                            old_frame = frame_map.pop(old_p)
                        else:
                            old_frame = 0
                        memory.append(p)
                        frame_map[p] = old_frame
                canvas.create_text(80+i*60, 60, text=str(p), font=("Arial", 14, "bold"))
            
            y = 25
            for p, f in frame_map.items():
                table_canvas.create_text(200, y, text=f"Page {p} → Frame {f}",
                                         font=("Arial", 11, "bold"), fill="#1e2a4a")
                y += 25
            canvas.create_text(500, 120, text=f"Total Page Faults: {faults}",
                               fill="red", font=("Arial", 16, "bold"))

        tk.Button(frame, text="▶ RUN", bg="#00d4ff", command=run).grid(row=2, column=1, pady=10)

# =========================================================
# 💾 ALLOCATION – WITH REAL-TIME STEP BY STEP ANIMATION
# =========================================================

    def allocation(self):
        self.clear()
        self.nav(self.allocation)

        BG = "#0f1a2e"
        ctrl = tk.Frame(self.main, bg=BG)
        ctrl.pack(fill="x", padx=8, pady=4)

        tk.Label(ctrl, text="Memory Holes (KB):", fg="white", bg=BG,
                 font=("Courier",10,"bold")).grid(row=0,column=0,sticky="e",padx=4)
        holes_e = tk.Entry(ctrl, width=35, font=("Courier",10))
        holes_e.insert(0, "100 500 200 300 400")
        holes_e.grid(row=0,column=1,padx=4)

        tk.Label(ctrl, text="Processes (KB):", fg="white", bg=BG,
                 font=("Courier",10,"bold")).grid(row=0,column=2,sticky="e",padx=4)
        procs_e = tk.Entry(ctrl, width=28, font=("Courier",10))
        procs_e.insert(0, "212 417 112 426")
        procs_e.grid(row=0,column=3,padx=4)

        algo_v = tk.StringVar(value="Best Fit")
        for i,(lbl,val) in enumerate([("First Fit","First Fit"),
                                       ("Best Fit","Best Fit"),
                                       ("Worst Fit","Worst Fit")]):
            tk.Radiobutton(ctrl, text=lbl, variable=algo_v, value=val,
                           fg="#00d4ff", bg=BG, selectcolor="#001133",
                           font=("Courier",10,"bold")).grid(row=0,column=4+i,padx=6)

        tk.Button(ctrl, text="▶ RUN ANIMATION", bg="#00ff99", fg="black",
                 font=("Courier",11,"bold"),
                 command=lambda: start_alloc_simulation()).grid(row=0,column=7,padx=10)

        canvas = tk.Canvas(self.main, bg="#07111f")
        canvas.pack(fill="both", expand=True)

        leg = tk.Frame(self.main, bg=BG)
        leg.pack(fill="x", padx=8, pady=2)
        for color, label in [("#4a90d9","Free / Hole"), ("#e05c5c","Process (allocated)"),
                              ("#f5a623","Internal Fragmentation"), ("#888888","External Fragmentation")]:
            tk.Label(leg, text="■", fg=color, bg=BG, font=("Arial",16)).pack(side="left")
            tk.Label(leg, text=label+"   ", fg="white", bg=BG, font=("Courier",9)).pack(side="left")

        summary_var = tk.StringVar(value="")
        tk.Label(self.main, textvariable=summary_var, fg="#ffdd00", bg=BG,
                 font=("Courier",10,"bold")).pack(pady=2)

        def start_alloc_simulation():
            if self._alloc_anim_id:
                self.root.after_cancel(self._alloc_anim_id)
            
            try:
                holes_orig = list(map(int, holes_e.get().split()))
                procs_orig = list(map(int, procs_e.get().split()))
            except ValueError:
                summary_var.set("⚠ Invalid input")
                return

            algo = algo_v.get()
            alloc_result = []
            
            W = canvas.winfo_width() if canvas.winfo_width() > 10 else 1200
            SCALE = (W * 0.55) / sum(holes_orig)
            MEM_X0, MEM_Y0, MEM_H, PROC_Y0 = 60, 60, 70, 200
            process_colors = ["#e05c5c","#d45fd4","#5cd4a0","#d4a05c","#5c9cd4"]

            def draw_state(current_p_idx):
                canvas.delete("all")
                canvas.create_text(W//2, 20, text=f"Memory Allocation Model: {algo} (Step {current_p_idx+1})", font=("Courier",14,"bold"), fill="#00d4ff")
                
                x = MEM_X0
                hole_xs = []
                for h in holes_orig:
                    w = int(h * SCALE)
                    hole_xs.append(x)
                    canvas.create_rectangle(x, MEM_Y0, x+w, MEM_Y0+MEM_H, fill="#1a3a5c", outline="#4a90d9", width=2)
                    canvas.create_text(x+w//2, MEM_Y0+MEM_H//2, text=f"Hole\n{h} KB", fill="#4a90d9", font=("Courier",9,"bold"))
                    x += w

                hole_drawn = {i:[] for i in range(len(holes_orig))}
                
                for pi in range(current_p_idx + 1):
                    if pi >= len(procs_orig): break
                    proc = procs_orig[pi]
                    hidx = alloc_result[pi][1]
                    leftover = alloc_result[pi][2]
                    col = process_colors[pi % len(process_colors)]
                    
                    if hidx != -1:
                        start_kb = sum(r[1] for r in hole_drawn[hidx])
                        hole_drawn[hidx].append((start_kb, proc, col, f"P{pi}\n{proc}KB"))
                        if leftover > 0 and pi == current_p_idx:
                            hole_drawn[hidx].append((start_kb+proc, leftover, "#f5a623", f"IF\n{leftover}KB"))

                for hi, segs in hole_drawn.items():
                    hx0 = hole_xs[hi]
                    for (start_kb, size_kb, col, lbl) in segs:
                        sx = hx0 + int(start_kb * SCALE)
                        sw = max(int(size_kb * SCALE), 2)
                        canvas.create_rectangle(sx, MEM_Y0, sx+sw, MEM_Y0+MEM_H, fill=col, outline="white")
                        if sw > 20:
                            canvas.create_text(sx+sw//2, MEM_Y0+MEM_H//2, text=lbl, fill="white", font=("Courier",8,"bold"))

                PROC_BW = 90
                for pi, proc in enumerate(procs_orig):
                    col = process_colors[pi % len(process_colors)]
                    px = MEM_X0 + pi*(PROC_BW+12)
                    
                    border_w = 4 if pi == current_p_idx else 1
                    outline_c = "#ffdd00" if pi == current_p_idx else "white"
                    
                    bg_c = "#333333"
                    status = "Waiting..."
                    if pi <= current_p_idx:
                        hidx = alloc_result[pi][1]
                        bg_c = col if hidx != -1 else "#551111"
                        status = f"→ Hole {hidx}" if hidx != -1 else "NO FIT"

                    canvas.create_rectangle(px, PROC_Y0, px+PROC_BW, PROC_Y0+50, fill=bg_c, outline=outline_c, width=border_w)
                    canvas.create_text(px+PROC_BW//2, PROC_Y0+25, text=f"P{pi}\n{proc}KB\n{status}", fill="white", font=("Courier",8,"bold"))
                    
                    if pi <= current_p_idx and alloc_result[pi][1] != -1:
                        hx = hole_xs[alloc_result[pi][1]] + int(holes_orig[alloc_result[pi][1]]*SCALE//2)
                        canvas.create_line(px+PROC_BW//2, PROC_Y0, hx, MEM_Y0+MEM_H, fill=col, width=2, arrow=tk.LAST, dash=(4,2))

            temp_holes = holes_orig[:]
            for proc in procs_orig:
                idx = -1
                if algo == "First Fit":
                    for i, h in enumerate(temp_holes):
                        if h >= proc: idx = i; break
                elif algo == "Best Fit":
                    best = 10**9
                    for i, h in enumerate(temp_holes):
                        if h >= proc and h < best:
                            best = h
                            idx = i
                elif algo == "Worst Fit":
                    worst = -1
                    for i, h in enumerate(temp_holes):
                        if h >= proc and h > worst:
                            worst = h
                            idx = i

                if idx != -1:
                    leftover = temp_holes[idx] - proc
                    alloc_result.append((proc, idx, leftover))
                    temp_holes[idx] -= proc
                else:
                    alloc_result.append((proc, -1, 0))

            def next_anim_step(step):
                if step < len(procs_orig):
                    draw_state(step)
                    self._alloc_anim_id = self.root.after(1200, lambda: next_anim_step(step+1))
                else:
                    summary_var.set(f"Simulation Done! Algorithm: {algo} finished placement execution.")

            next_anim_step(0)

# =========================================================
# 🔒 BANKER'S ALGORITHM
# =========================================================

    def banker(self):
        self.clear()
        self.nav(self.banker)
        self.reset_state()

        self.n_proc = 5
        self.n_res  = 3
        self.alloc  = [[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]]
        self.maxm   = [[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]]
        self.avail  = [3,3,2]
        self.need   = [[self.maxm[i][j]-self.alloc[i][j] for j in range(self.n_res)] for i in range(self.n_proc)]

        self.sim_step  = 0
        self.sim_steps = []

        BG = "#0f1a30"
        outer = tk.Frame(self.main, bg=BG)
        outer.pack(fill="both", expand=True, padx=6, pady=4)

        left  = tk.Frame(outer, bg=BG)
        left.pack(side="left", fill="both", expand=True)
        right = tk.Frame(outer, bg=BG, width=420)
        right.pack(side="right", fill="y", padx=(6,0))
        right.pack_propagate(False)

        tk.Label(left, text="🔒 Banker's Algorithm – Deadlock Avoidance", font=("Courier",15,"bold"), fg="#00d4ff", bg=BG).pack(pady=(4,2))
        tk.Label(left, text="Resources Available Vector:  A   B   C", font=("Courier",11), fg="#aaaaff", bg=BG).pack()

        avail_frame = tk.Frame(left, bg=BG)
        avail_frame.pack(pady=2)
        self.avail_labels = []
        for j in range(self.n_res):
            lbl = tk.Label(avail_frame, text=str(self.avail[j]), font=("Courier",13,"bold"), fg="#ffdd00", bg="#1a2a10", width=5, relief="ridge")
            lbl.pack(side="left", padx=3)
            self.avail_labels.append(lbl)

        tables_frame = tk.Frame(left, bg=BG)
        tables_frame.pack(pady=6, fill="x")

        def make_table(parent, title, data, color):
            f = tk.Frame(parent, bg=BG)
            f.pack(side="left", padx=12)
            tk.Label(f, text=title, font=("Courier",12,"bold"), fg=color, bg=BG).grid(row=0,column=0,columnspan=self.n_res+1)
            tk.Label(f, text="Proc", font=("Courier",10,"bold"), fg="white", bg="#1e2e4a", width=5).grid(row=1,column=0,padx=1,pady=1)
            for j,c in enumerate(["A","B","C"]):
                tk.Label(f, text=c, font=("Courier",10,"bold"), fg="white", bg="#1e2e4a", width=5).grid(row=1,column=j+1,padx=1,pady=1)
            cells = []
            for i in range(self.n_proc):
                row_c = []
                tk.Label(f, text=f"P{i}", font=("Courier",10,"bold"), fg="#aaaaff", bg=BG, width=5).grid(row=i+2,column=0,padx=1,pady=1)
                for j in range(self.n_res):
                    cell = tk.Label(f, text=str(data[i][j]), font=("Courier",11), fg="white", bg="#141e30", width=5, relief="ridge")
                    cell.grid(row=i+2,column=j+1,padx=1,pady=1)
                    row_c.append(cell)
                cells.append(row_c)
            return cells

        self.alloc_cells = make_table(tables_frame,"📊 Allocation",self.alloc,"#00ff99")
        self.maxm_cells  = make_table(tables_frame,"📊 Maximum",  self.maxm, "#ff9900")
        self.need_cells  = make_table(tables_frame,"📊 Need (Max-Alloc)", self.need, "#ff66cc")

        status_f = tk.Frame(left, bg=BG)
        status_f.pack(pady=4)
        tk.Label(status_f, text="Execution Status:", font=("Courier",11,"bold"), fg="#aaaaff", bg=BG).pack(side="left", padx=6)
        self.proc_status = []
        for i in range(self.n_proc):
            lbl = tk.Label(status_f, text=f"P{i}", font=("Courier",11,"bold"), fg="white", bg="#2a2a2a", width=5, relief="ridge")
            lbl.pack(side="left", padx=2)
            self.proc_status.append(lbl)

        seq_outer = tk.Frame(left, bg=BG)
        seq_outer.pack(pady=10, fill="x", padx=20)
        tk.Label(seq_outer, text="🚀 SAFE PATH SEQUENCE:", font=("Courier",11,"bold"), fg="#ffdd00", bg=BG).pack(side="left")
        self.seq_frame = tk.Frame(seq_outer, bg=BG)
        self.seq_frame.pack(side="left", padx=8)

        btn_f = tk.Frame(left, bg=BG)
        btn_f.pack(pady=6)
        tk.Button(btn_f, text="▶ RUN INSTANT", font=("Courier",11,"bold"), bg="#00d4ff", fg="black", padx=10, command=self.banker_run_instant).pack(side="left", padx=6)
        tk.Button(btn_f, text="⏭ STEP BY STEP", font=("Courier",11,"bold"), bg="#ffdd00", fg="black", padx=10, command=self.banker_next_step).pack(side="left", padx=6)
        tk.Button(btn_f, text="🔄 Reset", font=("Courier",11,"bold"), bg="#ff6666", fg="white", padx=10, command=self.banker_reset_view).pack(side="left", padx=6)

        tk.Label(right, text="📋 Banker Simulation Log", font=("Courier",12,"bold"), fg="#00d4ff", bg=BG).pack(pady=(6,2))
        log_scroll = tk.Scrollbar(right)
        log_scroll.pack(side="right", fill="y")
        self.log_text = tk.Text(right, font=("Courier",10), bg="#0a0f1e", fg="#cccccc", yscrollcommand=log_scroll.set, state="disabled", wrap="word")
        self.log_text.pack(fill="both", expand=True)
        log_scroll.config(command=self.log_text.yview)
        
        self.log_text.tag_config("head", foreground="#00d4ff", font=("Courier",10,"bold"))
        self.log_text.tag_config("ok", foreground="#00ff99")
        self.log_text.tag_config("skip", foreground="#888888")
        self.log_text.tag_config("safe", foreground="#ffdd00", font=("Courier",11,"bold"))

        self._build_steps()
        self._log_initial_state()

    def _log(self, text, tag=""):
        self.log_text.config(state="normal")
        self.log_text.insert("end", text+"\n", tag)
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _log_initial_state(self):
        self._log("="*38,"head")
        self._log("  BANKER'S SAFE PATH DETECTION","head")
        self._log("="*38,"head")
        self._log(f"  Available Work Vector: {self.avail}")
        self._log("  Rule: If Need <= Work -> Safe to execute")

    def _build_steps(self):
        work = self.avail[:]
        finish = [False] * self.n_proc
        self.sim_steps = []
        
        count = 0
        while count < self.n_proc:
            found = False
            for i in range(self.n_proc):
                if not finish[i]:
                    if all(self.need[i][j] <= work[j] for j in range(self.n_res)):
                        old_work = work[:]
                        for j in range(self.n_res):
                            work[j] += self.alloc[i][j]
                        finish[i] = True
                        found = True
                        count += 1
                        self.sim_steps.append({
                            "proc": i, "success": True, 
                            "need": self.need[i], "alloc": self.alloc[i],
                            "old_work": old_work, "new_work": work[:]
                        })
            if not found:
                for i in range(self.n_proc):
                    if not finish[i]:
                        self.sim_steps.append({
                            "proc": i, "success": False,
                            "need": self.need[i], "work": work[:]
                        })
                break

    def banker_next_step(self):
        if self.sim_step >= len(self.sim_steps):
            self._log("\n➔ Simulation ended.", "head")
            return

        step = self.sim_steps[self.sim_step]
        p = step["proc"]

        if step["success"]:
            self.proc_status[p].config(bg="#00ff99", fg="black", text="DONE")
            for j in range(self.n_res):
                self.need_cells[p][j].config(bg="#003311", fg="#00ff99")
                self.avail_labels[j].config(text=str(step["new_work"][j]))
            
            tk.Label(self.seq_frame, text=f" P{p} ", font=("Courier",12,"bold"), bg="#00ff99", fg="black").pack(side="left", padx=2)
            self._log(f"✔ P{p}: Need{step['need']} <= Work{step['old_work']} -> Safe!", "ok")
            self._log(f"   Released Alloc {step['alloc']} -> New Work: {step['new_work']}\n")
        else:
            self.proc_status[p].config(bg="#ff4d4d", fg="white", text="WAIT")
            self._log(f"✖ P{p}: Need{step['need']} > Work{step['work']} -> Cannot allocate! Skipping...", "skip")

        self.sim_step += 1
        if self.sim_step == len(self.sim_steps) and all(s.get("success", False) for s in self.sim_steps[:self.n_proc]):
            self._log("➔ SYSTEM IS IN SAFE STATE! 🎉", "safe")

    def banker_run_instant(self):
        while self.sim_step < len(self.sim_steps):
            self.banker_next_step()

    def banker_reset_view(self):
        self.banker()

# =========================================================
# 🔁 SWAPPING
# =========================================================

    def swapping(self):
        self.clear()
        self.nav(self.swapping)
        
        canvas = tk.Canvas(self.main, bg="#0d1b2a")
        canvas.pack(fill="both", expand=True)
        canvas.create_text(800, 200, text="🔁 Memory Swapping Simulation Mode", font=("Arial", 24, "bold"), fill="#00d4ff")
        canvas.create_rectangle(300, 300, 600, 550, outline="#ffdd00", width=3)
        canvas.create_text(450, 425, text="Main Memory\n(RAM)", fill="white", font=("Arial", 14))
        
        canvas.create_rectangle(1000, 300, 1300, 550, outline="#00ff99", width=3)
        canvas.create_text(1150, 425, text="Backing Store\n(Disk)", fill="white", font=("Arial", 14))

        def do_swap():
            canvas.create_line(600, 380, 1000, 380, fill="#ff4d4d", width=4, arrow=tk.LAST, tag="arrow")
            canvas.create_text(800, 360, text="Swap Out (P1)", fill="#ff4d4d", font=("Courier", 12, "bold"), tag="arrow")
            self.root.after(1500, lambda: [
                canvas.delete("arrow"),
                canvas.create_line(1000, 480, 600, 480, fill="#00ff99", width=4, arrow=tk.LAST),
                canvas.create_text(800, 500, text="Swap In (P2)", fill="#00ff99", font=("Courier", 12, "bold"))
            ])

        tk.Button(self.main, text="▶ TRIGGER SWAP ANIMATION", bg="#ffdd00", font=("Arial", 12, "bold"), command=do_swap).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = OSSimulator(root)
    root.mainloop()