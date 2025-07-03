import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from data_structures.functional_dependency import FD
from itertools import combinations

class NormalFormCheckerFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.fd_set = []
        self.all_attributes = set()
        self.all_keys = []
        self.prime_attributes = set()
        self.non_prime_attributes = set()
        
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
            text="📊 XÁC ĐỊNH DẠNG CHUẨN CỦA QUAN HỆ",
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
        control_frame = tk.Frame(content_frame, bg='#f0f0f0', height=100)
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
        
        # Frame cho file input
        file_frame = tk.Frame(control_frame, bg='#f0f0f0')
        file_frame.pack(side=tk.LEFT, padx=20, pady=10, fill='y')
        
        self.open_button = ttk.Button(
            file_frame,
            text="📂 Chọn File Quan Hệ",
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
        
        # Button kiểm tra dạng chuẩn
        check_frame = tk.Frame(control_frame, bg='#f0f0f0')
        check_frame.pack(expand=True, fill='both')
        
        self.check_button = ttk.Button(
            check_frame,
            text="📊 Kiểm Tra Dạng Chuẩn",
            style='Custom.TButton',
            command=self.check_normal_forms,
            state='disabled'
        )
        self.check_button.pack(expand=True, pady=20)
        
        # Label thống kê
        self.stats_label = tk.Label(
            control_frame,
            text="",
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='#f0f0f0'
        )
        self.stats_label.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Left Panel - Thông tin cơ bản
        left_frame = tk.LabelFrame(
            content_frame,
            text="📝 Thông Tin Quan Hệ",
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
        
        # Text area cho thông tin cơ bản
        self.info_text = tk.Text(
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
        self.info_text.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar cho info
        info_scroll = ttk.Scrollbar(left_frame, command=self.info_text.yview)
        info_scroll.grid(row=0, column=1, sticky="ns")
        self.info_text.config(yscrollcommand=info_scroll.set)
        
        # Right Panel - Kết quả kiểm tra dạng chuẩn
        right_frame = tk.LabelFrame(
            content_frame,
            text="📊 Kết Quả Kiểm Tra Dạng Chuẩn",
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
            bg='#fdf2e9',
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
        
    def open_file(self):
        """Mở và đọc file"""
        file_path = filedialog.askopenfilename(
            title="Chọn file quan hệ",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            filename = file_path.split('/')[-1]
            
            # Xóa nội dung cũ
            self.file_label.config(text=f"📄 {filename}", fg='#2c3e50')
            self.info_text.config(state=tk.NORMAL)
            self.info_text.delete(1.0, tk.END)
            self.fd_set.clear()
            self.all_attributes.clear()
            self.all_keys.clear()
            
            # Đọc file
            with open(file_path, 'r', encoding='utf-8') as file:
                file_data = file.read().strip()
            
            if not file_data:
                messagebox.showwarning("Cảnh báo", "File rỗng!")
                return
            
            lines = file_data.split('\n')
            lines = [line.strip() for line in lines if line.strip()]
            
            if len(lines) < 2:
                messagebox.showwarning("Cảnh báo", "File phải có ít nhất 2 dòng!")
                return
            
            # Dòng đầu tiên là tập thuộc tính
            relation_line = lines[0].strip()
            self.all_attributes = set(relation_line.replace(' ', ''))
            
            # Hiển thị thông tin cơ bản
            self.info_text.insert(tk.END, "THÔNG TIN QUAN HỆ\n")
            self.info_text.insert(tk.END, "=" * 40 + "\n\n")
            self.info_text.insert(tk.END, f"Tập thuộc tính R = {{{', '.join(sorted(self.all_attributes))}}}\n")
            self.info_text.insert(tk.END, f"Số thuộc tính: {len(self.all_attributes)}\n\n")
            
            # Các dòng tiếp theo là phụ thuộc hàm
            self.info_text.insert(tk.END, "TẬP PHỤ THUỘC HÀM F:\n")
            self.info_text.insert(tk.END, "-" * 30 + "\n")
            
            fd_count = 0
            for i, line in enumerate(lines[1:], 1):
                line = line.strip()
                if not line:
                    continue
                
                fd = self.parse_fd_format(line)
                if fd:
                    self.fd_set.append(fd)
                    fd_count += 1
                    self.info_text.insert(tk.END, f"FD{fd_count}: {fd}\n")
            
            self.info_text.insert(tk.END, f"\nTổng số FD: {fd_count}\n")
            self.info_text.config(state=tk.DISABLED)
            
            # Cập nhật trạng thái button
            if self.fd_set:
                self.check_button.config(state='normal')
            
            self.update_stats()
            
            messagebox.showinfo("Thành công", f"Đã đọc {fd_count} phụ thuộc hàm!")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
    
    def parse_fd_format(self, line):
        """Phân tích phụ thuộc hàm"""
        try:
            if '-' not in line:
                return None
            
            parts = line.split('-')
            if len(parts) != 2:
                return None
            
            lhs_part = parts[0].strip()
            rhs_part = parts[1].strip()
            
            lhs_attrs = set(lhs_part.split())
            rhs_attrs = set(rhs_part.split())
            
            if not lhs_attrs.union(rhs_attrs).issubset(self.all_attributes):
                return None
            
            return FD(lhs_attrs, rhs_attrs)
            
        except Exception:
            return None
    
    def update_stats(self):
        """Cập nhật thống kê"""
        stats_text = f"FD: {len(self.fd_set)} | Thuộc tính: {len(self.all_attributes)}"
        if self.all_keys:
            stats_text += f" | Khóa: {len(self.all_keys)}"
        self.stats_label.config(text=stats_text)
    
    def check_normal_forms(self):
        """Kiểm tra các dạng chuẩn"""
        if not self.fd_set or not self.all_attributes:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file trước!")
            return
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        self.result_text.insert(tk.END, "KIỂM TRA DẠNG CHUẨN CỦA QUAN HỆ\n")
        self.result_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # Tìm tất cả các khóa trước
        self.find_all_keys()
        
        # Xác định thuộc tính chính và không chính
        self.classify_attributes()
        
        # Hiển thị thông tin về khóa
        self.result_text.insert(tk.END, "THÔNG TIN VỀ KHÓA:\n")
        self.result_text.insert(tk.END, "-" * 30 + "\n")
        
        if self.all_keys:
            for i, key in enumerate(self.all_keys, 1):
                self.result_text.insert(tk.END, f"Khóa {i}: {{{', '.join(sorted(key))}}}\n")
        else:
            self.result_text.insert(tk.END, "Không tìm thấy khóa nào!\n")
        
        self.result_text.insert(tk.END, f"\nThuộc tính chính: {{{', '.join(sorted(self.prime_attributes))}}}\n")
        self.result_text.insert(tk.END, f"Thuộc tính không chính: {{{', '.join(sorted(self.non_prime_attributes))}}}\n\n")
        
        # Kiểm tra từng dạng chuẩn
        is_1nf = self.check_1nf()
        is_2nf = self.check_2nf() if is_1nf else False
        is_3nf = self.check_3nf() if is_2nf else False
        is_bcnf = self.check_bcnf() if is_3nf else False
        
        # Kết luận
        self.result_text.insert(tk.END, "KẾT LUẬN:\n")
        self.result_text.insert(tk.END, "=" * 30 + "\n")
        
        if is_bcnf:
            self.result_text.insert(tk.END, "✅ Quan hệ đạt dạng chuẩn BCNF (Boyce-Codd)\n")
        elif is_3nf:
            self.result_text.insert(tk.END, "✅ Quan hệ đạt dạng chuẩn 3NF (Third Normal Form)\n")
        elif is_2nf:
            self.result_text.insert(tk.END, "✅ Quan hệ đạt dạng chuẩn 2NF (Second Normal Form)\n")
        elif is_1nf:
            self.result_text.insert(tk.END, "✅ Quan hệ đạt dạng chuẩn 1NF (First Normal Form)\n")
        else:
            self.result_text.insert(tk.END, "❌ Quan hệ không đạt dạng chuẩn 1NF\n")
        
        self.result_text.config(state=tk.DISABLED)
        self.update_stats()
    
    def find_all_keys(self):
        """Tìm tất cả các khóa"""
        all_subsets = []
        sorted_attrs = sorted(self.all_attributes)
        
        # Sinh tất cả các tập con
        for size in range(1, len(self.all_attributes) + 1):
            for subset in combinations(sorted_attrs, size):
                all_subsets.append(set(subset))
        
        # Tìm siêu khóa
        superkey_candidates = []
        for subset in all_subsets:
            closure = self.compute_closure(subset)
            if closure == self.all_attributes:
                superkey_candidates.append(subset)
        
        # Tìm khóa tối thiểu
        keys = []
        superkey_candidates.sort(key=len)
        
        for candidate in superkey_candidates:
            is_minimal = True
            for existing_key in keys:
                if existing_key.issubset(candidate):
                    is_minimal = False
                    break
            if is_minimal:
                keys.append(candidate)
        
        self.all_keys = keys
    
    def classify_attributes(self):
        """Phân loại thuộc tính chính và không chính"""
        self.prime_attributes = set()
        
        # Thuộc tính chính là những thuộc tính xuất hiện trong ít nhất một khóa
        for key in self.all_keys:
            self.prime_attributes.update(key)
        
        self.non_prime_attributes = self.all_attributes - self.prime_attributes
    
    def check_1nf(self):
        """Kiểm tra dạng chuẩn 1NF"""
        self.result_text.insert(tk.END, "KIỂM TRA 1NF (First Normal Form):\n")
        self.result_text.insert(tk.END, "-" * 40 + "\n")
        
        # Giả định quan hệ đã ở dạng 1NF (tất cả giá trị nguyên tử)
        self.result_text.insert(tk.END, "✅ Tất cả thuộc tính có giá trị nguyên tử\n")
        self.result_text.insert(tk.END, "✅ Quan hệ đạt dạng chuẩn 1NF\n\n")
        
        return True
    
    def check_2nf(self):
        """Kiểm tra dạng chuẩn 2NF"""
        self.result_text.insert(tk.END, "KIỂM TRA 2NF (Second Normal Form):\n")
        self.result_text.insert(tk.END, "-" * 40 + "\n")
        
        self.result_text.insert(tk.END, "Điều kiện: Không có thuộc tính không chính nào phụ thuộc một phần vào khóa\n\n")
        
        violations = []
        
        # Kiểm tra từng FD
        for fd in self.fd_set:
            lhs = fd.getLhs()
            rhs = fd.getRhs()
            
            # Kiểm tra nếu RHS chứa thuộc tính không chính
            non_prime_in_rhs = rhs.intersection(self.non_prime_attributes)
            if not non_prime_in_rhs:
                continue
            
            # Kiểm tra nếu LHS là tập con thực sự của một khóa nào đó
            for key in self.all_keys:
                if lhs.issubset(key) and lhs != key:
                    violations.append((fd, key, non_prime_in_rhs))
                    break
        
        if violations:
            self.result_text.insert(tk.END, "❌ Tìm thấy các vi phạm 2NF:\n")
            for fd, key, non_prime_attrs in violations:
                self.result_text.insert(tk.END, f"   - FD {fd}: {{{', '.join(sorted(non_prime_attrs))}}} phụ thuộc một phần vào khóa {{{', '.join(sorted(key))}}}\n")
            self.result_text.insert(tk.END, "❌ Quan hệ KHÔNG đạt dạng chuẩn 2NF\n\n")
            return False
        else:
            self.result_text.insert(tk.END, "✅ Không có vi phạm 2NF\n")
            self.result_text.insert(tk.END, "✅ Quan hệ đạt dạng chuẩn 2NF\n\n")
            return True
    
    def check_3nf(self):
        """Kiểm tra dạng chuẩn 3NF"""
        self.result_text.insert(tk.END, "KIỂM TRA 3NF (Third Normal Form):\n")
        self.result_text.insert(tk.END, "-" * 40 + "\n")
        
        self.result_text.insert(tk.END, "Điều kiện: Không có thuộc tính không chính nào phụ thuộc bắc cầu vào khóa\n\n")
        
        violations = []
        
        # Kiểm tra từng FD
        for fd in self.fd_set:
            lhs = fd.getLhs()
            rhs = fd.getRhs()
            
            # Kiểm tra nếu RHS chứa thuộc tính không chính
            non_prime_in_rhs = rhs.intersection(self.non_prime_attributes)
            if not non_prime_in_rhs:
                continue
            
            # Kiểm tra nếu LHS không phải là siêu khóa và chứa thuộc tính không chính
            lhs_closure = self.compute_closure(lhs)
            is_superkey = lhs_closure == self.all_attributes
            
            if not is_superkey and lhs.intersection(self.non_prime_attributes):
                violations.append((fd, non_prime_in_rhs))
        
        if violations:
            self.result_text.insert(tk.END, "❌ Tìm thấy các vi phạm 3NF:\n")
            for fd, non_prime_attrs in violations:
                self.result_text.insert(tk.END, f"   - FD {fd}: Phụ thuộc bắc cầu qua thuộc tính không chính\n")
            self.result_text.insert(tk.END, "❌ Quan hệ KHÔNG đạt dạng chuẩn 3NF\n\n")
            return False
        else:
            self.result_text.insert(tk.END, "✅ Không có vi phạm 3NF\n")
            self.result_text.insert(tk.END, "✅ Quan hệ đạt dạng chuẩn 3NF\n\n")
            return True
    
    def check_bcnf(self):
        """Kiểm tra dạng chuẩn BCNF"""
        self.result_text.insert(tk.END, "KIỂM TRA BCNF (Boyce-Codd Normal Form):\n")
        self.result_text.insert(tk.END, "-" * 45 + "\n")
        
        self.result_text.insert(tk.END, "Điều kiện: Với mọi FD X→Y, X phải là siêu khóa\n\n")
        
        violations = []
        
        # Kiểm tra từng FD
        for fd in self.fd_set:
            lhs = fd.getLhs()
            rhs = fd.getRhs()
            
            # Tính bao đóng của LHS
            lhs_closure = self.compute_closure(lhs)
            
            # Kiểm tra nếu LHS không phải là siêu khóa
            if lhs_closure != self.all_attributes:
                violations.append(fd)
        
        if violations:
            self.result_text.insert(tk.END, "❌ Tìm thấy các vi phạm BCNF:\n")
            for fd in violations:
                self.result_text.insert(tk.END, f"   - FD {fd}: LHS không phải là siêu khóa\n")
            self.result_text.insert(tk.END, "❌ Quan hệ KHÔNG đạt dạng chuẩn BCNF\n\n")
            return False
        else:
            self.result_text.insert(tk.END, "✅ Không có vi phạm BCNF\n")
            self.result_text.insert(tk.END, "✅ Quan hệ đạt dạng chuẩn BCNF\n\n")
            return True
    
    def compute_closure(self, attributes):
        """Tính toán bao đóng của một tập thuộc tính"""
        closure = attributes.copy()
        changed = True
        
        while changed:
            changed = False
            for fd in self.fd_set:
                if fd.getLhs().issubset(closure):
                    before_size = len(closure)
                    closure = closure.union(fd.getRhs())
                    if len(closure) > before_size:
                        changed = True
        
        return closure