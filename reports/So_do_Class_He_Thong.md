# Sơ đồ Class Hệ thống Quản lý Cửa hàng Thú cưng

Sơ đồ dưới đây mô tả cấu trúc các lớp (Class) và mối quan hệ giữa chúng trong hệ thống Pet Shop Management. Đặc biệt, logic liên kết giữa **Dịch vụ** và **Thú cưng** đã được xử lý thông qua bảng trung gian **Chi tiết lịch hẹn** để đảm bảo một lịch hẹn có thể đăng ký nhiều dịch vụ cho nhiều thú cưng khác nhau.

```plantuml
@startuml
skinparam classAttributeIconSize 0
skinparam classFontStyle bold
skinparam linetype ortho
skinparam nodesep 100
skinparam ranksep 100

' --- Định nghĩa các Class dựa trên thiết kế ---

class NguoiDung {
  +id : INT
  +ten_dang_nhap : string
  +vai_tro : string
  +mat_khau : string
  +email : string
  +so_dien_thoai : string
  +dang_nhap() : bool
  +dang_xuat() : bool
}

class QuanTriVien {
  +quan_ly_he_thong()
  +quan_ly_nhan_vien()
  +quan_ly_dich_vu()
}

class NhanVien {
  +phuc_vu_dich_vu()
}

class DichVu {
  +id : INT
  +ten_dich_vu : string
  +gia_tien : FLOAT
  +mo_ta : string
  +cap_nhat_gia() : void
}

class ChiTietLichHen {
  +id : INT
  +ghi_chu_rieng : string
  +trang_thai : string
}

class LichHen {
  +id : INT
  +thoi_gian : datetime
  +trang_thai : string
  +gio_bat_dau : time
  +gio_ket_thuc : time
  +xac_nhan() : void
  +huy_lich() : void
}

class ThuCung {
  +id : INT
  +ten_thu_cung : string
  +loai : string
  +giong : string
  +tuoi : int
  +cap_nhat_thong_tin() : void
}

class KhachHang {
  +id : INT
  +ho_ten : string
  +so_dien_thoai : string
  +dia_chi : string
  +hang_thanh_vien : string
  +diem_tich_luy : string
  +cap_nhat_thong_tin() : void
}

class HoaDon {
  +id : INT
  +tong_tien : float
  +giam_gia : float
  +ngay_tao : datetime
  +phuong_thuc_thanh_toan : string
  +tinh_tong_tien() : float
  +ap_dung_khuyen_mai() : void
}

class GhiChu {
  +id : int
  +noi_dung : text
  +ngay_tao : datetime
  +nguoi_tao : string
  +them_ghi_chu() : void
  +sua_ghi_chu() : void
}

' --- Các mối quan hệ (Relationships) ---

' Kế thừa từ Người Dùng
NguoiDung <|--down- QuanTriVien
NguoiDung <|--down- NhanVien

' Người dùng tạo Lịch hẹn
NguoiDung "1" -right-> "0..*" LichHen : tao_lich

' Logic Bảng trung gian (Chi tiết lịch hẹn)
' Lịch hẹn chứa nhiều chi tiết, mỗi chi tiết nối 1 dịch vụ với 1 thú cưng
LichHen "1" *-up-> "1..*" ChiTietLichHen : bao_gom
ChiTietLichHen "0..*" -up-> "1" DichVu : su_dung_dv
ChiTietLichHen "0..*" -right-> "1" ThuCung : phuc_vu_cho

' Khách hàng và Thú cưng
KhachHang "1" -up-> "1..*" ThuCung : so_huu
KhachHang "1" *-left-> "0..*" LichHen : dat_lich

' Các thành phần con của Lịch hẹn (Hóa đơn và Ghi chú)
LichHen "1" *-down-> "0..1" HoaDon : thanh_toan
LichHen "1" *-down-> "0..*" GhiChu : ghi_nhan

' Giữ layout ngang cho HoaDon và GhiChu
HoaDon -[hidden]right- GhiChu

@enduml
```

## Giải thích phần logic Bảng trung gian (Chi tiết lịch hẹn):

1. **Vấn đề trước đây:** Nếu Lịch hẹn kết nối trực tiếp với Thú cưng và Dịch vụ, hệ thống sẽ gặp khó khăn khi 1 khách hàng mang 2 con chó đến: một con cắt tỉa lông, một con tắm. Lịch hẹn không thể phân định rõ Dịch vụ nào áp dụng cho Thú cưng nào.
2. **Giải pháp Bảng trung gian (`ChiTietLichHen`):**
   - Lớp `ChiTietLichHen` nằm giữa và chia nhỏ `LichHen` thành nhiều dòng chi tiết.
   - **Mỗi chi tiết sẽ chỉ định rõ:** Đăng ký 1 `DichVu` cho 1 `ThuCung` cụ thể.
   - Nhờ đó, logic Lịch hẹn trở nên mềm dẻo, đáp ứng được mọi tình huống thực tế của phòng khám/spa thú cưng mà vẫn giữ được độ liên kết chặt chẽ (Clean Architecture).
   - `KhachHang` vẫn đóng vai trò trung tâm tạo ra `LichHen` và quản lý `ThuCung`.

