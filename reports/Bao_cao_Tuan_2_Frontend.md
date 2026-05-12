
## 4. Xây dựng Giao diện Frontend (Thực hành Tuần 2)

Trong tuần 2, dự án đã tiến hành hiện thực hóa các yêu cầu chức năng trên thành các giao diện phần mềm (Frontend). Các giao diện được xây dựng bằng công cụ **Qt Designer** dưới định dạng file `.ui` (XML) và kết nối khởi chạy thông qua **PyQt5** bằng ngôn ngữ Python.

Danh sách các giao diện chính đã được hoàn thiện trong thư mục `ui/`:

1. **Màn hình Đăng nhập (`login.ui`)**: Giao diện đăng nhập hệ thống, phân quyền (Quản trị viên, Nhân viên thu ngân, Thợ Grooming...).
2. **Dashboard Tổng quan (`dashboard.ui`)**: Cung cấp các biểu đồ thẻ (Card) ghi nhận KPI doanh thu, số lượng khách đang chờ lịch, báo cáo tồn kho và danh sách nhắc tiêm ngừa thú cưng.
3. **Màn hình Bán hàng POS (`pos.ui`)**: Thiết kế lưới (Grid layout) chia 2 khung tối ưu hóa cho thu ngân dễ dàng quét mã vạch bán hàng, chọn nhanh dịch vụ và thanh toán in hóa đơn siêu tốc.
4. **Mô đun Hồ sơ Thú cưng (`pet_profile.ui`)**: Giao diện sổ y bạ số hóa hiển thị thông tin chung, biểu đồ lịch sử khám bệnh (Timeline) và thư viện ảnh Before/After khi sử dụng dịch vụ Spa.
5. **Màn hình Lịch hẹn (`calendar_board.ui`)**: Giao diện tiến độ theo dạng biểu đồ Gantt Chart phân bổ các khung giờ, hỗ trợ Lễ tân xếp lịch (Booking) và chống xung đột phòng/nhân sự.
6. **Màn hình Quản lý Kho hàng (`inventory.ui`)**: Bảng giao diện nhập/xuất kho vật tư, thanh tìm kiếm nhanh các mặt hàng và theo dõi giới hạn tồn kho.
7. **Màn hình Dịch vụ & Gói Combo (`services.ui`)**: Bảng hệ thống cập nhật giá Spa/Grooming theo cân nặng/giống loài của pet, cùng việc gán hoa hồng cho từng nhóm thợ.
8. **Khách sạn Thú cưng (`pet_hotel.ui`)**: Bản đồ điều phối các lồng/chuồng với nút bấm màu sắc cảnh báo trực quan (Ví dụ: lồng chờ dọn, lồng đang sử dụng) và hệ thống ghi chú bữa ăn, vệ sinh.
9. **CRM & Thông báo (`crm_notifications.ui`)**: Module tích hợp gửi hàng loạt (Bulk send) các tin nhắn Zalo/SMS đến khách hàng nhằm nhắc nhở tái khám, tới lịch tiêm ngừa định kỳ.
