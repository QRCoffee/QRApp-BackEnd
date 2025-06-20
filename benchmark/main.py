from locust import HttpUser, between, task


class AuthUser(HttpUser):
    wait_time = between(1, 3)  # Đợi 1-3 giây giữa các request

    def on_start(self):
        # Khởi tạo dữ liệu test
        self.test_users = [
            {"username": "admin", "password": "admin"},
            {"username": "test1", "password": "test123"},
            {"username": "test2", "password": "test123"},
            # Thêm nhiều test user khác nếu cần
        ]

    @task(1)
    def sign_in(self):
        # Random chọn một user để test
        import random
        user = random.choice(self.test_users)
        
        # Headers
        headers = {
            "Content-Type": "application/json"
        }

        # Gọi API sign-in
        with self.client.post(
            "/sign-in",
            json=user,
            headers=headers,
            name="Sign In",
            catch_response=True
        ) as response:
            # Kiểm tra response
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Sign-in failed: {response.status_code}")