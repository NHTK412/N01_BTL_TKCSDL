# main.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Menu
from functional_dependency import FD
import copy
from itertools import combinations

class KeyFinder:
    DANH_SACH_TV = [
        {
            "name": "Nguyễn Hữu Tuấn Khang",
            "id": "058205002155",
        },
        {
            "name": "Hà Nguyễn Đình Phú",
            "id": "083205001449",
        },
        {
            "name": "Trương Chế Linh",
            "id": ""
        },
        {
            "name": "Phan Quang Thoại",
            "id": ""
        },
        {
            "name": "Trần Nguyễn Khang",
            "id": ""
        },
        {
            "name": "Nguyễn Thị Tuyết Nhi",
            "id": "087305003168"
        },
        {
            "name": "Đào Thị Mỹ Duyên",
            "id": ""
        }
    ]
    
    def __init__(self):
        self.root = tk.Tk()
        self.fd_set = []
        self.all_attributes = set()
        self.all_keys = []
        self.setup_window()
        self.create_menu()
        self.create_widgets()
        
    def setup_window(self):
        """Thiết lập cửa sổ chính"""
        self.root.title("Bài Tập Lớn Môn Thiết Kế Cơ Sở Dữ Liệu - Tìm Tất Cả Các Khóa")
        self.root.attributes("-topmost", True)
        
        try:
            icon = tk.PhotoImage(file="src/assets/icon2.png")  
            self.root.iconphoto(False, icon)
        except:
            pass  # Bỏ qua nếu không tìm thấy icon

        # Căn giữa cửa sổ
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1200) // 2
        y = (screen_height - 700) // 2
        self.root.geometry(f"1200x700+{x}+{y}")
        
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f0f0')
        
        # Cấu hình grid
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)
    
    def create_menu(self):
        menu = Menu(self.root)
        menu.add_cascade(label="Key Finder")

        menu_member = Menu(menu)
        for i in self.DANH_SACH_TV:
            menu_member.add_command(label=i["name"],
                                    command=lambda name=i["name"], id=i["id"]: 
                                    messagebox.showinfo("Thông Tin Thành Viên", 
                                                        f"Tên: {name}\nMSSV: {id}"))

        menu.add_cascade(label="Thông Tin Thành Viên", menu=menu_member)
        
        self.root.config(menu=menu)

    def create_widgets(self):
        """Tạo các widget"""
        # Header Frame
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.grid(row=0, 
                          column=0, 
                          columnspan=2, 
                          sticky="ew", 
                          padx=10, 
                          pady=(10, 0))
        
        header_frame.grid_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🔑 TÌM TẤT CẢ CÁC KHÓA CỦA LƯỢC ĐỒ QUAN HỆ",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        # Content Frame
        content_frame = tk.Frame(self.root, bg='#f0f0f0')
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
        
        # Button tìm khóa (đặt ở giữa)
        calc_frame = tk.Frame(control_frame, bg='#f0f0f0')
        calc_frame.pack(expand=True, fill='both')
        
        self.calc_button = ttk.Button(
            calc_frame,
            text="🔑 Tìm Tất Cả Các Khóa",
            style='Custom.TButton',
            command=self.find_all_keys,
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
            text="📝 Tập Phụ Thuộc Hàm và Thuộc Tính",
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
        
        # Right Panel - Kết quả tìm khóa và các bước
        right_frame = tk.LabelFrame(
            content_frame,
            text="🔑 Kết Quả Tìm Khóa và Các Bước Thực Hiện",
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
                fd = self.parse_fd_line(line)
                if fd:
                    self.fd_set.append(fd)
                    fd_count += 1
                    self.fd_text.insert(tk.END, f"FD{fd_count}: {fd}\n")
                    
                    # Thu thập tất cả thuộc tính
                    self.all_attributes.update(fd.getLhs())
                    self.all_attributes.update(fd.getRhs())

            # Hiển thị tập thuộc tính R
            self.fd_text.insert(tk.END, f"\nTập thuộc tính R = {{{', '.join(sorted(self.all_attributes))}}}\n")
            self.fd_text.insert(tk.END, f"Số thuộc tính: {len(self.all_attributes)}\n")
            
            self.fd_text.config(state=tk.DISABLED)
            
            # Cập nhật trạng thái button
            if self.fd_set:
                self.calc_button.config(state='normal')
            
            # Cập nhật thống kê
            self.update_stats()
            
            messagebox.showinfo("Thành công", f"Đã đọc {fd_count} phụ thuộc hàm!")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
            
    def parse_fd_line(self, line):
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
        stats_text = f"FD: {len(self.fd_set)} | Thuộc tính: {len(self.all_attributes)}"
        if self.all_keys:
            stats_text += f" | Khóa: {len(self.all_keys)}"
        self.stats_label.config(text=stats_text)
    
    def find_all_keys(self):
        """Tìm tất cả các khóa theo thuật toán đã cho"""
        if not self.fd_set or not self.all_attributes:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file trước!")
            return
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        self.result_text.insert(tk.END, "TÌM TẤT CẢ CÁC KHÓA CỦA LƯỢC ĐỒ QUAN HỆ R\n")
        self.result_text.insert(tk.END, "=" * 50 + "\n\n")
        
        self.result_text.insert(tk.END, f"Tập thuộc tính R = {{{', '.join(sorted(self.all_attributes))}}}\n")
        self.result_text.insert(tk.END, f"Tập phụ thuộc hàm F có {len(self.fd_set)} FD\n\n")
        
        # Bước 1: Sinh tất cả các tập con không rỗng của R, sắp xếp theo thứ tự tăng dần
        self.result_text.insert(tk.END, "BƯỚC 1: Sinh tất cả các tập con không rỗng của R, sắp xếp theo kích thước tăng dần\n")
        self.result_text.insert(tk.END, "-" * 70 + "\n")
        
        all_subsets = []
        sorted_attrs = sorted(self.all_attributes)
        
        # Sinh tất cả các tập con từ kích thước 1 đến n
        for size in range(1, len(self.all_attributes) + 1):
            for subset in combinations(sorted_attrs, size):
                all_subsets.append(set(subset))
        
        self.result_text.insert(tk.END, f"Tổng số tập con không rỗng: {len(all_subsets)}\n")
        
        # Hiển thị một số tập con đầu tiên
        self.result_text.insert(tk.END, "Các tập con theo kích thước:\n")
        for size in range(1, min(4, len(self.all_attributes) + 1)):
            subsets_of_size = [s for s in all_subsets if len(s) == size]
            if subsets_of_size:
                self.result_text.insert(tk.END, f"Kích thước {size}: ")
                for i, subset in enumerate(subsets_of_size[:10]):  # Hiển thị tối đa 10 tập con
                    self.result_text.insert(tk.END, f"{{{', '.join(sorted(subset))}}}")
                    if i < len(subsets_of_size) - 1 and i < 9:
                        self.result_text.insert(tk.END, ", ")
                if len(subsets_of_size) > 10:
                    self.result_text.insert(tk.END, f", ... (và {len(subsets_of_size) - 10} tập con khác)")
                self.result_text.insert(tk.END, "\n")
        self.result_text.insert(tk.END, "\n")
        
        # Bước 2: Tính bao đóng của các tập con
        self.result_text.insert(tk.END, "BƯỚC 2: Tính bao đóng của các tập con\n")
        self.result_text.insert(tk.END, "-" * 50 + "\n")
        
        closures = {}
        superkey_candidates = []
        
        for subset in all_subsets:
            closure = self.compute_closure(subset, self.fd_set)
            closures[frozenset(subset)] = closure
            
            # Kiểm tra xem closure có bằng R không
            if closure == self.all_attributes:
                superkey_candidates.append(subset)
        
        self.result_text.insert(tk.END, f"Tìm thấy {len(superkey_candidates)} siêu khóa (tập con có bao đóng = R)\n\n")
        
        # Bước 3: Chỉ giữ lại các tập có bao đóng bằng R
        self.result_text.insert(tk.END, "BƯỚC 3: Các siêu khóa (tập con có bao đóng = R)\n")
        self.result_text.insert(tk.END, "-" * 50 + "\n")
        
        for i, superkey in enumerate(superkey_candidates, 1):
            self.result_text.insert(tk.END, f"Siêu khóa {i}: {{{', '.join(sorted(superkey))}}}\n")
        self.result_text.insert(tk.END, "\n")
        
        # Bước 4: Loại bỏ các tập chứa tập con khác trong danh sách
        self.result_text.insert(tk.END, "BƯỚC 4: Loại bỏ các siêu khóa chứa siêu khóa khác (tìm khóa tối thiểu)\n")
        self.result_text.insert(tk.END, "-" * 70 + "\n")
        
        keys = []
        
        # Sắp xếp theo kích thước để kiểm tra từ nhỏ đến lớn
        superkey_candidates.sort(key=len)
        
        for candidate in superkey_candidates:
            is_minimal = True
            
            # Kiểm tra xem candidate có chứa khóa nào đã tìm thấy không
            for existing_key in keys:
                if existing_key.issubset(candidate):
                    is_minimal = False
                    self.result_text.insert(tk.END, f"Loại bỏ {{{', '.join(sorted(candidate))}}} vì chứa khóa {{{', '.join(sorted(existing_key))}}}\n")
                    break
            
            if is_minimal:
                keys.append(candidate)
                self.result_text.insert(tk.END, f"Giữ lại khóa: {{{', '.join(sorted(candidate))}}}\n")
        
        self.result_text.insert(tk.END, "\n")
        
        # Bước 5: Kết quả cuối cùng
        self.all_keys = keys
        
        self.result_text.insert(tk.END, "BƯỚC 5: TẤT CẢ CÁC KHÓA CỦA LƯỢC ĐỒ QUAN HỆ R\n")
        self.result_text.insert(tk.END, "=" * 50 + "\n")
        
        if self.all_keys:
            for i, key in enumerate(self.all_keys, 1):
                self.result_text.insert(tk.END, f"Khóa {i}: {{{', '.join(sorted(key))}}}\n")
        else:
            self.result_text.insert(tk.END, "Không tìm thấy khóa nào!\n")
        
        self.result_text.insert(tk.END, f"\nTổng số khóa tìm thấy: {len(self.all_keys)}\n")
        
        # Thống kê thêm
        if self.all_keys:
            min_key_size = min(len(key) for key in self.all_keys)
            max_key_size = max(len(key) for key in self.all_keys)
            self.result_text.insert(tk.END, f"Kích thước khóa nhỏ nhất: {min_key_size}\n")
            self.result_text.insert(tk.END, f"Kích thước khóa lớn nhất: {max_key_size}\n")
        
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
    
    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()


# Chạy ứng dụng 
if __name__ == "__main__":
    app = KeyFinder()
    app.run()