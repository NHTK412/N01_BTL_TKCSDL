import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Menu

from frame.key_finder import key_finder
from frame.MinimumCoverCalculator import MinimumCoverCalculator
from frame.FDReader import FDReader
from frame.FDProjectionCalculator import FDProjectionCalculator


class main_window(tk.Tk):

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
        super().__init__()
        self.setup_window()
        self.create_menu()
        self.frames = {}
        
        for F in (key_finder, MinimumCoverCalculator, FDReader, FDProjectionCalculator):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            # frame.pack()

        self.show_frame(key_finder)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
        
    def setup_window(self):
        """Thiết lập cửa sổ chính"""
        self.title("Bài Tập Lớn Môn Thiết Kế Cơ Sở Dữ Liệu")
        # self.attributes("-topmost", True)
        
        try:
            icon = tk.PhotoImage(file="src/assets/icon2.png")  
            self.iconphoto(False, icon)
        except:
            pass  # Bỏ qua nếu không tìm thấy icon

        # Căn giữa cửa sổ
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1200) // 2
        y = (screen_height - 600) // 2
        self.geometry(f"1200x600+{x}+{y}")
        
        self.resizable(True, True)
        self.configure(bg='#f0f0f0')
        
        # Cấu hình grid
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)


    def create_menu(self):
        menu = Menu(self)
        frame_menu = {
        "Tìm Khóa": key_finder,
        "Rút Gọn Phụ Thuộc Hàm": MinimumCoverCalculator,
        "Đọc Phụ Thuộc Hàm từ File": FDReader,
        "FDProjectionCalculator": FDProjectionCalculator
        }
        for label, frame_class in frame_menu.items():
            menu.add_command(label=label, command=lambda f=frame_class: self.show_frame(f))
        # menu.add_cascade(label="Key Finder", command = lambda: self.show_frame(key_finder))
        # menu.add_cascade(label="Minimum Cover Calculator", command = lambda: self.show_frame(MinimumCoverCalculator))

        menu_member = Menu(menu)
        for i in self.DANH_SACH_TV:
            menu_member.add_command(label=i["name"],
                                    command=lambda name=i["name"], id=i["id"]: 
                                    messagebox.showinfo("Thông Tin Thành Viên", 
                                                        f"Tên: {name}\nMSSV: {id}"))

        menu.add_cascade(label="Thông Tin Thành Viên", menu=menu_member)
        
        
        self.config(menu=menu)



if __name__ == "__main__":
    app = main_window();
    app.mainloop();