# main.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Menu
from data_structures.functional_dependency import FD
from util.util import util

import os

class FDReader(tk.Frame):
   
    
    def __init__(self, parent):
        super().__init__(parent)
        self.fd_set1 = []
        self.fd_set2 = []
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_widgets()
        
   
    def create_widgets(self):
        """Tạo các widget"""
        # Header Frame
        header_frame = tk.Frame(self, bg='#2c3e50', height=80)
        header_frame.grid(row=0, 
                          column=0, 
                          columnspan=3, 
                          sticky="ew", 
                          padx=10, 
                          pady=(10, 0))
        
        header_frame.grid_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🔍 KIỂM TRA TƯƠNG ĐƯƠNG HAI TẬP PHỤ THUỘC HÀM",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        # Content Frame
        content_frame = tk.Frame(self, bg='#f0f0f0')
        content_frame.grid(row=1, 
                           column=0, 
                           columnspan=3, 
                           sticky="nsew", 
                           padx=10, 
                           pady=10)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.columnconfigure(2, weight=1)
        content_frame.rowconfigure(1, weight=1)
        
        # Control Panel
        control_frame = tk.Frame(content_frame, bg='#f0f0f0', height=100)
        control_frame.grid(row=0, 
                           column=0, 
                           columnspan=3, 
                           sticky="ew", 
                           pady=(0, 10))
        control_frame.grid_propagate(False)
        
        # Style cho button
        style = ttk.Style()
        style.configure(
            'Custom.TButton',
            font=('Arial', 11, 'bold'),
            padding=(15, 8)
        )
        
        # Frame cho file 1
        file1_frame = tk.Frame(control_frame, bg='#f0f0f0')
        file1_frame.pack(side=tk.LEFT, padx=20, pady=10, fill='y')
        
        self.open_button1 = ttk.Button(
            file1_frame,
            text="📂 Chọn File Tập 1",
            style='Custom.TButton',
            command=lambda: self.open_file(1)
        )
        self.open_button1.pack(pady=(0, 5))
        
        self.file_label1 = tk.Label(
            file1_frame,
            text="Chưa chọn file tập 1",
            font=('Arial', 9),
            fg='#7f8c8d',
            bg='#f0f0f0'
        )
        self.file_label1.pack()
        
        # Frame cho file 2
        file2_frame = tk.Frame(control_frame, bg='#f0f0f0')
        file2_frame.pack(side=tk.LEFT, padx=20, pady=10, fill='y')
        
        self.open_button2 = ttk.Button(
            file2_frame,
            text="📂 Chọn File Tập 2",
            style='Custom.TButton',
            command=lambda: self.open_file(2)
        )
        self.open_button2.pack(pady=(0, 5))
        
        self.file_label2 = tk.Label(
            file2_frame,
            text="Chưa chọn file tập 2",
            font=('Arial', 9),
            fg='#7f8c8d',
            bg='#f0f0f0'
        )
        self.file_label2.pack()
        
        # Button kiểm tra tương đương (đặt ở giữa)
        check_frame = tk.Frame(control_frame, bg='#f0f0f0')
        check_frame.pack(expand=True, fill='both')
        
        self.check_equiv_button = ttk.Button(
            check_frame,
            text="🔍 Kiểm Tra Tương Đương",
            style='Custom.TButton',
            command=self.check_equivalence,
            state='disabled'
        )
        self.check_equiv_button.pack(expand=True, pady=20)
        
        # Label thống kê
        self.stats_label = tk.Label(
            control_frame,
            text="",
            font=('Arial', 10, 'bold'),
            fg='#27ae60',
            bg='#f0f0f0'
        )
        self.stats_label.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Left Panel - Tập FD 1
        left_frame = tk.LabelFrame(
            content_frame,
            text="📝 Tập Phụ Thuộc Hàm 1",
            font=('Arial', 11, 'bold'),
            fg='#34495e',
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        left_frame.grid(row=1, 
                        column=0, 
                        sticky="nsew", 
                        padx=(0, 5))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        
        # Text area cho tập FD 1
        self.fd1_text = tk.Text(
            left_frame,
            font=('Consolas', 10),
            wrap=tk.WORD,
            bg='#f8f9fa',
            relief=tk.FLAT,
            bd=1,
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.fd1_text.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar cho fd1
        fd1_scroll = ttk.Scrollbar(left_frame, command=self.fd1_text.yview)
        fd1_scroll.grid(row=0, column=1, sticky="ns")
        self.fd1_text.config(yscrollcommand=fd1_scroll.set)
        
        # Middle Panel - Tập FD 2
        middle_frame = tk.LabelFrame(
            content_frame,
            text="📝 Tập Phụ Thuộc Hàm 2",
            font=('Arial', 11, 'bold'),
            fg='#34495e',
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        middle_frame.grid(row=1, column=1, sticky="nsew", padx=(2.5, 2.5))
        middle_frame.columnconfigure(0, weight=1)
        middle_frame.rowconfigure(0, weight=1)
        
        # Text area cho tập FD 2
        self.fd2_text = tk.Text(
            middle_frame,
            font=('Consolas', 10),
            wrap=tk.WORD,
            bg='#f8f9fa',
            relief=tk.FLAT,
            bd=1,
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.fd2_text.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar cho fd2
        fd2_scroll = ttk.Scrollbar(middle_frame, command=self.fd2_text.yview)
        fd2_scroll.grid(row=0, column=1, sticky="ns")
        self.fd2_text.config(yscrollcommand=fd2_scroll.set)
        
        # Right Panel - Kết quả kiểm tra
        right_frame = tk.LabelFrame(
            content_frame,
            text="🔍 Kết Quả Kiểm Tra Tương Đương",
            font=('Arial', 11, 'bold'),
            fg='#34495e',
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        right_frame.grid(row=1, column=2, sticky="nsew", padx=(5, 0))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        
        # Text area cho kết quả
        self.result_text = tk.Text(
            right_frame,
            font=('Consolas', 10),
            wrap=tk.WORD,
            bg='#e8f5e8',
            relief=tk.FLAT,
            bd=1,
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.result_text.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar cho result
        result_scroll = ttk.Scrollbar(right_frame, command=self.result_text.yview)
        result_scroll.grid(row=0, column=1, sticky="ns")
        self.result_text.config(yscrollcommand=result_scroll.set)
        
    def open_file(self, file_number):
        """Mở và đọc file"""
        file_path = filedialog.askopenfilename(
            title=f"Chọn file tập phụ thuộc hàm {file_number}",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            filename = file_path.split('/')[-1]
            
            # Xóa nội dung cũ
            if file_number == 1:
                self.file_label1.config(text=f"📄 {filename}", fg='#2c3e50')
                self.fd1_text.config(state=tk.NORMAL)
                self.fd1_text.delete(1.0, tk.END)
                self.fd_set1.clear()
                fd_list = self.fd_set1
                text_widget = self.fd1_text
            else:
                self.file_label2.config(text=f"📄 {filename}", fg='#2c3e50')
                self.fd2_text.config(state=tk.NORMAL)
                self.fd2_text.delete(1.0, tk.END)
                self.fd_set2.clear()
                fd_list = self.fd_set2
                text_widget = self.fd2_text
            
            # Đọc file
            with open(file_path, 'r', encoding='utf-8') as file:
                file_data = file.read()
            
            file_data = file_data.split('\n')
            fd_count = 0

            for line in file_data:
                line = line.strip()
                if not line:
                    continue
                
                # Phân tích phụ thuộc hàm
                fd = util.parse_fd_line(line)
                if fd:
                    fd_list.append(fd)
                    fd_count += 1
                    text_widget.insert(tk.END, f"FD{fd_count}: {fd}\n")

            text_widget.config(state=tk.DISABLED)
            
            # Cập nhật trạng thái button
            if self.fd_set1 and self.fd_set2:
                self.check_equiv_button.config(state='normal')
            
            # Cập nhật thống kê
            self.update_stats()
            
            messagebox.showinfo("Thành công", f"Đã đọc {fd_count} phụ thuộc hàm từ tập {file_number}!")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
            
    
    
    def update_stats(self):
        """Cập nhật thống kê"""
        stats_text = f"Tập 1: {len(self.fd_set1)} FD"
        if self.fd_set2:
            stats_text += f" | Tập 2: {len(self.fd_set2)} FD"
        self.stats_label.config(text=stats_text)
    
    def check_equivalence(self):
        """Kiểm tra tương đương hai tập FD"""
        if not self.fd_set1 or not self.fd_set2:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cả hai file trước!")
            return
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        self.result_text.insert(tk.END, "KIỂM TRA TƯƠNG ĐƯƠNG HAI TẬP PHỤ THUỘC HÀM\n")
        self.result_text.insert(tk.END, "=" * 46 + "\n\n")
        
        # Bước 1: Kiểm tra F1 ⊢ F2
        self.result_text.insert(tk.END, "BƯỚC 1: Kiểm tra Tập 1 có suy diễn ra Tập 2 không?\n")
        self.result_text.insert(tk.END, "-" * 46 + "\n")
        
        f1_implies_f2, f1_f2_details = self.check_implication(self.fd_set1, self.fd_set2, "Tập 1", "Tập 2")
        
        self.result_text.insert(tk.END, f1_f2_details)
        self.result_text.insert(tk.END, f"\nKết quả Bước 1: {'✅ Tập 1 suy diễn ra Tập 2' if f1_implies_f2 else '❌ Tập 1 KHÔNG suy diễn ra Tập 2'}\n\n")
        
        # Bước 2: Kiểm tra F2 ⊢ F1
        self.result_text.insert(tk.END, "BƯỚC 2: Kiểm tra Tập 2 có suy diễn ra Tập 1 không?\n")
        self.result_text.insert(tk.END, "-" * 46 + "\n")
        
        f2_implies_f1, f2_f1_details = self.check_implication(self.fd_set2, self.fd_set1, "Tập 2", "Tập 1")
        
        self.result_text.insert(tk.END, f2_f1_details)
        self.result_text.insert(tk.END, f"\nKết quả Bước 2: {'✅ Tập 2 suy diễn ra Tập 1' if f2_implies_f1 else '❌ Tập 2 KHÔNG suy diễn ra Tập 1'}\n\n")
        
        # Bước 3: Kết luận
        self.result_text.insert(tk.END, "BƯỚC 3: KẾT LUẬN\n")
        self.result_text.insert(tk.END, "=" * 20 + "\n")
        
        if f1_implies_f2 and f2_implies_f1:
            self.result_text.insert(tk.END, "✅ HAI TẬP PHỤ THUỘC HÀM TƯƠNG ĐƯƠNG!\n")
            self.result_text.insert(tk.END, "Lý do: Tập 1 ⊢ Tập 2 VÀ Tập 2 ⊢ Tập 1\n")
        else:
            self.result_text.insert(tk.END, "❌ HAI TẬP PHỤ THUỘC HÀM KHÔNG TƯƠNG ĐƯƠNG!\n")
            if not f1_implies_f2 and not f2_implies_f1:
                self.result_text.insert(tk.END, "Lý do: Tập 1 không suy diễn ra Tập 2 VÀ Tập 2 không suy diễn ra Tập 1\n")
            elif not f1_implies_f2:
                self.result_text.insert(tk.END, "Lý do: Tập 1 không suy diễn ra Tập 2\n")
            else:
                self.result_text.insert(tk.END, "Lý do: Tập 2 không suy diễn ra Tập 1\n")
        
        self.result_text.config(state=tk.DISABLED)
    
    def check_implication(self, from_set, to_set, from_name, to_name):
        """Kiểm tra xem from_set có suy diễn ra to_set không"""
        details = ""
        all_implied = True
        failed_fds = []
        
        for i, fd in enumerate(to_set, 1):
            lhs = fd.getLhs()
            rhs = fd.getRhs()
            
            # Tính bao đóng của LHS sử dụng from_set
            closure, steps = self.compute_closure_with_set(lhs, from_set)
            
            # Kiểm tra xem RHS có nằm trong bao đóng không
            is_implied = rhs.issubset(closure)
            
            lhs_str = ''.join(sorted(lhs))
            rhs_str = ''.join(sorted(rhs))
            closure_str = ''.join(sorted(closure))
            
            details += f"Kiểm tra FD{i}: {lhs_str} → {rhs_str}\n"
            details += f"({lhs_str})⁺ theo {from_name} = {{{closure_str}}}\n"
            
            if is_implied:
                details += f"✅ {rhs_str} ⊆ {{{closure_str}}} → FD{i} được suy diễn\n\n"
            else:
                details += f"❌ {rhs_str} ⊄ {{{closure_str}}} → FD{i} KHÔNG được suy diễn\n\n"
                all_implied = False
                failed_fds.append(f"FD{i}")
        
        return all_implied, details
    
    def compute_closure_with_set(self, attributes, fd_set):
        """Tính toán bao đóng với tập FD cho trước"""
        closure = attributes.copy()
        steps = []
        changed = True
        
        while changed:
            changed = False
            applied_fds = []
            
            for fd in fd_set:
                # Kiểm tra nếu LHS của FD nằm trong closure hiện tại
                if fd.getLhs().issubset(closure):
                    # Thêm RHS vào closure
                    before_size = len(closure)
                    closure = closure.union(fd.getRhs())
                    
                    # Nếu có thuộc tính mới được thêm vào
                    if len(closure) > before_size:
                        applied_fds.append(fd)
                        changed = True
            
            # Lưu bước nếu có thay đổi
            if changed:
                steps.append((closure.copy(), applied_fds))
        
        return closure, steps
    
   