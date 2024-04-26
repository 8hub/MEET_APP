from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserAccountTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.STRONG_PASSWORD = 'ter33fsRRwSd12#'
        cls.WEAK_PASSWORD = 'password'
        cls.GOOD_EMAIL = 'newuser@example.com'
        cls.BAD_EMAIL = 'test@com'
        
    def setUp(self):
        self.client = APIClient()   # test client
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password=self.STRONG_PASSWORD)
        self.refresh = RefreshToken.for_user(self.user) # jwt token

    def test_register_user(self):
        url = reverse('UsersApp:register')
        data = {'username': 'newuser', 'email': self.GOOD_EMAIL, 'password': self.STRONG_PASSWORD}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
    
    def test_register_same_email(self):
        url = reverse('UsersApp:register')
        data = {'username': 'newuser', 'email': self.GOOD_EMAIL, 'password': self.STRONG_PASSWORD}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('UsersApp:register')
        data = {'username': 'testuser', 'email': self.GOOD_EMAIL, 'password': self.STRONG_PASSWORD}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_same_username(self):
        url = reverse('UsersApp:register')
        data = {'username': 'newuser', 'email': self.GOOD_EMAIL, 'password': self.STRONG_PASSWORD}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('UsersApp:register')
        data = {'username': 'newuser', 'email': 'email@example.com', 'password': self.STRONG_PASSWORD}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_password(self):
        url = reverse('UsersApp:register')
        data = {'username': 'newuser', 'email': self.GOOD_EMAIL, 'password': self.WEAK_PASSWORD}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_bad_email(self):
        url = reverse('UsersApp:register')
        data = {'username': 'newuser', 'email': self.BAD_EMAIL, 'password': self.STRONG_PASSWORD}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def test_login_user(self):
        url = reverse('UsersApp:login')
        data = {'username': 'testuser', 'password': self.STRONG_PASSWORD}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_logout_user(self):
        url = reverse('UsersApp:logout')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        data = {'refresh': str(self.refresh)}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_user_detail(self):
        url = reverse('UsersApp:user_detail')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_user_detail_unauthorized(self):
        url = reverse('UsersApp:user_detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_detail_bad_token(self):
        url = reverse('UsersApp:user_detail')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}bad')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
