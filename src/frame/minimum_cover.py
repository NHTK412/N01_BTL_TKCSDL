# main.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Menu
from data_structures.functional_dependency import FD
import copy
from util.util import util

class MinimumCoverFrame(tk.Frame):
   
    def __init__(self, parent):
        super().__init__(parent)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.fd_set = []
        self.minimum_cover = []
        # self.setup_window()
        # self.create_menu()
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
            text="🔍 TÍNH MINIMUM COVER CỦA TẬP PHỤ THUỘC HÀM",
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
        
        # Button tính minimum cover (đặt ở giữa)
        calc_frame = tk.Frame(control_frame, bg='#f0f0f0')
        calc_frame.pack(expand=True, fill='both')
        
        self.calc_button = ttk.Button(
            calc_frame,
            text="🔍 Tính Minimum Cover",
            style='Custom.TButton',
            command=self.calculate_minimum_cover,
            state='disabled'
        )
        self.calc_button.pack(expand=True, pady=20)
        
        # Label thống kê
        self.stats_label = tk.Label(
            control_frame,
            text="",
            font=('Arial', 10, 'bold'),
            fg='#27ae60',
            bg='#f0f0f0'
        )
        self.stats_label.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Left Panel - Tập FD gốc
        left_frame = tk.LabelFrame(
            content_frame,
            text="📝 Tập Phụ Thuộc Hàm Gốc",
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
        
        # Right Panel - Kết quả minimum cover và các bước
        right_frame = tk.LabelFrame(
            content_frame,
            text="🔍 Kết Quả Minimum Cover và Các Bước Thực Hiện",
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

            self.fd_text.config(state=tk.DISABLED)
            
            # Cập nhật trạng thái button
            if self.fd_set:
                self.calc_button.config(state='normal')
            
            # Cập nhật thống kê
            self.update_stats()
            
            messagebox.showinfo("Thành công", f"Đã đọc {fd_count} phụ thuộc hàm!")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
            
   
        """Phân tích một dòng phụ thuộc hàm"""
        # Xử lý dấu mũi tên khác nhau
        arrow_symbols = ['->', '→', '-->', '－＞']
        
        for arrow in arrow_symbols:
            if arrow in line:
                parts = line.split(arrow)
                break
        else:
            # Nếu không tìm thấy mũi tên, thử tìm dấu '-'
            if '-' in line:
                tokens = line.split()
                if '-' in tokens:
                    arrow_index = tokens.index('-')
                    left_tokens = tokens[:arrow_index]
                    right_tokens = tokens[arrow_index + 1:]
                    
                    left_side = set([attr.strip() for token in left_tokens for attr in token if attr.isalnum()])
                    right_side = set([attr.strip() for token in right_tokens for attr in token if attr.isalnum()])
                else:
                    return None
            else:
                return None
        
        # Nếu đã tìm thấy mũi tên
        if 'parts' in locals() and len(parts) == 2:
            left_part = parts[0].strip()
            right_part = parts[1].strip()
            
            # Trích xuất các thuộc tính từ chuỗi
            left_side = set([attr for attr in left_part if attr.isalnum()])
            right_side = set([attr for attr in right_part if attr.isalnum()])
        
        if left_side and right_side:
            try:
                # Tạo đối tượng FD
                fd = FD(lhs=left_side, rhs=right_side)
                return fd
            except Exception as e:
                return None
        
        return None
    
    def update_stats(self):
        """Cập nhật thống kê"""
        stats_text = f"FD gốc: {len(self.fd_set)}"
        if self.minimum_cover:
            stats_text += f" | Minimum Cover: {len(self.minimum_cover)}"
        self.stats_label.config(text=stats_text)
    
    def calculate_minimum_cover(self):
        """Tính minimum cover theo thuật toán"""
        if not self.fd_set:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file trước!")
            return
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        self.result_text.insert(tk.END, "TÍNH MINIMUM COVER CỦA TẬP PHỤ THUỘC HÀM\n")
        self.result_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # Sao chép tập FD gốc
        current_fds = copy.deepcopy(self.fd_set)
        
        # Bước 1: Decompose right side FDs to one attribute
        self.result_text.insert(tk.END, "BƯỚC 1: Phân rã vế phải thành một thuộc tính\n")
        self.result_text.insert(tk.END, "-" * 50 + "\n")
        
        step1_fds = []
        for fd in current_fds:
            lhs = fd.getLhs()
            rhs = fd.getRhs()
            
            if len(rhs) > 1:
                # Phân rá thành nhiều FD với vế phải là một thuộc tính
                for attr in rhs:
                    new_fd = FD(lhs=lhs.copy(), rhs={attr})
                    step1_fds.append(new_fd)
                    self.result_text.insert(tk.END, f"Phân rã: {''.join(sorted(lhs))} → {''.join(sorted(rhs))} thành {''.join(sorted(lhs))} → {attr}\n")
            else:
                step1_fds.append(fd)
        
        current_fds = step1_fds
        
        self.result_text.insert(tk.END, f"\nSau bước 1: {len(current_fds)} FD\n")
        for i, fd in enumerate(current_fds, 1):
            self.result_text.insert(tk.END, f"FD{i}: {fd}\n")
        self.result_text.insert(tk.END, "\n")
        
        # Bước 2: Loại bỏ các FD thừa
        self.result_text.insert(tk.END, "BƯỚC 2: Loại bỏ các FD thừa\n")
        self.result_text.insert(tk.END, "-" * 50 + "\n")
        
        i = 0
        while i < len(current_fds):
            fd_to_test = current_fds[i]
            remaining_fds = current_fds[:i] + current_fds[i+1:]
            
            # Kiểm tra xem fd_to_test có thể suy diễn từ remaining_fds không
            if self.is_fd_implied_by_set(fd_to_test, remaining_fds):
                self.result_text.insert(tk.END, f"Loại bỏ FD thừa: {fd_to_test} (có thể suy diễn từ các FD còn lại)\n")
                current_fds.pop(i)
            else:
                self.result_text.insert(tk.END, f"Giữ lại: {fd_to_test} (không thể suy diễn từ các FD còn lại)\n")
                i += 1
        
        self.result_text.insert(tk.END, f"\nSau bước 2: {len(current_fds)} FD\n")
        for i, fd in enumerate(current_fds, 1):
            self.result_text.insert(tk.END, f"FD{i}: {fd}\n")
        self.result_text.insert(tk.END, "\n")
        
        # Bước 3: Rút gọn vế trái
        self.result_text.insert(tk.END, "BƯỚC 3: Rút gọn vế trái\n")
        self.result_text.insert(tk.END, "-" * 50 + "\n")
        
        for i, fd in enumerate(current_fds):
            lhs = fd.getLhs()
            rhs = fd.getRhs()
            
            if len(lhs) <= 1:
                continue
                
            # Thử loại bỏ từng thuộc tính từ vế trái
            attributes_to_remove = []
            for attr in lhs:
                reduced_lhs = lhs - {attr}
                if not reduced_lhs:  # Không thể loại bỏ tất cả
                    continue
                    
                # Tạo FD mới với vế trái rút gọn
                new_fd = FD(lhs=reduced_lhs, rhs=rhs.copy())
                
                # Tạo tập FD thử nghiệm
                test_fds = current_fds[:i] + [new_fd] + current_fds[i+1:]
                
                # Kiểm tra tương đương
                if self.are_fd_sets_equivalent(current_fds, test_fds):
                    attributes_to_remove.append(attr)
                    self.result_text.insert(tk.END, f"Có thể loại bỏ {attr} từ vế trái của {fd}\n")
                    break  # Chỉ loại bỏ một thuộc tính tại một thời điểm
            
            # Cập nhật FD với vế trái rút gọn
            if attributes_to_remove:
                new_lhs = lhs - set(attributes_to_remove)
                current_fds[i] = FD(lhs=new_lhs, rhs=rhs.copy())
                self.result_text.insert(tk.END, f"Rút gọn: {fd} → {current_fds[i]}\n")
        
        self.result_text.insert(tk.END, f"\nSau bước 3: {len(current_fds)} FD\n")
        for i, fd in enumerate(current_fds, 1):
            self.result_text.insert(tk.END, f"FD{i}: {fd}\n")
        self.result_text.insert(tk.END, "\n")
        
        # Kết quả cuối cùng
        self.minimum_cover = current_fds
        
        self.result_text.insert(tk.END, "KẾT QUẢ CUỐI CÙNG - MINIMUM COVER\n")
        self.result_text.insert(tk.END, "=" * 50 + "\n")
        
        for i, fd in enumerate(self.minimum_cover, 1):
            self.result_text.insert(tk.END, f"FD{i}: {fd}\n")
        
        self.result_text.insert(tk.END, f"\nSố lượng FD gốc: {len(self.fd_set)}\n")
        self.result_text.insert(tk.END, f"Số lượng FD trong Minimum Cover: {len(self.minimum_cover)}\n")
        self.result_text.insert(tk.END, f"Giảm được: {len(self.fd_set) - len(self.minimum_cover)} FD\n")
        
        self.result_text.config(state=tk.DISABLED)
        
        # Cập nhật thống kê
        self.update_stats()
    
    def is_fd_implied_by_set(self, fd, fd_set):
        """Kiểm tra xem một FD có thể suy diễn từ một tập FD không"""
        lhs = fd.getLhs()
        rhs = fd.getRhs()
        
        # Tính bao đóng của LHS sử dụng fd_set
        closure = self.compute_closure(lhs, fd_set)
        
        # Kiểm tra xem RHS có nằm trong bao đóng không
        return rhs.issubset(closure)
    
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
    
