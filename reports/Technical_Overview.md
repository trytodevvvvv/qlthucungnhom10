# Tổng quan Kiến trúc Kỹ thuật - PetShop Pro

Tài liệu này tóm tắt các công nghệ và cấu trúc code được sử dụng trong dự án quản lý cửa hàng thú cưng.

## 1. Công nghệ sử dụng (Tech Stack)

Trái với FastAPI, dự án này được xây dựng trên nền tảng **Flask Framework** - một micro-framework cực kỳ phổ biến và linh hoạt của Python.

*   **Backend Framework**: [Flask](https://flask.palletsprojects.com/) (Python).
*   **Database ORM**: SQLAlchemy (thông qua `Flask-SQLAlchemy`).
*   **Database Migration**: Flask-Migrate (Alembic).
*   **Authentication**: Flask-Login (Quản lý phiên đăng nhập và phân quyền).
*   **Template Engine**: Jinja2 (Dùng để render HTML động từ Server).
*   **Frontend**: HTML5, Vanilla CSS (Custom thiết kế), FontAwesome 6 (Icons).

## 2. Cấu trúc thư mục (Project Structure)

Dự án áp dụng mô hình **Application Factory Pattern**, giúp code sạch sẽ và dễ mở rộng:

```text
├── app/
│   ├── routes/          # Chứa các Blueprint (Module chức năng: POS, Pets, Dashboard...)
│   ├── templates/       # Chứa các file giao diện HTML (Jinja2)
│   ├── static/          # Chứa CSS, JavaScript và hình ảnh
│   ├── models.py        # Định nghĩa cấu trúc các bảng Database (ORM)
│   ├── extensions.py    # Khởi tạo các thư viện ngoài (DB, Login Manager)
│   └── __init__.py      # Nơi khởi tạo Ứng dụng (Factory)
├── reports/             # Chứa tài liệu mô tả và báo cáo
├── config.py            # Cấu hình môi trường (Database URL, Secret Key)
├── run.py               # File chạy ứng dụng chính
└── seed.py              # Script nạp dữ liệu mẫu tự động
```

## 3. Cách thức Code và Luồng xử lý (Coding Methodology)

Dự án tuân thủ các nguyên tắc lập trình hiện đại:

### 3.1. Phân tách Module bằng Blueprints
Thay vì viết tất cả Route vào một file, dự án chia nhỏ thành các **Blueprint**:
*   `auth_bp`: Xử lý đăng nhập/đăng xuất.
*   `pets_bp`: Quản lý khách hàng và hồ sơ thú cưng.
*   `inventory_bp`: Quản lý kho hàng và sản phẩm.
*   `pos_bp`: Giao diện bán hàng tại quầy.
*   `services_bp` & `bookings_bp`: Quản lý dịch vụ và lịch hẹn.

### 3.2. Quản lý Database qua ORM
Chúng ta không viết câu lệnh SQL thuần (`SELECT * FROM...`). Thay vào đó, chúng ta sử dụng các **Python Class** trong `models.py`. 
*   **Ví dụ**: Lệnh `Customer.query.all()` sẽ tự động chuyển thành SQL để lấy toàn bộ khách hàng.
*   Hỗ trợ quan hệ **Relationship**: Một khách hàng có thể có nhiều thú cưng (`One-to-Many`), giúp việc truy xuất dữ liệu liên kết cực kỳ nhanh chóng.

### 3.3. Xử lý Logic (Hybrid Approach)
Dự án được thiết lập theo cơ chế **Hybrid**: Phần lớn xử lý trên Server (SSR) để đảm bảo an toàn dữ liệu, nhưng một số tính năng tương tác cao được xử lý tại trình duyệt (Logic Client) để mang lại cảm giác mượt mà.

### 3.4. Giao diện Tùy biến (Custom UI)
Ứng dụng không dùng Bootstrap hay Tailwind để tránh bị "rập khuôn". Toàn bộ giao diện được thiết kế bằng **Vanilla CSS** (`style.css`) với hệ thống biến (`--root`) giúp dễ dàng thay đổi màu sắc chủ đạo theo thương hiệu PetShop Pro.

## 4. Chiến lược Render: SSR hay CSR?

Ứng dụng của bạn chủ yếu là **SSR (Server-Side Rendering)**, nhưng có những yếu tố **Hybrid** thông minh.

### 4.1. Chủ yếu là SSR (Server-Side Rendering)
Hầu hết các trang như *Danh sách khách hàng*, *Danh sách thú cưng*, *Dashboard*... đều sử dụng SSR.
*   **Cách hoạt động**: Khi bạn bấm vào một Menu, trình duyệt gửi yêu cầu lên Flask Server -> Flask truy vấn Database -> Flask "đúc" dữ liệu vào Template Jinja2 để tạo ra file HTML hoàn chỉnh -> Gửi file HTML đó về trình duyệt để hiển thị ngay lập tức.
*   **Ưu điểm**: Tốc độ hiển thị trang đầu tiên nhanh, bảo mật dữ liệu tốt (vì logic xử lý nằm ở Server), và thân thiện với các công cụ tìm kiếm (SEO).

### 4.2. Kết hợp Client-Side Logic (Trải nghiệm như CSR)
Riêng tại màn hình **Bán hàng (POS)**, chúng ta áp dụng cơ chế giống như CSR (Client-Side Rendering) để tối ưu trải nghiệm:
*   **Cơ chế**: Khi bạn click chọn sản phẩm, JavaScript sẽ tự động tính toán tổng tiền, thêm/bớt hàng trong giỏ ngay tại trình duyệt mà **không cần tải lại trang** (No page reload). 
*   **Tại sao làm vậy?**: Giúp nhân viên bán hàng thao tác cực nhanh, không phải chờ đợi Server phản hồi cho mỗi lần bấm chuột, tạo cảm giác chuyên nghiệp như một phần mềm Desktop.

## 5. Vị trí mã nguồn Giao diện (UI Source Locations)

Để chỉnh sửa hoặc nâng cấp giao diện, bạn có thể tìm thấy các file tương ứng tại các thư mục sau:

### 5.1. Mã nguồn Jinja2 (HTML Templates)
Toàn bộ các file cấu trúc giao diện nằm trong thư mục `app/templates/`.
*   **Base Layout**: `app/templates/base.html` (Chứa Sidebar, Header và khung sườn chung của toàn ứng dụng).
*   **Trang chủ/Dashboard**: `app/templates/dashboard/index.html`.
*   **Module Khách hàng/Thú cưng**: `app/templates/pets/`.
*   **Module Kho hàng**: `app/templates/inventory/`.
*   **Giao diện Bán hàng (POS)**: `app/templates/pos/`.

### 5.2. Mã nguồn Vanilla CSS (Styling)
Các file quy định màu sắc, font chữ và layout nằm trong thư mục `app/static/`.
*   **File CSS chính**: `app/static/css/style.css`.
*   **Lưu ý**: Đây là file CSS thuần (Vanilla CSS). Tất cả các biến màu sắc (Variables) đều được khai báo tại `:root` trong file này để bạn dễ dàng quản lý tông màu của toàn hệ thống (ví dụ: `--primary: #ff7675`).

## 6. Phân biệt Jinja2 và Pug (Comparison with Pug)

Dự án này sử dụng **Jinja2**. Dưới đây là sự khác biệt cơ bản giữa Jinja2 và Pug để bạn dễ dàng nắm bắt:

### 6.1. Khác biệt về triết lý thiết kế
*   **Pug (trước đây là Jade)**: Đi theo hướng **Indentation-based** (dựa vào khoảng lùi đầu dòng). Pug loại bỏ hoàn toàn các thẻ đóng/mở (`<>`, `</>`) và dấu ngoặc, giúp code rất ngắn nhưng cần thời gian để làm quen.
*   **Jinja2**: Đi theo hướng **Enhanced HTML** (HTML tăng cường). File Jinja2 bản chất là một file HTML bình thường, nhưng được bổ sung thêm các "lỗ hổng" để đổ dữ liệu từ Python vào. Nó thân thiện hơn với những người đã biết HTML.

### 6.2. So sánh cú pháp (Syntax Comparison)

| Chức năng | **Pug** (NodeJS) | **Jinja2** (Flask/Python) |
| :--- | :--- | :--- |
| **Thẻ HTML** | `h1 Hello World` | `<h1>Hello World</h1>` |
| **Biến (Variables)** | `p= username` | `<p>{{ username }}</p>` |
| **Vòng lặp (Loops)** | `each item in list` | `{% for item in list %}...{% endfor %}` |
| **Điều kiện (If)** | `if isAdmin` | `{% if isAdmin %}...{% endif %}` |
| **Kế thừa (Layout)** | `extends layout` | `{% extends "base.html" %}` |

### 6.3. 3 Loại ký hiệu cốt lõi trong Jinja2
Trong code của PetShop Pro, bạn chỉ cần nhớ 3 loại dấu ngoặc này:

1.  **`{{ ... }}` (Dùng để in dữ liệu)**:
    *   *Ví dụ*: `{{ pet.name }}` sẽ in tên của thú cưng ra màn hình.
2.  **`{% ... %}` (Dùng cho logic điều khiển)**:
    *   Dùng cho `if`, `for`, `block`, `extends`.
    *   *Ví dụ*: `{% for p in pets %} ... {% endfor %}`.
3.  **`{# ... #}` (Dùng để comment)**:
    *   Các nội dung nằm trong dấu này sẽ bị Server bỏ qua, không hiện ra ngoài trình duyệt.

=> **Tại sao chọn Jinja2 cho dự án này?**
Vì Jinja2 giữ nguyên cấu trúc HTML chuẩn, giúp bạn dễ dàng copy-paste các giao diện hiện đại từ các thư viện CSS hoặc dùng các công cụ thiết kế mà không phải chuyển đổi (convert) sang định dạng thụt lề phức tạp như Pug.
