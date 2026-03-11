# URL-ы эндпоинтов
BASE_URL = "https://stellarburgers.education-services.ru"

# Эндпоинты
ENDPOINT_REGISTER = f"{BASE_URL}/api/auth/register"
ENDPOINT_LOGIN = f"{BASE_URL}/api/auth/login"
ENDPOINT_USER = f"{BASE_URL}/api/auth/user"
ENDPOINT_ORDERS = f"{BASE_URL}/api/orders"
ENDPOINT_INGREDIENTS = f"{BASE_URL}/api/ingredients"

# Сообщения об ошибках
MSG_USER_EXISTS = "User already exists"
MSG_REQUIRED_FIELDS = "Email, password and name are required fields"
MSG_INVALID_CREDENTIALS = "email or password are incorrect"
MSG_UNAUTHORIZED = "You should be authorised"
MSG_EMAIL_EXISTS = "User with such email already exists"
MSG_NO_INGREDIENTS = "Ingredient ids must be provided"