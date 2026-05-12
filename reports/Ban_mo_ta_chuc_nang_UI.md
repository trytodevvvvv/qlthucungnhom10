# Bản mô tả chức năng và thiết kế UI sơ bộ: Phần mềm quản lý cửa hàng thú cưng

## 1. Giới thiệu chung
Phần mềm quản lý cửa hàng thú cưng (Pet Shop) được xây dựng nhằm hỗ trợ chủ cửa hàng và ban quản lý vận hành toàn diện các hoạt động kinh doanh: từ bán lẻ sản phẩm (thức ăn, phụ kiện), quản lý dịch vụ chăm sóc (spa, cắt tỉa lông, lưu chuồng), đến quản lý hồ sơ sức khỏe thú cưng và khách hàng. Hệ thống giúp tối ưu hóa quy trình làm việc, kiểm soát tồn kho chặt chẽ, tránh sai sót trong việc đặt lịch và bám sát trải nghiệm chăm sóc khách hàng một cách chuyên nghiệp nhất.

### 1.1 Mục tiêu hệ thống
- Quản lý tập trung toàn bộ dữ liệu, lịch sử giao dịch và hồ sơ sức khỏe thú cưng.
- Quản lý hàng hóa, tồn kho sản phẩm tự động, cảnh báo khi sắp hết hàng hoặc cận hạn sử dụng.
- Lên lịch và theo dõi trực quan các dịch vụ chăm sóc thú cưng (Spa, Grooming, Pet Hotel).
- Số hóa và đẩy nhanh nghiệp vụ bán hàng (POS) với tích hợp quét mã vạch, thanh toán, in hóa đơn.
- Cung cấp hệ thống báo cáo doanh thu, chi phí, lợi nhuận chi tiết.

### 1.2 Đối tượng sử dụng
- **Quản trị viên / Chủ cửa hàng:** Quản lý toàn bộ hệ thống, thiết lập giá, danh mục, phân quyền và theo dõi báo cáo.
- **Nhân viên thu ngân / Lễ tân:** Thực hiện nghiệp vụ POS, thanh toán, nghe điện thoại đặt lịch và tư vấn dịch vụ.
- **Nhân viên chăm sóc (Groomer / Bác sĩ thú y):** Xem lịch làm việc của mình, cập nhật trạng thái thú cưng trong và sau khi thực hiện dịch vụ.
- **Khách hàng :** Đặt lịch dịch vụ trực tuyến, xem lịch sử tiêm phòng, theo dõi điểm thưởng.

---

## 2. Các chức năng chính của ứng dụng

### 2.1 Quản lý đăng nhập và phân quyền
- **Mô tả:** Đảm bảo an toàn thông tin và chỉ định đúng quyền hạn cho từng vị trí nhân sự.
- **Chức năng chi tiết:**
  - Đăng nhập bảo mật tài khoản cá nhân. Cấp lại mật khẩu khi quên.
  - Phân quyền theo vai trò: Chủ cửa hàng (toàn quyền), Thu ngân (Thao tác bán hàng, lập hóa đơn), Thợ cắt tỉa/Spa (Chỉ xem lịch hẹn và cập nhật trạng thái làm việc).
  - Ghi vết lưu lại lịch sử thao tác của các tài khoản (Log history).
- **Kết quả mong đợi:** Dữ liệu kinh doanh được bảo mật tối đa, không bị chỉnh sửa trái phép từ nhân viên không có thẩm quyền.

### 2.2 Quản lý khách hàng và hồ sơ thú cưng (Pet Profile)
- **Mô tả:** Lưu trữ thông tin của chủ vật nuôi liên kết chặt chẽ với từng cá thể thú cưng.
- **Chức năng chi tiết:**
  - **Hồ sơ chủ nuôi:** Họ tên, SĐT, địa chỉ, lịch sử mua hàng, hạng thẻ (Bạc, Vàng, VIP) và điểm tích lũy.
  - **Hồ sơ thú cưng:** Tên, loài (Chó/Mèo...), giống, ngày sinh, cân nặng, hình ảnh, đặc điểm nhận dạng.
  - **Hồ sơ sức khỏe:** Ghi sổ lịch sử tiêm phòng, tẩy giun, dị ứng hoặc tiền sử bệnh lý cần lưu ý.
- **Kết quả mong đợi:** Tăng cường dịch vụ chăm sóc thú cưng một cách cá nhân hóa, hiểu đúng tình trạng của Pet để phục vụ tốt nhất.

### 2.3 Quản lý hàng hóa, sản phẩm (Tồn kho)
- **Mô tả:** Quản lý số lượng mặt hàng như thức ăn, cát vệ sinh, đồ chơi, phụ kiện, thuốc thú y, v.v.
- **Chức năng chi tiết:**
  - Thêm, sửa, xóa thông tin sản phẩm (có mã SKU, mã vạch, giá nhập, giá bán lẻ).
  - Phân loại theo nhà cung cấp, theo danh mục sản phẩm (Đồ ăn chó / Đồ ăn mèo / Phụ kiện làm đẹp).
  - Khai báo nhập kho, xuất hủy, kiểm kê kho.
  - Cảnh báo sản phẩm bán chạy bị thiếu hụt hoặc sản phẩm tới gần ngày hết hạn.
- **Kết quả mong đợi:** Hàng hóa luôn ở mức tối ưu, giảm thiểu tỷ lệ thất thoát.

### 2.4 Quản lý dịch vụ và gói thẻ
- **Mô tả:** Quản lý quy định, giá thành của các khối dịch vụ mà Pet Shop cung cấp.
- **Chức năng chi tiết:**
  - Tạo mới các dịch vụ: Tắm sấy, Cắt tỉa (Grooming), Cạo lông, Vệ sinh tai móng, Khám bệnh cơ bản.
  - Phân tách bảng giá linh động: Giá thay đổi tùy thuộc vào "Cân nặng" hoặc thiết lập riêng cho "Chó/Mèo".
  - Bán gói liệu trình (Combo/Gói): VD mua 10 buổi tắm tặng 1 buổi. Theo dõi số buổi đã sử dụng.
  - Thiết lập tính hoa hồng theo % cho nhân viên spa khi thực hiện xong dịch vụ.
- **Kết quả mong đợi:** Định giá khoa học, khuyến khích khách mua trọn gói dịch vụ.

### 2.5 Quản lý đặt lịch hẹn (Booking) và Lịch làm việc
- **Mô tả:** Tiếp nhận và phân bổ thời gian thực hiện dịch vụ để không bị quá tải.
- **Chức năng chi tiết:**
  - Lễ tân tạo lịch hẹn trên hệ thống: Chọn thời gian, chọn dịch vụ, chọn thú cưng và (tùy chọn) chọn nhân viên Spa cụ thể.
  - Hiển thị theo giao diện Lịch (Calendar View). Hệ thống tự phát hiện và cảnh báo nếu trùng khung giờ của thợ Grooming.
  - Theo dõi trạng thái lịch: Mới đặt -> Đã nhận thú cưng -> Đang tắm/tỉa -> Hoàn thành (Chờ khách đón) -> Hủy lịch.
- **Kết quả mong đợi:** Sắp xếp lịch khoa học, giảm thời gian khách hàng ngồi đợi tại cửa sổ dịch vụ.

### 2.6 Quản lý khu vực Lưu chuồng (Khách sạn thú cưng / Pet Hotel)
- **Mô tả:** Dành cho cửa hàng có nhận nội trú đồ chơi qua đêm.
- **Chức năng chi tiết:**
  - Sơ đồ lồng chuồng: hiển thị trạng thái Trống, Đang có khách, Đang cần dọn dẹp.
  - Nhật ký chăm sóc trong ngày lưu chuồng: Đã ăn mấy bữa, tình trạng đi vệ sinh, hình ảnh theo dõi gửi cho khách.
  - Tự động tính phí check-in / check-out theo mốc giờ quy định của cửa hàng.
- **Kết quả mong đợi:** Vận hành khách sạn thú cưng quy củ, gia chủ vật nuôi cảm thấy cực kỳ an tâm làm việc, du lịch xa.

### 2.7 Bán hàng tại quầy (POS) & Thanh toán
- **Mô tả:** Giao diện tối ưu để nhân viên thu ngân lên đơn tính tiền cực nhanh.
- **Chức năng chi tiết:**
  - Hỗ trợ thiết bị quét mã vạch tích hợp.
  - Tạo đơn hàng kết hợp cả Sản phẩm bán lẻ + Khấu trừ Dịch vụ thẻ + Dịch vụ dùng 1 lần trong cùng 1 hóa đơn.
  - Áp dụng mã giảm giá, voucher, đổi điểm thưởng từ khách hàng thân thiết.
  - Hỗ trợ đa kênh thanh toán (Tiền mặt, Chuyển khoản QR ngân hàng, Quẹt thẻ POS). In hóa đơn tự động.
- **Kết quả mong đợi:** Tăng trải nghiệm mượt mà, quản lý dòng tiền minh bạch, hạn chế nhầm lẫn.

### 2.8 Chăm sóc khách hàng tự động (CRM) & Thông báo
- **Mô tả:** Công cụ tăng tương tác mạnh mẽ.
- **Chức năng chi tiết:**
  - Gửi tin nhắn SMS / Zalo nhắc nhở lịch hẹn sắp tới.
  - Hệ thống tự bốc dữ liệu báo lịch sắp tới ngày tiêm phòng định kỳ, nhắc tẩy giun.
  - Thông báo ưu đãi, chúc mừng vào sinh nhật của khách hàng hoặc sinh nhật thú cưng.
- **Kết quả mong đợi:** Tỷ lệ khách hàng quay lại cửa hàng tăng cao nhờ khâu chăm sóc tận tâm.

### 2.9 Báo cáo và thống kê
- **Mô tả:** Tóm tắt dữ liệu qua biểu đồ cho chủ đầu tư.
- **Chức năng chi tiết:**
  - Thống kê doanh thu theo ngày, tuần, tháng, năm. Tách biệt rõ chỉ số của Mảng Sản Phẩm vs Mảng Dịch Vụ.
  - Bảng xếp hạng các mặt hàng bán chạy, danh sách hàng tồn đọng cần khuyến mãi.
  - Báo cáo công nợ nhà cung cấp. Báo cáo chấm công, tính lương hoa hồng của nhân sự Spa.
- **Kết quả mong đợi:** Cung cấp đầy đủ thông tin để chủ shop kịp thời thay đổi chiến lược kinh doanh.

---

## 3. Yêu cầu phi chức năng
- **Bảo mật dữ liệu:** Hệ thống cần được sao lưu (backup) thường xuyên để không mất lịch sử khách hàng và sổ bệnh lý.
- **Giao diện hiện đại (UI/UX):** Phải được thiết kế có nhiều không gian, thân thiện, mang tính chất "Pet-friendly" như icon và màu sắc ấm áp tươi vui.
- **Tốc độ xử lý:** Phản hồi nhanh nhất, đặc biệt tại khu vực Bán hàng (POS) không được treo/lag máy.
- **Đa nền tảng:** Có thể quản trị bằng máy tính tại quầy lễ tân (Web/Desktop) và kiểm soát từ xa trên di động / máy tính bảng (Tablet) cho chủ quán hoặc thợ Groom chạy qua lại giữa các phòng.

## 4. Thiết kế UI cho các giao diện chính (Mockup Idea)
*(Sẽ cần dùng Figma hoặc Balsamiq để lên bản Wireframe)*

1. **Dashboard (Màn hình tổng quan):** Trang chủ chứa các Card KPI Doanh thu, số lịch chờ phục vụ trong ngày, đồ thị tồn kho gần hết, danh sách thú cưng sắp tới hạn tiêm ngừa.
2. **Màn hình Bán hàng (POS):** Layout 2 khung. Bên trái là Lưới Danh sách sản phẩm/dịch vụ dạng hình ảnh trực quan (hoặc nhập từ mã vạch nhảy xuống danh sách). Bên phải là Chi tiết giỏ đơn hàng tương ứng kèm thanh toán - Nút "Thanh Toán" để đỏ lớn, bắt mắt nổi bật.
3. **Màn hình Lịch Hẹn (Calendar Board):** Chia dạng Gantt chart theo timeline hàng ngang ứng với thời gian, hàng dọc là các cột nhân viên chăm sóc hoặc phòng dịch vụ. Có thể khéo thả (Drag & Drop) lịch nếu khách thay đổi giờ.
4. **Mô đun Hồ sơ Thú Cưng:** Như một sổ y bạ mini, có Avatar khoét tròn xinh xắn của thú cưng, Timeline tiểu sử bên dưới lưu các vết giao dịch, ảnh trước và sau cắt tỉa (Before & After image album).
