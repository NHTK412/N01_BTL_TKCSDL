# main.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Menu
from data_structures.functional_dependency import FD
import copy
from itertools import combinations
from util.util import util

class ProjectionFrame(tk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.fd_set = []
        self.all_attributes = set()
        self.r1_attributes = set()
        self.projection_result = []
       
        self.create_widgets()
        
   
    def create_widgets(self):
        """Tạo các widget"""
        # Header Frame
        header_frame = tk.Frame(self, bg='#2c3e50', height=80)
        header_frame.grid(row=0, 
                          column=0, 
                          columnspan=2, 
                          sticky="ew", 
                          padx=10, 
                          pady=(10, 0))
        
        header_frame.grid_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🔍 TÍNH PROJECTION CỦA TẬP PHỤ THUỘC HÀM: F1 = πR1(F)",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        # Content Frame
        content_frame = tk.Frame(self, bg='#f0f0f0')
        content_frame.grid(row=1, 
                           column=0, 
                           columnspan=2, 
                           sticky="nsew", 
                           padx=10, 
                           pady=10)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(1, weight=1)
        
        # Control Panel
        control_frame = tk.Frame(content_frame, bg='#f0f0f0', height=120)
        control_frame.grid(row=0, 
                           column=0, 
                           columnspan=2, 
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
        
        # Frame cho file input (hàng đầu)
        top_control_frame = tk.Frame(control_frame, bg='#f0f0f0')
        top_control_frame.pack(fill='x', pady=5)
        
        file_frame = tk.Frame(top_control_frame, bg='#f0f0f0')
        file_frame.pack(side=tk.LEFT, padx=20)
        
        self.open_button = ttk.Button(
            file_frame,
            text="📂 Chọn File Tập FD",
            style='Custom.TButton',
            command=self.open_file
        )
        self.open_button.pack(pady=(0, 5))
        
        self.file_label = tk.Label(
            file_frame,
            text="Chưa chọn file",
            font=('Arial', 9),
            fg='#7f8c8d',
            bg='#f0f0f0'
        )
        self.file_label.pack()
        
        # Label thông tin R (tập thuộc tính toàn bộ)
        self.r_label = tk.Label(
            top_control_frame,
            text="R = { }",
            font=('Arial', 11, 'bold'),
            fg='#e74c3c',
            bg='#f0f0f0'
        )
        self.r_label.pack(side=tk.RIGHT, padx=20)
        
        # Frame cho R1 input và button (hàng thứ hai)
        bottom_control_frame = tk.Frame(control_frame, bg='#f0f0f0')
        bottom_control_frame.pack(fill='x', pady=5)
        
        # R1 input frame
        r1_frame = tk.Frame(bottom_control_frame, bg='#f0f0f0')
        r1_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(r1_frame, text="Nhập R1 (tập thuộc tính con):", 
                font=('Arial', 10, 'bold'), bg='#f0f0f0').pack(anchor='w')
        
        self.r1_entry = tk.Entry(
            r1_frame,
            font=('Arial', 11),
            width=20,
            relief=tk.FLAT,
            bd=1
        )
        self.r1_entry.pack(pady=(2, 0))
        self.r1_entry.insert(0, "Ví dụ: ABC")
        self.r1_entry.bind('<FocusIn>', self.clear_placeholder)
        
        # Button tính projection (ở giữa)
        self.calc_button = ttk.Button(
            bottom_control_frame,
            text="🔍 Tính Projection πR1(F)",
            style='Custom.TButton',
            command=self.calculate_projection,
            state='disabled'
        )
        self.calc_button.pack(expand=True)
        
        # Label thống kê
        self.stats_label = tk.Label(
            bottom_control_frame,
            text="",
            font=('Arial', 10, 'bold'),
            fg='#27ae60',
            bg='#f0f0f0'
        )
        self.stats_label.pack(side=tk.RIGHT, padx=20)
        
        # Left Panel - Tập FD gốc
        left_frame = tk.LabelFrame(
            content_frame,
            text="📝 Tập Phụ Thuộc Hàm Gốc F",
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
        
        # Text area cho tập FD gốc
        self.fd_text = tk.Text(
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
        self.fd_text.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar cho fd
        fd_scroll = ttk.Scrollbar(left_frame, command=self.fd_text.yview)
        fd_scroll.grid(row=0, column=1, sticky="ns")
        self.fd_text.config(yscrollcommand=fd_scroll.set)
        
        # Right Panel - Kết quả projection
        right_frame = tk.LabelFrame(
            content_frame,
            text="🔍 Kết Quả Projection F1 = πR1(F) và Các Bước Thực Hiện",
            font=('Arial', 11, 'bold'),
            fg='#34495e',
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 0))
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
        
    def clear_placeholder(self, event):
        """Xóa placeholder khi focus vào entry"""
        if self.r1_entry.get() == "Ví dụ: ABC":
            self.r1_entry.delete(0, tk.END)
            
    def open_file(self):
        """Mở và đọc file"""
        file_path = filedialog.askopenfilename(
            title="Chọn file tập phụ thuộc hàm",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            filename = file_path.split('/')[-1]
            
            # Xóa nội dung cũ
            self.file_label.config(text=f"📄 {filename}", fg='#2c3e50')
            self.fd_text.config(state=tk.NORMAL)
            self.fd_text.delete(1.0, tk.END)
            self.fd_set.clear()
            self.all_attributes.clear()
            
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
                    self.fd_set.append(fd)
                    fd_count += 1
                    self.fd_text.insert(tk.END, f"FD{fd_count}: {fd}\n")
                    
                    # Thu thập tất cả thuộc tính
                    self.all_attributes.update(fd.getLhs())
                    self.all_attributes.update(fd.getRhs())

            self.fd_text.config(state=tk.DISABLED)
            
            # Cập nhật hiển thị R
            self.r_label.config(text=f"R = {{{', '.join(sorted(self.all_attributes))}}}")
            
            # Cập nhật trạng thái button
            if self.fd_set:
                self.calc_button.config(state='normal')
            
            # Cập nhật thống kê
            self.update_stats()
            
            messagebox.showinfo("Thành công", f"Đã đọc {fd_count} phụ thuộc hàm!\nTập thuộc tính R: {{{', '.join(sorted(self.all_attributes))}}}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
            
    # def parse_fd_line(self, line):
        # """Phân tích một dòng phụ thuộc hàm"""
        # # Xử lý dấu mũi tên khác nhau
        # arrow_symbols = ['->', '→', '-->', '－＞']
        
        # for arrow in arrow_symbols:
        #     if arrow in line:
        #         parts = line.split(arrow)
        #         break
        # else:
        #     # Nếu không tìm thấy mũi tên, thử tìm dấu '-'
        #     if '-' in line:
        #         tokens = line.split()
        #         if '-' in tokens:
        #             arrow_index = tokens.index('-')
        #             left_tokens = tokens[:arrow_index]
        #             right_tokens = tokens[arrow_index + 1:]
                    
        #             left_side = set([attr.strip() for token in left_tokens for attr in token if attr.isalnum()])
        #             right_side = set([attr.strip() for token in right_tokens for attr in token if attr.isalnum()])
        #         else:
        #             return None
        #     else:
        #         return None
        
        # # Nếu đã tìm thấy mũi tên
        # if 'parts' in locals() and len(parts) == 2:
        #     left_part = parts[0].strip()
        #     right_part = parts[1].strip()
            
        #     # Trích xuất các thuộc tính từ chuỗi
        #     left_side = set([attr for attr in left_part if attr.isalnum()])
        #     right_side = set([attr for attr in right_part if attr.isalnum()])
        
        # if left_side and right_side:
        #     try:
        #         # Tạo đối tượng FD
        #         fd = FD(lhs=left_side, rhs=right_side)
        #         return fd
        #     except Exception as e:
        #         return None
        
        # return None
    
    def update_stats(self):
        """Cập nhật thống kê"""
        stats_text = f"FD gốc: {len(self.fd_set)}"
        if self.projection_result:
            stats_text += f" | Projection: {len(self.projection_result)}"
        self.stats_label.config(text=stats_text)
    
    def calculate_projection(self):
        """Tính projection theo thuật toán πR1(F)"""
        if not self.fd_set:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file trước!")
            return
        
        # Lấy R1 từ input
        r1_input = self.r1_entry.get().strip().upper()
        if not r1_input or r1_input == "VÍ DỤ: ABC":
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tập thuộc tính R1!")
            return
        
        # Parse R1
        self.r1_attributes = {attr for attr in r1_input if attr.isalnum()}
        
        if not self.r1_attributes:
            messagebox.showwarning("Cảnh báo", "Tập R1 không hợp lệ!")
            return
        
        # Kiểm tra R1 có phải tập con của R không
        if not self.r1_attributes.issubset(self.all_attributes):
            invalid_attrs = self.r1_attributes - self.all_attributes
            messagebox.showwarning("Cảnh báo", f"R1 chứa thuộc tính không có trong R: {', '.join(invalid_attrs)}")
            return
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        self.result_text.insert(tk.END, "TÍNH PROJECTION CỦA TẬP PHỤ THUỘC HÀM\n")
        self.result_text.insert(tk.END, "F1 = πR1(F)\n")
        self.result_text.insert(tk.END, "=" * 60 + "\n\n")
        
        self.result_text.insert(tk.END, f"R = {{{', '.join(sorted(self.all_attributes))}}}\n")
        self.result_text.insert(tk.END, f"R1 = {{{', '.join(sorted(self.r1_attributes))}}}\n")
        self.result_text.insert(tk.END, f"F = {{{', '.join(str(fd) for fd in self.fd_set)}}}\n\n")
        
        # Bước 1: Khởi tạo F1 = ∅
        self.result_text.insert(tk.END, "BƯỚC 1: Khởi tạo F1 = ∅\n")
        self.result_text.insert(tk.END, "-" * 60 + "\n\n")
        
        f1 = []
        
        # Bước 2: Với mọi X ⊆ R1
        self.result_text.insert(tk.END, "BƯỚC 2: Với mọi X ⊆ R1, tính X⁺ và kiểm tra điều kiện\n")
        self.result_text.insert(tk.END, "-" * 60 + "\n")
        
        # Tạo tất cả tập con của R1 (trừ tập rỗng)
        all_subsets = []
        for i in range(1, len(self.r1_attributes) + 1):
            for subset in combinations(self.r1_attributes, i):
                all_subsets.append(set(subset))
        
        step_count = 0
        for x_set in all_subsets:
            step_count += 1
            x_str = ''.join(sorted(x_set))
            
            # Tính X⁺ theo F
            closure = self.compute_closure(x_set, self.fd_set)
            closure_str = ''.join(sorted(closure))
            
            # Tính X⁺ ∩ R1
            intersection = closure.intersection(self.r1_attributes)
            intersection_str = ''.join(sorted(intersection))
            
            self.result_text.insert(tk.END, f"Bước 2.{step_count}: X = {{{x_str}}}\n")
            self.result_text.insert(tk.END, f"  X⁺ = {{{closure_str}}}\n")
            self.result_text.insert(tk.END, f"  X⁺ ∩ R1 = {{{intersection_str}}}\n")
            
            # Kiểm tra điều kiện: X⁺ ∩ R1 ≠ X
            if intersection != x_set and intersection:
                # Thêm FD: X → (X⁺ ∩ R1)
                new_rhs = intersection - x_set  # Loại bỏ các thuộc tính đã có trong X
                if new_rhs:  # Chỉ thêm nếu có thuộc tính mới
                    new_fd = FD(lhs=x_set.copy(), rhs=new_rhs)
                    f1.append(new_fd)
                    self.result_text.insert(tk.END, f"  ✅ Thêm FD: {new_fd}\n")
                else:
                    self.result_text.insert(tk.END, f"  ⏭️ Không thêm (không có thuộc tính mới)\n")
            else:
                if not intersection:
                    self.result_text.insert(tk.END, f"  ❌ Không thêm (X⁺ ∩ R1 = ∅)\n")
                else:
                    self.result_text.insert(tk.END, f"  ❌ Không thêm (X⁺ ∩ R1 = X)\n")
            
            self.result_text.insert(tk.END, "\n")
        
        self.result_text.insert(tk.END, f"Sau bước 2: F1 = {{{', '.join(str(fd) for fd in f1)}}}\n")
        self.result_text.insert(tk.END, f"Số lượng FD trong F1: {len(f1)}\n\n")
        
        # Bước 3: Tính minimal cover của F1
        self.result_text.insert(tk.END, "BƯỚC 3: Tính minimal cover của F1\n")
        self.result_text.insert(tk.END, "-" * 60 + "\n")
        
        if not f1:
            self.result_text.insert(tk.END, "F1 = ∅, không cần tính minimal cover.\n\n")
            self.projection_result = []
        else:
            minimal_cover = self.compute_minimal_cover(f1)
            self.projection_result = minimal_cover
            
            self.result_text.insert(tk.END, f"Minimal cover của F1: {{{', '.join(str(fd) for fd in minimal_cover)}}}\n")
            self.result_text.insert(tk.END, f"Số lượng FD sau minimal cover: {len(minimal_cover)}\n\n")
        
        # Kết quả cuối cùng
        self.result_text.insert(tk.END, "KẾT QUẢ CUỐI CÙNG\n")
        self.result_text.insert(tk.END, "=" * 60 + "\n")
        
        if self.projection_result:
            self.result_text.insert(tk.END, f"F1 = πR1(F) = {{{', '.join(str(fd) for fd in self.projection_result)}}}\n\n")
            
            for i, fd in enumerate(self.projection_result, 1):
                self.result_text.insert(tk.END, f"FD{i}: {fd}\n")
        else:
            self.result_text.insert(tk.END, "F1 = πR1(F) = ∅\n")
            self.result_text.insert(tk.END, "Tập R1 không có phụ thuộc hàm nào được suy diễn từ F.\n")
        
        self.result_text.config(state=tk.DISABLED)
        
        # Cập nhật thống kê
        self.update_stats()
    
    def compute_closure(self, attributes, fd_set):
        """Tính toán bao đóng của một tập thuộc tính"""
        closure = attributes.copy()
        changed = True
        
        while changed:
            changed = False
            
            for fd in fd_set:
                # Kiểm tra nếu LHS của FD nằm trong closure hiện tại
                if fd.getLhs().issubset(closure):
                    # Thêm RHS vào closure
                    before_size = len(closure)
                    closure = closure.union(fd.getRhs())
                    
                    # Nếu có thuộc tính mới được thêm vào
                    if len(closure) > before_size:
                        changed = True
        
        return closure
    
    def compute_minimal_cover(self, fd_set):
        """Tính minimal cover của một tập FD"""
        if not fd_set:
            return []
        
        # Sao chép tập FD
        current_fds = copy.deepcopy(fd_set)
        
        # Bước 1: Phân rã vế phải thành một thuộc tính
        step1_fds = []
        for fd in current_fds:
            lhs = fd.getLhs()
            rhs = fd.getRhs()
            
            if len(rhs) > 1:
                # Phân rã thành nhiều FD với vế phải là một thuộc tính
                for attr in rhs:
                    new_fd = FD(lhs=lhs.copy(), rhs={attr})
                    step1_fds.append(new_fd)
            else:
                step1_fds.append(fd)
        
        current_fds = step1_fds
        
        # Bước 2: Loại bỏ các FD thừa
        i = 0
        while i < len(current_fds):
            fd_to_test = current_fds[i]
            remaining_fds = current_fds[:i] + current_fds[i+1:]
            
            # Kiểm tra xem fd_to_test có thể suy diễn từ remaining_fds không
            if self.is_fd_implied_by_set(fd_to_test, remaining_fds):
                current_fds.pop(i)
            else:
                i += 1
        
        # Bước 3: Rút gọn vế trái
        for i, fd in enumerate(current_fds):
            lhs = fd.getLhs()
            rhs = fd.getRhs()
            
            if len(lhs) <= 1:
                continue
                
            # Thử loại bỏ từng thuộc tính từ vế trái
            for attr in lhs.copy():
                reduced_lhs = lhs - {attr}
                if not reduced_lhs:
                    continue
                    
                # Tạo FD mới với vế trái rút gọn
                new_fd = FD(lhs=reduced_lhs, rhs=rhs.copy())
                
                # Tạo tập FD thử nghiệm
                test_fds = current_fds[:i] + [new_fd] + current_fds[i+1:]
                
                # Kiểm tra tương đương
                if self.are_fd_sets_equivalent(current_fds, test_fds):
                    current_fds[i] = new_fd
                    break
        
        return current_fds
    
    def is_fd_implied_by_set(self, fd, fd_set):
        """Kiểm tra xem một FD có thể suy diễn từ một tập FD không"""
        lhs = fd.getLhs()
        rhs = fd.getRhs()
        
        # Tính bao đóng của LHS sử dụng fd_set
        closure = self.compute_closure(lhs, fd_set)
        
        # Kiểm tra xem RHS có nằm trong bao đóng không
        return rhs.issubset(closure)
    
    def are_fd_sets_equivalent(self, set1, set2):
        """Kiểm tra tương đương giữa hai tập FD"""
        # Kiểm tra set1 ⊢ set2
        for fd in set2:
            if not self.is_fd_implied_by_set(fd, set1):
                return False
        
        # Kiểm tra set2 ⊢ set1
        for fd in set1:
            if not self.is_fd_implied_by_set(fd, set2):
                return False
        
        return True
    
