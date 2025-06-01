from django.test import TestCase, Client  
from django.contrib.auth.models import User  
from django.urls import reverse  
from datetime import date, timedelta  
  
class BookingTestCase(TestCase):  
    """Тесты функционала бронирования"""  
      
    def setUp(self):  
        # Создаем только пользователя Django (без Clients)  
        self.user = User.objects.create_user(  
            username='testuser',  
            email='test@example.com',  
            password='testpass123'  
        )  
        self.client = Client()  
      
    def test_user_authentication(self):  
        """Тест аутентификации пользователя"""  
        self.assertTrue(self.user.is_authenticated)  
        self.assertEqual(self.user.username, 'testuser')  
        self.assertEqual(self.user.email, 'test@example.com')  
      
    def test_login_functionality(self):  
        """Тест функции входа"""  
        login_successful = self.client.login(username='testuser', password='testpass123')  
        self.assertTrue(login_successful)  
      
    def test_booking_requires_authentication(self):  
        """Тест требования авторизации для бронирования"""  
        # Попытка доступа без авторизации  
        response = self.client.get('/createtour/hotels/')  
        self.assertEqual(response.status_code, 302)  # Редирект на логин  
      
    def test_authenticated_access_to_hotels(self):  
        """Тест доступа к отелям для авторизованного пользователя"""  
        self.client.login(username='testuser', password='testpass123')  
        response = self.client.get('/createtour/hotels/')  
        # Проверяем, что нет редиректа на логин  
        self.assertNotEqual(response.status_code, 302)  
      
    def test_booking_view_requires_room_id(self):  
        """Тест требования room_id для бронирования"""  
        self.client.login(username='testuser', password='testpass123')  
        # Попытка доступа к несуществующей комнате  
        response = self.client.get('/order/create/99999/')  
        self.assertEqual(response.status_code, 404)  
      
    def test_user_profile_data(self):  
        """Тест данных профиля пользователя"""  
        self.assertEqual(self.user.first_name, '')  
        self.assertEqual(self.user.last_name, '')  
        # Можно установить данные  
        self.user.first_name = 'Тест'  
        self.user.last_name = 'Пользователь'  
        self.user.save()  
        self.user.refresh_from_db()  
        self.assertEqual(self.user.first_name, 'Тест')  
        self.assertEqual(self.user.last_name, 'Пользователь')  
      
    def test_password_validation(self):  
        """Тест валидации пароля"""  
        # Проверяем правильный пароль  
        self.assertTrue(self.user.check_password('testpass123'))  
        # Проверяем неправильный пароль  
        self.assertFalse(self.user.check_password('wrongpassword'))