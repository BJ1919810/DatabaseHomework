import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import psycopg2, uuid, datetime
# 主题配色
BG_COLOR = "#f0f4f8"
BTN_COLOR = "#4a90e2"
BTN_TEXT_COLOR = "#ffffff"
TITLE_COLOR = "#2c3e50"
TEXT_COLOR = "#34495e"

# 按钮样式
def styled_button(master, text, command=None):
    return tk.Button(
        master,
        text=text,
        command=command,
        width=20,
        height=2,
        font=("微软雅黑", 12),
        bg=BTN_COLOR,
        fg=BTN_TEXT_COLOR,
        activebackground="#357ABD",
        activeforeground=BTN_TEXT_COLOR,
        bd=0,
        relief="flat",
        cursor="hand2"
    )

# ========= 管理员登录界面 =========
def open_admin_login(parent_window):
    parent_window.destroy()  # 关闭主窗口

    login_win = tk.Tk()
    login_win.title("管理员登录")
    login_win.geometry("558x883")
    login_win.resizable(False, False)
    login_win.configure(bg=BG_COLOR)

    # 上方留白
    tk.Frame(login_win, height=150, bg=BG_COLOR).pack()

    # 标题
    title = tk.Label(
        login_win,
        text="管理员登录",
        font=("微软雅黑", 24, "bold"),
        pady=20,
        fg=TITLE_COLOR,
        bg=BG_COLOR
    )
    title.pack()

    # 表单框架
    form_frame = tk.Frame(login_win, bg=BG_COLOR)
    form_frame.pack(pady=30)

    # 管理员账号
    tk.Label(form_frame, text="管理员账号：", font=("微软雅黑", 12), bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, pady=10, sticky="e")
    entry_admin_id = tk.Entry(form_frame, width=30, font=("微软雅黑", 12))
    entry_admin_id.grid(row=0, column=1, pady=10)

    # 管理员密码
    tk.Label(form_frame, text="管理员密码：", font=("微软雅黑", 12), bg=BG_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, pady=10, sticky="e")
    entry_admin_pwd = tk.Entry(form_frame, width=30, font=("微软雅黑", 12), show="*")
    entry_admin_pwd.grid(row=1, column=1, pady=10)

    btn_frame = tk.Frame(login_win, bg=BG_COLOR)
    btn_frame.pack(pady=100)

    # 登录按钮
    def login_action():
        admin_id = entry_admin_id.get().strip()
        admin_pwd = entry_admin_pwd.get().strip()
        def open_admin_dashboard(admin_id):
            dash = tk.Tk()
            dash.title("管理员后台")
            dash.geometry("558x883")
            dash.configure(bg=BG_COLOR)
            # 标题
            tk.Label(
                dash,
                text=f"欢迎，管理员 {admin_id}",
                font=("微软雅黑", 20, "bold"),
                bg=BG_COLOR,
                fg=TITLE_COLOR
            ).pack(pady=60)

            # 按钮容器
            btn_frame = tk.Frame(dash, bg=BG_COLOR)
            btn_frame.pack()

            def open_book_manage_page():
                book_win = tk.Tk()
                book_win.title("图书信息管理")
                book_win.geometry("558x883")
                book_win.configure(bg=BG_COLOR)

                # ---------- 标题 ----------
                tk.Label(book_win, text="图书信息", font=("微软雅黑", 20, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

                # ---------- 上方输入框 和 按钮区域并列 ----------
                form_frame = tk.Frame(book_win, bg=BG_COLOR)
                form_frame.pack(pady=10)

                # 左边：输入框区域
                input_frame = tk.Frame(form_frame, bg=BG_COLOR)
                input_frame.pack(side="left", padx=20)

                fields = [
                    ("编号", "BookID"),
                    ("标题", "Title"),
                    ("作者", "Author"),
                    ("出版社", "Publisher"),
                    ("ISBN", "ISBN"),
                    ("总数目", "TotalCopies"),
                    ("可借阅数目", "AvailableCopies"),
                ]

                entry_vars = {}
                for idx, (label_text, field_name) in enumerate(fields):
                    tk.Label(
                        input_frame,
                        text=f"{label_text}：",
                        font=("微软雅黑", 12),
                        bg=BG_COLOR,
                        fg=TEXT_COLOR
                    ).grid(row=idx, column=0, pady=5, padx=5, sticky="e")

                    var = tk.StringVar()
                    entry = tk.Entry(input_frame, textvariable=var, width=25, font=("微软雅黑", 12))
                    entry.grid(row=idx, column=1, pady=5, padx=5)
                    entry_vars[field_name] = var

                # 右边：按钮区域
                button_frame = tk.Frame(form_frame, bg=BG_COLOR)
                button_frame.pack(side="left", padx=20)

                # 三个操作按钮
                styled_button(button_frame, "新建图书信息", lambda: insert_book()).pack(pady=5)
                styled_button(button_frame, "更新选中图书信息", lambda: update_book()).pack(pady=5)
                styled_button(button_frame, "删除选中图书信息", lambda: delete_book()).pack(pady=5)

                # ---------- Treeview 表格 ----------
                columns = [label_text for idx, (label_text, field_name) in enumerate(fields)]
                tree = ttk.Treeview(book_win, columns=columns, show="headings", height=10)

                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, anchor="center", width=80)

                tree.pack(pady=20)

                # ---------- 返回按钮 ----------
                def go_back():
                    book_win.destroy()
                    open_admin_dashboard(admin_id)

                styled_button(book_win, "返回", lambda: go_back()).pack(pady=10)


                # ---------- 数据库相关函数 ----------
                def update_table():
                    tree.delete(*tree.get_children())
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM book_k")
                    for row in cur.fetchall():
                        tree.insert("", "end", values=row)
                    cur.close()
                
                    def on_tree_select(event):
                        selected = tree.focus()
                        if not selected:
                            return
                        values = tree.item(selected, "values")
                        for i, (_, field_name) in enumerate(fields):
                            entry_vars[field_name].set(values[i])

                    tree.bind("<<TreeviewSelect>>", on_tree_select)

                def insert_book():
                    try:
                        cur = conn.cursor()
                        values = tuple(entry_vars[f].get() for _, f in fields)
                        cur.execute("INSERT INTO book_k VALUES (%s, %s, %s, %s, %s, %s, %s)", values)
                        conn.commit()
                        cur.close()
                        update_table()
                    except Exception as e:
                        messagebox.showerror("错误", f"插入失败：{e}")

                def update_book():
                    try:
                        selected = tree.focus()
                        if not selected:
                            messagebox.showwarning("提示", "请选择要更新的图书记录")
                            return
                        selected_id = tree.item(selected)["values"][0]
                        cur = conn.cursor()
                        values = tuple(entry_vars[f].get() for _, f in fields[1:])  # 不更新主键
                        cur.execute(f"""
                            UPDATE book_k SET 
                                Title=%s, Author=%s, Publisher=%s, ISBN=%s, 
                                TotalCopies=%s, AvailableCopies=%s 
                            WHERE BookID=%s
                        """, (*values, selected_id))
                        conn.commit()
                        cur.close()
                        update_table()
                    except Exception as e:
                        messagebox.showerror("错误", f"更新失败：{e}")

                def delete_book():
                    try:
                        selected = tree.focus()
                        if not selected:
                            messagebox.showwarning("提示", "请选择要删除的图书记录")
                            return
                        selected_id = tree.item(selected)["values"][0]
                        cur = conn.cursor()
                        cur.execute("DELETE FROM book_k WHERE BookID = %s", (selected_id,))
                        conn.commit()
                        cur.close()
                        update_table()
                    except Exception as e:
                        messagebox.showerror("错误", f"删除失败：{e}")

                # 初始更新
                update_table()
            
            # 各按钮事件
            def open_book_manage():
                dash.destroy()
                open_book_manage_page()

            def open_record_manage_page():
                record_win = tk.Tk()
                record_win.title("借阅记录管理")
                record_win.geometry("558x883")
                record_win.configure(bg=BG_COLOR)

                tk.Label(record_win, text="借阅记录", font=("微软雅黑", 20, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

                form_frame = tk.Frame(record_win, bg=BG_COLOR)
                form_frame.pack(pady=10)

                input_frame = tk.Frame(form_frame, bg=BG_COLOR)
                input_frame.pack(side="left", padx=20)

                fields = [
                    ("编号", "RecordID"),
                    ("借阅人ID", "UserID"),
                    ("图书编号", "BookID"),
                    ("借阅日期", "BorrowDate"),
                    ("应归还日期", "DueDate"),
                    ("归还日期", "ReturnDate"),
                ]

                entry_vars = {}
                for idx, (label_text, field_name) in enumerate(fields):
                    tk.Label(input_frame, text=f"{label_text}：", font=("微软雅黑", 12), bg=BG_COLOR, fg=TEXT_COLOR).grid(row=idx, column=0, pady=5, padx=5, sticky="e")
                    var = tk.StringVar()
                    entry = tk.Entry(input_frame, textvariable=var, width=25, font=("微软雅黑", 12))
                    entry.grid(row=idx, column=1, pady=5, padx=5)
                    entry_vars[field_name] = var

                button_frame = tk.Frame(form_frame, bg=BG_COLOR)
                button_frame.pack(side="left", padx=20)

                styled_button(button_frame, "新建借阅记录", lambda: insert_record()).pack(pady=5)
                styled_button(button_frame, "更新选中借阅记录", lambda: update_record()).pack(pady=5)
                styled_button(button_frame, "删除选中借阅记录", lambda: delete_record()).pack(pady=5)

                # 包含真实ID的列（隐藏）+ 显示列
                columns = ["编号", "借阅人ID", "借阅人姓名", "图书ID", "图书名称", "借阅日期", "应归还日期", "归还日期"]
                tree = ttk.Treeview(record_win, columns=columns, show="headings", height=10)

                for col in columns:
                    tree.heading(col, text=col)
                    if col in ["UserID", "BookID"]:
                        tree.column(col, width=0, stretch=False)
                    else:
                        tree.column(col, anchor="center", width=80)

                tree.tag_configure("late", foreground="red")
                tree.pack(pady=20)

                def go_back():
                    record_win.destroy()
                    open_admin_dashboard(admin_id)

                styled_button(record_win, "返回", lambda: go_back()).pack(pady=10)

                def update_table():
                    tree.delete(*tree.get_children())
                    cur = conn.cursor()
                    cur.execute("""
                        SELECT r.RecordID, r.UserID, u.UserName, r.BookID, b.Title, r.BorrowDate, r.DueDate, r.ReturnDate
                        FROM record_k r
                        LEFT JOIN user_k u ON r.UserID = u.UserID
                        LEFT JOIN book_k b ON r.BookID = b.BookID
                    """)
                    for row in cur.fetchall():
                        tag = "late" if row[5] and row[6] and row[5] > row[6] else ""
                        tree.insert("", "end", values=row, tags=(tag,))
                    cur.close()

                def on_tree_select(event):
                    selected = tree.focus()
                    if not selected:
                        return
                    values = tree.item(selected, "values")
                    if values:
                        entry_vars["RecordID"].set(values[0])
                        entry_vars["UserID"].set(values[1])   # hidden but used
                        entry_vars["BookID"].set(values[3])   # hidden but used
                        entry_vars["BorrowDate"].set(values[5])
                        entry_vars["DueDate"].set(values[6])
                        entry_vars["ReturnDate"].set(values[7])

                tree.bind("<<TreeviewSelect>>", on_tree_select)

                def insert_record():
                    try:
                        values = {f: entry_vars[f].get() for _, f in fields}

                        cur = conn.cursor()
                        cur.execute("SELECT 1 FROM user_k WHERE UserID = %s", (values["UserID"],))
                        if not cur.fetchone():
                            messagebox.showerror("错误", f"用户ID {values['UserID']} 不存在")
                            return

                        cur.execute("SELECT 1 FROM book_k WHERE BookID = %s", (values["BookID"],))
                        if not cur.fetchone():
                            messagebox.showerror("错误", f"图书ID {values['BookID']} 不存在")
                            return

                        cur.execute("INSERT INTO record_k VALUES (%s, %s, %s, %s, %s, %s)", (
                            values["RecordID"], values["UserID"], values["BookID"],
                            values["BorrowDate"], values["DueDate"], values["ReturnDate"]
                        ))
                        conn.commit()
                        cur.close()
                        update_table()
                    except Exception as e:
                        messagebox.showerror("错误", f"插入失败：{e}")

                def update_record():
                    selected = tree.focus()
                    if not selected:
                        messagebox.showwarning("提示", "请选择要更新的记录")
                        return
                    selected_id = tree.item(selected)["values"][0]
                    values = {f: entry_vars[f].get() for _, f in fields}

                    try:
                        cur = conn.cursor()
                        cur.execute("SELECT 1 FROM user_k WHERE UserID = %s", (values["UserID"],))
                        if not cur.fetchone():
                            messagebox.showerror("错误", f"用户ID {values['UserID']} 不存在")
                            return

                        cur.execute("SELECT 1 FROM book_k WHERE BookID = %s", (values["BookID"],))
                        if not cur.fetchone():
                            messagebox.showerror("错误", f"图书ID {values['BookID']} 不存在")
                            return

                        cur.execute("""
                            UPDATE record_k SET 
                                UserID=%s, BookID=%s, BorrowDate=%s, DueDate=%s, ReturnDate=%s
                            WHERE RecordID=%s
                        """, (
                            values["UserID"], values["BookID"], values["BorrowDate"],
                            values["DueDate"], values["ReturnDate"], selected_id
                        ))
                        conn.commit()
                        cur.close()
                        update_table()
                    except Exception as e:
                        messagebox.showerror("错误", f"更新失败：{e}")

                def delete_record():
                    selected = tree.focus()
                    if not selected:
                        messagebox.showwarning("提示", "请选择要删除的记录")
                        return
                    selected_id = tree.item(selected)["values"][0]
                    try:
                        cur = conn.cursor()
                        cur.execute("DELETE FROM record_k WHERE RecordID = %s", (selected_id,))
                        conn.commit()
                        cur.close()
                        update_table()
                    except Exception as e:
                        messagebox.showerror("错误", f"删除失败：{e}")

                update_table()


            # 管理借阅记录
            def open_record_manage():
                dash.destroy()
                open_record_manage_page()

            def go_back():
                dash.destroy()
                main()

            # 按钮摆放
            styled_button(btn_frame, "管理图书信息", open_book_manage).pack(pady=15)
            styled_button(btn_frame, "管理借阅记录", open_record_manage).pack(pady=15)
            styled_button(btn_frame, "返回", go_back).pack(pady=40)

            dash.mainloop()

        try:
            conn = psycopg2.connect(
                host="localhost",
                port=8888,
                database="mydb",
                user="dbuser",
                password="Test@123"
            )
            cur = conn.cursor()
            query = "SELECT * FROM admin_login_k WHERE admin_id = %s AND admin_pass = %s"
            cur.execute(query, (admin_id, admin_pwd))
            result = cur.fetchone()

            if result:
                login_win.destroy()
                open_admin_dashboard(admin_id)
            else:
                messagebox.showerror("登录失败", "账号或密码错误！")

            cur.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("数据库错误", str(e))

    styled_button(btn_frame, "登录", login_action).pack(pady=10)

    # 返回首页按钮
    def back_to_home():
        login_win.destroy()
        main()  # 重新打开主界面

    styled_button(btn_frame, "返回首页", back_to_home).pack(pady=10)

    login_win.mainloop()

# ========= 用户登录界面 =========
def open_user_login(parent_window):
    parent_window.destroy()
    login_win = tk.Tk()
    login_win.title("用户登录")
    login_win.geometry("558x883")
    login_win.resizable(False, False)
    login_win.configure(bg=BG_COLOR)

    # 上方留白
    tk.Frame(login_win, height=150, bg=BG_COLOR).pack()

    # 标题
    title = tk.Label(
        login_win,
        text="用户登录",
        font=("微软雅黑", 24, "bold"),
        pady=10,
        fg=TITLE_COLOR,
        bg=BG_COLOR
    )
    title.pack()

    # 表单区域
    form_frame = tk.Frame(login_win, bg=BG_COLOR)
    form_frame.pack(pady=30)

    tk.Label(form_frame, text="用户账号：", font=("微软雅黑", 12), bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, pady=10, sticky="e")
    entry_user_id = tk.Entry(form_frame, width=30, font=("微软雅黑", 12))
    entry_user_id.grid(row=0, column=1, pady=10)

    tk.Label(form_frame, text="用户密码：", font=("微软雅黑", 12), bg=BG_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, pady=10, sticky="e")
    entry_user_pwd = tk.Entry(form_frame, width=30, font=("微软雅黑", 12), show="*")
    entry_user_pwd.grid(row=1, column=1, pady=10)

    # 子页面
    def open_user_dashboard(user_id):
        dash = tk.Tk()
        dash.title("用户后台")
        dash.geometry("558x883")
        dash.configure(bg=BG_COLOR)
        try:
            try:
                conn = psycopg2.connect(
                    host="localhost",
                    port=8888,
                    database="mydb",
                    user="dbuser",
                    password="Test@123"
                )
            except Exception as e:
                messagebox.showerror("数据库连接失败", f"错误信息：{e}")
                return
            cur = conn.cursor()
            cur.execute("SELECT UserName FROM user_k WHERE UserID = %s", (user_id,))
            result = cur.fetchone()
            user_name = result[0].strip() if result else user_id  # 若未查到则退而显示 user_id
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("错误", f"获取用户名失败：{e}")
            user_name = user_id

        tk.Label(dash, text=f"欢迎，{user_name}", font=("微软雅黑", 20, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=30)

        btn_frame = tk.Frame(dash, bg=BG_COLOR)
        btn_frame.pack(pady=80)

        styled_button(btn_frame, "查询图书", lambda: open_user_book_view(user_id)).pack(pady=10)
        styled_button(btn_frame, "查询借阅记录", lambda: open_user_record_view(user_id)).pack(pady=10)
        styled_button(btn_frame, "退出登录", lambda: (dash.destroy(), main())).pack(pady=10)
    
        def open_user_book_view(user_id):
            dash.destroy()
            view_win = tk.Tk()
            view_win.title("查询图书")
            view_win.geometry("558x883")
            view_win.configure(bg=BG_COLOR)

            tk.Label(view_win, text="图书查询", font=("微软雅黑", 20, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

            form_frame = tk.Frame(view_win, bg=BG_COLOR)
            form_frame.pack(pady=10)

            # 左侧搜索栏
            input_frame = tk.Frame(form_frame, bg=BG_COLOR)
            input_frame.pack(side="left", padx=20)

            search_var = tk.StringVar()
            tk.Label(input_frame, text="搜索：", font=("微软雅黑", 12), bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, pady=5, padx=5)
            tk.Entry(input_frame, textvariable=search_var, width=30, font=("微软雅黑", 12)).grid(row=0, column=1, pady=5, padx=5)

            # 右侧按钮
            button_frame = tk.Frame(form_frame, bg=BG_COLOR)
            button_frame.pack(side="left", padx=20)

            styled_button(button_frame, "查询", lambda: update_table()).pack(pady=5)
            styled_button(button_frame, "借阅", lambda: borrow_selected_book()).pack(pady=5)
            styled_button(button_frame, "返回上级", lambda: go_back()).pack(pady=5)

            # 表格区域
            columns = ["编号", "标题", "作者", "出版社", "ISBN", "总数目", "可借阅数目"]
            tree = ttk.Treeview(view_win, columns=columns, show="headings", height=15)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=80)

            tree.pack(pady=20)

            def update_table():
                tree.delete(*tree.get_children())
                keyword = search_var.get()
                try:
                    conn = psycopg2.connect(
                        host="localhost",
                        port=8888,
                        database="mydb",
                        user="dbuser",
                        password="Test@123"
                    )
                except Exception as e:
                    messagebox.showerror("数据库连接失败", f"错误信息：{e}")
                    return
                cur = conn.cursor()
                sql = """
                    SELECT * FROM book_k
                    WHERE BookID ILIKE %s OR Title ILIKE %s OR Author ILIKE %s OR Publisher ILIKE %s OR ISBN ILIKE %s
                """
                params = tuple([f"%{keyword}%"] * 5)
                cur.execute(sql, params)
                for row in cur.fetchall():
                    tree.insert("", "end", values=row)
                cur.close()

            def borrow_selected_book():
                selected = tree.focus()
                if not selected:
                    messagebox.showwarning("提示", "请先选择一本图书")
                    return
                book_data = tree.item(selected)["values"]
                book_id, available = book_data[0], int(book_data[-1])

                if available <= 0:
                    messagebox.showwarning("提示", "当前图书已无可借阅数量")
                    return

                try:
                    try:
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="mydb",
                            user="dbuser",
                            password="Test@123"
                        )
                    except Exception as e:
                        messagebox.showerror("数据库连接失败", f"错误信息：{e}")
                        return
                    cur = conn.cursor()
                    # 插入借阅记录
                    today = datetime.date.today()
                    due = today + datetime.timedelta(days=60)
                    record_id = str(uuid.uuid4())[:8]

                    # 插入借阅记录表
                    cur.execute("""
                        INSERT INTO record_k (recordid, userid, bookid, borrowdate, duedate)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (record_id, user_id, book_id, today, due))

                    # 更新图书库存
                    cur.execute("""
                        UPDATE book_k SET AvailableCopies = AvailableCopies - 1 WHERE BookID = %s
                    """, (book_id,))

                    conn.commit()
                    cur.close()
                    conn.close()
                    update_table()
                    messagebox.showinfo("成功", f"成功借阅《{book_data[1].strip()}》，请于{due}前归还")
                except Exception as e:
                    messagebox.showerror("错误", f"借阅失败：{e}")

            def go_back():
                view_win.destroy()
                open_user_dashboard(user_id)

            update_table()
        
        def open_user_record_view(user_id):
            dash.destroy()
            record_win = tk.Tk()
            record_win.title("借阅记录查询")
            record_win.geometry("558x883")
            record_win.configure(bg=BG_COLOR)

            # ---------- 标题 ----------
            tk.Label(record_win, text="借阅记录", font=("微软雅黑", 20, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

            # ---------- 搜索框和按钮区域 ----------
            form_frame = tk.Frame(record_win, bg=BG_COLOR)
            form_frame.pack(pady=10)

            # 左侧搜索框
            input_frame = tk.Frame(form_frame, bg=BG_COLOR)
            input_frame.pack(side="left", padx=20)

            tk.Label(input_frame, text="搜索：", font=("微软雅黑", 12), bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, pady=5, padx=5)
            search_var = tk.StringVar()
            tk.Entry(input_frame, textvariable=search_var, width=25, font=("微软雅黑", 12)).grid(row=0, column=1, pady=5, padx=5)

            # 右侧按钮区域
            button_frame = tk.Frame(form_frame, bg=BG_COLOR)
            button_frame.pack(side="left", padx=20)

            styled_button(button_frame, "查询", lambda: update_table(search_var.get())).pack(pady=5)
            styled_button(button_frame, "归还", lambda: return_book()).pack(pady=5)
            styled_button(button_frame, "返回上级", lambda: (record_win.destroy(), open_user_dashboard(user_id))).pack(pady=5)

            # ---------- 表格 ----------
            columns = ["编号", "借阅人", "借阅图书", "借阅日期", "应归还日期", "归还日期"]
            tree = ttk.Treeview(record_win, columns=columns, show="headings", height=15)
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=90)

            tree.pack(pady=20)

            # 行颜色样式
            style = ttk.Style()
            style.configure("Treeview", rowheight=30)
            style.map("Treeview", background=[("selected", "#3399FF")])

            # ---------- 归还图书 ----------
            def return_book():
                selected = tree.focus()
                if not selected:
                    messagebox.showwarning("提示", "请选择要归还的记录")
                    return
                values = tree.item(selected)["values"]
                record_id = values[0]
                return_date = datetime.date.today()
                try:
                    conn = psycopg2.connect(
                    host="localhost",
                    port=8888,
                    database="mydb",
                    user="dbuser",
                    password="Test@123"
                    )
                    cur = conn.cursor()
                    # 先检查是否已归还
                    cur.execute("SELECT ReturnDate, BookID FROM record_k WHERE RecordID = %s", (record_id,))
                    result = cur.fetchone()
                    if result is None:
                        messagebox.showerror("错误", "记录不存在")
                        cur.close()
                        return
                    if result[0] is not None:
                        messagebox.showinfo("提示", "该记录已归还，不能重复归还！")
                        cur.close()
                        return
                    
                    book_id = result[1]

                    # 更新归还日期
                    cur.execute("UPDATE record_k SET ReturnDate = %s WHERE RecordID = %s", (return_date, record_id))

                    # 更新书籍库存 +1
                    cur.execute("UPDATE book_k SET AvailableCopies = AvailableCopies + 1 WHERE BookID = %s", (book_id,))

                    conn.commit()
                    cur.close()
                    update_table(search_var.get())
                    messagebox.showinfo("成功", "归还成功，库存已更新！")
                except Exception as e:
                    messagebox.showerror("错误", f"归还失败：{e}")
            # ---------- 数据更新 ----------
            def update_table(keyword=""):
                tree.delete(*tree.get_children())
                conn = psycopg2.connect(
                        host="localhost",
                        port=8888,
                        database="mydb",
                        user="dbuser",
                        password="Test@123"
                    )
                cur = conn.cursor()
                like_keyword = f"%{keyword}%"
                cur.execute("""
                    SELECT r.RecordID, u.UserName, b.Title, r.BorrowDate, r.DueDate, r.ReturnDate
                    FROM record_k r
                    JOIN user_k u ON r.UserID = u.UserID
                    JOIN book_k b ON r.BookID = b.BookID
                    WHERE r.UserID = %s AND (
                        r.RecordID ILIKE %s OR u.UserName ILIKE %s OR b.Title ILIKE %s OR
                        CAST(r.BorrowDate AS TEXT) ILIKE %s OR
                        CAST(r.DueDate AS TEXT) ILIKE %s OR
                        CAST(r.ReturnDate AS TEXT) ILIKE %s
                    )
                """, (user_id, like_keyword, like_keyword, like_keyword, like_keyword, like_keyword, like_keyword))
                for row in cur.fetchall():
                    tag = ""
                    if row[5] is not None:  # 已归还
                        tag = "returned"
                    tree.insert("", "end", values=row, tags=(tag,))
                cur.close()

            # 样式：归还记录标绿
            tree.tag_configure("returned", background="#d0f0c0")

            # ---------- Treeview 联动 ----------
            def on_tree_select(event):
                selected = tree.focus()
                if not selected:
                    return
                # 可以在此实现选中行为，比如自动填写表单（如有）

            tree.bind("<<TreeviewSelect>>", on_tree_select)

            update_table()

            record_win.mainloop()

    # 登录行为u
    def login_action():
        global user_id
        user_id = entry_user_id.get()
        user_pwd = entry_user_pwd.get()
        try:
            conn = psycopg2.connect(
                host="localhost",
                port=8888,
                database="mydb",
                user="dbuser",
                password="Test@123"
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM user_login_k WHERE user_id=%s AND user_pass=%s", (user_id, user_pwd))
            result = cur.fetchone()
            if result:
                login_win.destroy()
                open_user_dashboard(user_id)
            else:
                messagebox.showerror("登录失败", "账号或密码错误")
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("数据库错误", str(e))

    # 返回主界面
    def back_to_home():
        login_win.destroy()
        main()

    # 按钮底部对齐
    btn_frame = tk.Frame(login_win, bg=BG_COLOR)
    btn_frame.pack(pady=100)

    styled_button(btn_frame, "登录", login_action).pack(pady=10)
    styled_button(btn_frame, "返回首页", back_to_home).pack(pady=10)

    login_win.mainloop()

# ========= 主界面 =========
def main():
    parent_window = tk.Tk()
    parent_window.title("图书馆管理系统")
    parent_window.geometry("558x883")
    parent_window.resizable(False, False)
    parent_window.configure(bg=BG_COLOR)

    # 空白Frame用于整体下移
    tk.Frame(parent_window, height=150, bg=BG_COLOR).pack()

    # 标题
    title = tk.Label(
        parent_window,
        text="欢迎使用图书馆管理系统",
        font=("微软雅黑", 24, "bold"),
        pady=20,
        fg=TITLE_COLOR,
        bg=BG_COLOR
    )
    title.pack()

    # 按钮区
    button_frame = tk.Frame(parent_window, bg=BG_COLOR)
    button_frame.pack(pady=30)

    styled_button(button_frame, "管理员登录", lambda: open_admin_login(parent_window)).pack(pady=10)
    styled_button(button_frame, "用户登录", lambda: open_user_login(parent_window)).pack(pady=10)
    styled_button(button_frame, "关于", lambda: messagebox.showinfo("关于", "本系统由2023级赵炳杰开发。")).pack(pady=10)
    styled_button(button_frame, "退出系统", lambda: parent_window.destroy()).pack(pady=10)

    # 图片展示
    try:
        image = Image.open("logo.jpg")  # 请使用你本地的图片路径
        image = image.resize((450, 180))
        photo = ImageTk.PhotoImage(image)
        img_label = tk.Label(parent_window, image=photo, bg=BG_COLOR)
        img_label.image = photo
        img_label.pack(pady=30)
    except Exception as e:
        img_label = tk.Label(parent_window, text="（图片加载失败）", fg="gray", bg=BG_COLOR)
        img_label.pack(pady=30)

    parent_window.mainloop()

# 启动程序
main()
