from enum import Enum


class UserRole(str, Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    STAFF = "Staff"

class APIError(str, Enum):
    # Auth related errors
    UNAUTHORIZED = "Unauthorized"  # Chưa xác thực hoặc không có quyền truy cập
    INVALID_TOKEN = "InvalidToken"  # Token không hợp lệ hoặc sai định dạng
    SESSION_INVALID = "SessionInvalid"  # Phiên đăng nhập không tồn tại
    SESSION_EXPIRED = "SessionExpired"  # Phiên đăng nhập đã hết hạn
    TOKEN_EXPIRED = "TokenExpired"  # Token đã hết hạn
    INVALID_REFRESH_TOKEN = "InvalidRefreshToken"  # Refresh token không hợp lệ
    TOKEN_BLACKLISTED = "TokenBlacklisted"  # Token đã bị đưa vào blacklist
    TOKEN_REVOKED = "TokenRevoked"  # Token đã bị thu hồi
    
    # Permission related errors 
    PERMISSION_DENIED = "PermissionDenied"  # Không có quyền truy cập tài nguyên
    INSUFFICIENT_ROLE = "InsufficientRole"  # Vai trò không đủ quyền thực hiện
    ROLE_NOT_FOUND = "RoleNotFound"  # Không tìm thấy vai trò
    
    # User related errors
    USER_NOT_FOUND = "UserNotFound"  # Không tìm thấy người dùng
    INVALID_CREDENTIALS = "InvalidCredentials"  # Thông tin đăng nhập không chính xác
    USER_ALREADY_EXISTS = "UserAlreadyExists"  # Username đã tồn tại
    USER_INACTIVE = "UserInactive"  # Tài khoản bị vô hiệu hóa
    PASSWORD_MISMATCH = "PasswordMismatch"  # Mật khẩu không khớp khi đổi mật khẩu
    PASSWORD_TOO_WEAK = "PasswordTooWeak"  # Mật khẩu quá yếu
    ACCOUNT_LOCKED = "AccountLocked"  # Tài khoản bị khóa do đăng nhập sai nhiều lần
    ACCOUNT_DISABLED = "AccountDisabled"  # Tài khoản bị vô hiệu hóa bởi admin
    
    # Data validation errors
    VALIDATION_ERROR = "ValidationError"  # Lỗi validate dữ liệu đầu vào
    INVALID_FORMAT = "InvalidFormat"  # Định dạng dữ liệu không hợp lệ
    REQUIRED_FIELD = "RequiredField"  # Thiếu trường bắt buộc
    INVALID_LENGTH = "InvalidLength"  # Độ dài không hợp lệ
    INVALID_VALUE = "InvalidValue"  # Giá trị không hợp lệ
    INVALID_DATE = "InvalidDate"  # Ngày không hợp lệ
    INVALID_RANGE = "InvalidRange"  # Giá trị nằm ngoài phạm vi cho phép
    
    # Resource errors
    RESOURCE_NOT_FOUND = "ResourceNotFound"  # Không tìm thấy tài nguyên
    RESOURCE_CONFLICT = "ResourceConflict"  # Xung đột tài nguyên
    RESOURCE_LOCKED = "ResourceLocked"  # Tài nguyên đang bị khóa/sử dụng
    RESOURCE_EXPIRED = "ResourceExpired"  # Tài nguyên đã hết hạn
    RESOURCE_LIMIT_EXCEEDED = "ResourceLimitExceeded"  # Vượt quá giới hạn tài nguyên
    
    # Database errors
    DATABASE_ERROR = "DatabaseError"  # Lỗi thao tác với database
    CONNECTION_ERROR = "ConnectionError"  # Lỗi kết nối database/redis
    DUPLICATE_ENTRY = "DuplicateEntry"  # Dữ liệu trùng lặp (unique constraint)
    FOREIGN_KEY_VIOLATION = "ForeignKeyViolation"  # Vi phạm khóa ngoại
    TRANSACTION_ERROR = "TransactionError"  # Lỗi trong quá trình transaction
    DEADLOCK_ERROR = "DeadlockError"  # Xảy ra deadlock trong database
    
    # File related errors
    FILE_NOT_FOUND = "FileNotFound"  # Không tìm thấy file
    FILE_TOO_LARGE = "FileTooLarge"  # File quá lớn
    INVALID_FILE_TYPE = "InvalidFileType"  # Loại file không hợp lệ
    FILE_UPLOAD_ERROR = "FileUploadError"  # Lỗi upload file
    FILE_DOWNLOAD_ERROR = "FileDownloadError"  # Lỗi download file
    
    # Rate limiting errors
    TOO_MANY_REQUESTS = "TooManyRequests"  # Quá nhiều request trong thời gian ngắn
    RATE_LIMIT_EXCEEDED = "RateLimitExceeded"  # Vượt quá giới hạn request
    IP_BLOCKED = "IpBlocked"  # IP bị chặn do vi phạm rate limit
    
    # External service errors
    SERVICE_ERROR = "ServiceError"  # Lỗi từ service bên ngoài
    TIMEOUT_ERROR = "TimeoutError"  # Quá thời gian chờ phản hồi
    INTEGRATION_ERROR = "IntegrationError"  # Lỗi tích hợp với service khác
    
    # Generic errors
    BAD_REQUEST = "BadRequest"  # Request không hợp lệ
    NOT_FOUND = "NotFound"  # Không tìm thấy endpoint/resource
    SERVER_ERROR = "InternalError"  # Lỗi server không xác định
    SERVICE_UNAVAILABLE = "ServiceUnavailable"  # Dịch vụ tạm thời không khả dụng
    MAINTENANCE_MODE = "MaintenanceMode"  # Hệ thống đang bảo trì
    METHOD_NOT_ALLOWED = "MethodNotAllowed"  # Phương thức không được phép
    CONFLICT = "Conflict"  # Xung đột dữ liệu
    PRECONDITION_FAILED = "PreconditionFailed"  # Điều kiện tiên quyết không thỏa mãn
    
class APIMessage(str, Enum):
    # Generic request messages
    SUCCESS = "Thành công"
    # Auth related messages
    USERNAME_CONFLIC = "username đã được sử dụng"
    PHONE_CONFLIC = "Số điện thoại đã được sử dụng"
    UNAUTHORIZED = "Đăng nhập để sử dụng"
    INVALID_CREDENTIALS = "Tên đăng nhập hoặc mật khẩu không chính xác"
    INVALID_TOKEN = "Token không hợp lệ"
    SESSION_EXPIRED = "Session không hợp lệ"
    PERMISSION_DENIED = "Không đủ quyền"
    SERVER_ERROR = "Đã có lỗi xảy ra, vui lòng thử lại sau"

class PermissionCode(Enum):
    """System Permissions Enumeration
    Format:
    - 1xx: Restaurant permissions
    - 2xx: Area permissions
    - 3xx: Table permissions
    - 4xx: User/Staff permissions
    """

    # Restaurant Permissions (1xx)
    CREATE_RESTAURANT = (101, "Tạo nhà hàng mới")
    UPDATE_RESTAURANT = (102, "Cập nhật thông tin nhà hàng")
    DELETE_RESTAURANT = (103, "Xóa nhà hàng")
    VIEW_RESTAURANT   = (104, "Xem thông tin nhà hàng")

    # Area Permissions (2xx)
    CREATE_AREA = (201, "Tạo khu vực mới")
    UPDATE_AREA = (202, "Cập nhật thông tin khu vực")
    DELETE_AREA = (203, "Xóa khu vực")
    VIEW_AREA   = (204, "Xem thông tin khu vực")

    # Table Permissions (3xx)
    CREATE_TABLE = (301, "Tạo bàn mới")
    UPDATE_TABLE = (302, "Cập nhật thông tin bàn")
    DELETE_TABLE = (303, "Xóa bàn")
    VIEW_TABLE   = (304, "Xem thông tin bàn")

    # Staff Permissions (4xx)
    CREATE_STAFF = (401, "Tạo tài khoản nhân viên")
    UPDATE_STAFF = (402, "Cập nhật thông tin nhân viên")
    DELETE_STAFF = (403, "Xóa tài khoản nhân viên")
    VIEW_STAFF   = (404, "Xem thông tin nhân viên")

    # Admin/User Permissions (5xx)
    CREATE_USER = (501, "Tạo người dùng mới")
    UPDATE_USER = (502, "Cập nhật thông tin người dùng")
    DELETE_USER = (503, "Xóa tải khoản người dùng")
    VIEW_USER = (504, "Xem thông tin người dùng")
    
    CREATE_ADMIN_USER = (505, "Tạo quản trị mới")
    DELETE_ADMIN_USER = (506, "Xóa tải khoản quản trị")
    UPDATE_ADMIN_USER = (507, "Cập nhật thông tin quản trị")
    VIEW_ADMIN_USER = (508, "Xem thông tin người dùng")


    # Permission (6xx)
    CREATE_PERMISSION = (601, "Tạo quyền hạn mới")
    UPDATE_PERMISSION = (602, "Cập nhật thông tin quyền hạn")
    DELETE_PERMISSION = (603, "Xóa quyền hạn")
    VIEW_PERMISSION = (604, "Xem quyền hạn")

    def __init__(self, code: int, description: str):
        self._code = code
        self._description = description

    @property
    def code(self) -> int:
        return self._code

    @property
    def description(self) -> str:
        return self._description
    
    @classmethod
    def get_permissions_by_role(cls, role: UserRole) -> list["PermissionCode"]:
        if role == UserRole.ADMIN:
            return [
                # Restaurant full access
                cls.CREATE_RESTAURANT.code,
                cls.UPDATE_RESTAURANT.code,
                cls.DELETE_RESTAURANT.code,
                cls.VIEW_RESTAURANT.code,
                # User full access
                cls.CREATE_USER.code,
                cls.UPDATE_USER.code,
                cls.DELETE_USER.code,
                cls.VIEW_USER.code,
                # Admin full access
                cls.CREATE_ADMIN_USER.code,
                cls.DELETE_ADMIN_USER.code,
                cls.UPDATE_ADMIN_USER.code,
                cls.VIEW_ADMIN_USER.code,
            ]
        if role == UserRole.MANAGER:
            return [
                # Restaurant limited access
                cls.UPDATE_RESTAURANT.code,
                cls.VIEW_RESTAURANT.code,
                # Area full access
                cls.CREATE_AREA.code,
                cls.UPDATE_AREA.code,
                cls.DELETE_AREA.code,
                cls.VIEW_AREA.code,
                # Table full access
                cls.CREATE_TABLE.code,
                cls.UPDATE_TABLE.code,
                cls.DELETE_TABLE.code,
                cls.VIEW_TABLE.code,
                # Staff full access
                cls.CREATE_STAFF.code,
                cls.UPDATE_STAFF.code,
                cls.DELETE_STAFF.code,
                cls.VIEW_STAFF.code,
            ]
        if role == UserRole.STAFF:
            return []  # No permissions yet
        return []  # Return empty list for unknown roles