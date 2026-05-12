# Sơ đồ Thực thể Mối quan hệ (ERD) - Pet Shop Management

Sơ đồ dưới đây mô tả cấu trúc cơ sở dữ liệu của hệ thống, bao gồm các bảng, các trường thông tin và mối liên kết giữa chúng. Cấu trúc đã được làm sạch và sắp xếp logic theo luồng chức năng.

```plantuml
@startuml
hide circle
skinparam linetype ortho
skinparam nodesep 100
skinparam ranksep 100

skinparam entity {
  BackgroundColor #FFFDE7
  BorderColor #F9A825
  FontSize 12
}
skinparam arrow {
  Color #555555
  FontSize 11
}

' --- Entities ---

entity "**users**\n(Người dùng)" as users {
  * id : INT <<PK>>
  --
  customer_id : INT <<FK>>
  username : VARCHAR(64)
  role : VARCHAR(20)
  full_name : VARCHAR(100)
  is_active : BOOLEAN
}

entity "**customers**\n(Khách hàng)" as customers {
  * id : INT <<PK>>
  --
  name : VARCHAR(100)
  phone : VARCHAR(20)
  tier : VARCHAR(20)
  total_spent : FLOAT
}

entity "**pets**\n(Thú cưng)" as pets {
  * id : INT <<PK>>
  --
  customer_id : INT <<FK>>
  name : VARCHAR(100)
  species : VARCHAR(50)
}

entity "**bookings**\n(Lịch hẹn)" as bookings {
  * id : INT <<PK>>
  --
  customer_id : INT <<FK>>
  pet_id : INT <<FK>>
  service_id : INT <<FK>>
  status : VARCHAR(20)
  is_paid : BOOLEAN
}

entity "**orders**\n(Hóa đơn POS)" as orders {
  * id : INT <<PK>>
  --
  customer_id : INT <<FK>>
  user_id : INT <<FK>>
  total_amount : FLOAT
  payment_method : VARCHAR(50)
}

entity "**order_items**\n(Chi tiết hóa đơn)" as order_items {
  * id : INT <<PK>>
  --
  order_id : INT <<FK>>
  product_id : INT <<FK>>
  service_id : INT <<FK>>
  quantity : INT
  price : FLOAT
}

entity "**services**\n(Dịch vụ Pet)" as services {
  * id : INT <<PK>>
  --
  category_id : INT <<FK>>
  name : VARCHAR(150)
  price : FLOAT
}

entity "**service_categories**\n(Danh mục DV)" as service_categories {
  * id : INT <<PK>>
  --
  name : VARCHAR(100)
}

entity "**products**\n(Sản phẩm)" as products {
  * id : INT <<PK>>
  --
  category_id : INT <<FK>>
  name : VARCHAR(150)
  price : FLOAT
}

entity "**categories**\n(Danh mục SP)" as categories {
  * id : INT <<PK>>
  --
  name : VARCHAR(100)
}

entity "**vouchers**\n(Mã giảm giá)" as vouchers {
  * id : INT <<PK>>
  --
  code : VARCHAR(50)
  discount_amount : FLOAT
}

' --- Relationships & Layout ---

' Hàng ngang trên cùng
users "1" ||-right-o| "0..1" customers : "liên kết"
customers "1" ||-right-o{ "0..*" pets : "sở hữu"

' Luồng dọc chính
users "1" ||-down-o{ "0..*" orders : "nhân viên lập"
customers "1" ||-down-o{ "0..*" bookings : "đặt lịch"

' Xung quanh Bookings
pets "1" ||-down-o{ "0..*" bookings : "được phục vụ"
services "1" ||-up-o{ "0..*" bookings : "sử dụng"
users "1" ||--o{ "0..*" bookings : "thực hiện"

' Xung quanh Orders
vouchers "0..1" |o-right-o{ "0..*" orders : "áp dụng"
customers "1" ||--o{ "0..*" orders : "thanh toán"

' Xuống dòng từ Orders
orders "1" ||-down-o{ "1..*" order_items : "có dòng hàng"

' Các liên kết từ Order Items
order_items "0..*" }o-right-o| "0..1" services : "mua DV"
order_items "0..*" }o-down-o| "0..1" products : "mua SP"

' Categories
categories "1" ||-right-o{ "0..*" products : "phân loại"
service_categories "1" ||-up-o{ "0..*" services : "phân loại"

@enduml
```

## Giải thích các bảng chính:

1.  **users**: Lưu trữ thông tin tài khoản đăng nhập và phân quyền (Admin, Nhân viên, Khách).
2.  **customers & pets**: Quản lý thông tin chủ sở hữu và thú cưng. Có mối quan hệ 1-nhiều.
3.  **products & services**: Danh mục các mặt hàng và dịch vụ mà cửa hàng cung cấp.
4.  **bookings**: Quản lý lịch hẹn chăm sóc thú cưng, kết nối khách hàng, thú cưng và dịch vụ.
5.  **orders & order_items**: Lưu trữ lịch sử giao dịch bán hàng và sử dụng dịch vụ tại quầy (POS).

