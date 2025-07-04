from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'



class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


User = get_user_model()

class Clients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    date_of_birth = models.DateField("Дата рождения", null=True, blank=True)
    phone = models.CharField("Телефон", max_length=20, blank=True, null=True)
    email = models.CharField("Электронная почта", max_length=255, blank=True, null=True)
    gender = models.CharField("Пол", max_length=10, choices=[('male', 'Мужской'), ('female', 'Женский')], blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clients'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    def clean(self):
        if self.email and not re.match(r'^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$', self.email):
            raise ValidationError({'email': 'Некорректный формат email'})
        
        if self.phone and not re.match(r'^[0-9]{11}$', self.phone):
            raise ValidationError({'phone': 'Телефон должен содержать 11 цифр'})
        
        if self.date_of_birth:
            from django.utils import timezone
            from datetime import timedelta
            if self.date_of_birth > timezone.now().date():
                raise ValidationError({'date_of_birth': 'Дата рождения не может быть в будущем'})
            if timezone.now().date() - self.date_of_birth < timedelta(days=365*18):
                raise ValidationError({'date_of_birth': 'Клиент должен быть старше 18 лет'})
    
    def save(self, *args, **kwargs):
        self.clean() 
        super().save(*args, **kwargs)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class HotelInTour(models.Model):
    hotel = models.ForeignKey('Hotels', verbose_name="Отель", on_delete=models.DO_NOTHING, blank=True, null=True)
    tour = models.ForeignKey('Tours', verbose_name="Тур", on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hotel_in_tour'
        verbose_name = 'Отель в туре'
        verbose_name_plural = 'Отели в турах'


class Hotels(models.Model):
    name = models.CharField('Название', max_length=255)
    phone = models.CharField('Номер телефона', max_length=20, blank=True, null=True)
    country = models.CharField('Страна', max_length=100, blank=True, null=True)
    city = models.CharField('Город', max_length=255, blank=True, null=True)
    street = models.CharField('Улица', max_length=255, blank=True, null=True)
    house = models.CharField('Дом', max_length=20, blank=True, null=True)
    rating = models.DecimalField('Рейтинг', max_digits=3, decimal_places=2, blank=True, null=True)
    photo = models.ImageField(upload_to="photos/hotels/")

    class Meta:
        managed = False
        db_table = 'hotels'
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'


class Reviews(models.Model):
    text = models.TextField("Текст отзыва", blank=True, null=True)
    client = models.ForeignKey('Clients', verbose_name="Клиент", on_delete=models.DO_NOTHING, blank=True, null=True)
    tour = models.ForeignKey('Tours', verbose_name="Тур", on_delete=models.DO_NOTHING, blank=True, null=True)
    hotel = models.ForeignKey('Hotels', verbose_name="Отель", on_delete=models.DO_NOTHING, blank=True, null=True)
    room = models.ForeignKey('Rooms', verbose_name="Комната", on_delete=models.DO_NOTHING, blank=True, null=True)
    star_count = models.IntegerField("Количество звезд", blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class Service(models.Model):
    SERVICE_TYPES = [
        ('wifi', 'Wi-Fi'),
        ('breakfast', 'Завтрак'),
        ('cleaning', 'Уборка'),
        ('pool', 'Бассейн'),
        ('gym', 'Тренажерный зал'),
        ('spa', 'SPA'),
        ('transfer', 'Трансфер'),
    ]
    
    name = models.CharField("Название услуги", max_length=100)
    service_type = models.CharField("Тип услуги", max_length=50, choices=SERVICE_TYPES)

    class Meta:
        db_table = 'services'
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name


class RoomServices(models.Model):
    room = models.ForeignKey('Rooms', verbose_name="Комната", on_delete=models.CASCADE)
    service = models.ForeignKey('Service', verbose_name="Услуга", on_delete=models.CASCADE)
    included_in_price = models.BooleanField("Включено в стоимость", default=False)
    
    class Meta:
        db_table = 'room_services'
        verbose_name = 'Услуга комнаты'
        verbose_name_plural = 'Услуги комнат'
        unique_together = (('room', 'service'),)


class Rooms(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Забронирована'),
        ('available', 'Свободна'),
    ]
    
    status = models.CharField(
        "Статус",
        max_length=50,
        choices=STATUS_CHOICES,
        default='available',
        blank=True,
        null=True
    )
    room_number = models.CharField("Номер комнаты", max_length=10, blank=True, null=True)
    floor = models.IntegerField("Этаж", blank=True, null=True)
    hotel = models.ForeignKey('Hotels', verbose_name="Отель", on_delete=models.DO_NOTHING, blank=True, null=True)
    bed_count = models.IntegerField("Количество кроватей", blank=True, null=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2, blank=True, null=True)
    photo = models.ImageField(upload_to="photos/hotel/rooms")

    class Meta:
        managed = False
        db_table = 'rooms'
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'


class Tours(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('confirmed', 'Подтвержден'),
        ('canceled', 'Отклонён'),
        ('completed', 'Завершен'),
    ]
    client = models.ForeignKey(
        'Clients', 
        verbose_name="Клиент", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    country = models.CharField("Страна", max_length=100, blank=True, null=True)
    arrival_date = models.DateField("Дата прибытия", blank=True, null=True)
    departure_date = models.DateField("Дата выезда", blank=True, null=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2, blank=True, null=True)
    rating = models.DecimalField("Рейтинг", max_digits=3, decimal_places=2, blank=True, null=True)
    hotel = models.ForeignKey('Hotels', verbose_name="Отель", on_delete=models.DO_NOTHING, blank=True, null=True)
    transport = models.ForeignKey('Transport', verbose_name="Транспорт", on_delete=models.DO_NOTHING, blank=True, null=True)
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
    deleted_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_comment='Статус бронирования'
    )
    class Meta:
        managed = False
        db_table = 'tours'
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'


class Transport(models.Model):
    TRANSPORT_CHOICES = [
        ('bus', 'Автобус'),
        ('plane', 'Самолет'),
        ('train', 'Поезд'),
    ]   
    transport_type = models.CharField("Транспорт", max_length=50, choices=TRANSPORT_CHOICES)
    cost = models.DecimalField("Стоимость", max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transport'
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспорты'

