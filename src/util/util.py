from data_structures.functional_dependency import FD

class util:
    @staticmethod
    def parse_fd_line(line):
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