from django.db import models
from django.contrib.auth import get_user_model


class Agent(models.Model):
    name = models.CharField("Имя", max_length=255)
    email = models.CharField("Электронная почта", unique=True, max_length=255)
    phone = models.CharField("Телефон", max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'agent'
        verbose_name = 'Туроператор'
        verbose_name_plural = 'Туроператоры'

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
    name = models.CharField('Название',max_length=255)
    phone = models.CharField('Номер телефона',max_length=20, blank=True, null=True)
    country = models.CharField('Страна',max_length=100, blank=True, null=True)
    address = models.TextField('Адрес',blank=True, null=True)
    rating = models.DecimalField('Рейтинг',max_digits=3, decimal_places=2, blank=True, null=True)
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


class RoomServices(models.Model):
    room = models.ForeignKey('Rooms', verbose_name="Комната", on_delete=models.DO_NOTHING, blank=True, null=True)
    service_type = models.CharField("Тип услуги", max_length=50, blank=True, null=True)
    description = models.TextField("Описание", blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_services'
        verbose_name = 'Услуга комнаты'
        verbose_name_plural = 'Услуги комнат'


class Rooms(models.Model):
    status = models.CharField("Статус", max_length=50, blank=True, null=True)
    room_number = models.CharField("Номер комнаты", max_length=10, blank=True, null=True)
    services = models.TextField("Услуги", blank=True, null=True)
    floor = models.IntegerField("Этаж", blank=True, null=True)
    hotel = models.ForeignKey('Hotels', verbose_name="Отель", on_delete=models.DO_NOTHING, blank=True, null=True)
    bed_count = models.IntegerField("Количество кроватей", blank=True, null=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rooms'
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'


class Tours(models.Model):
    country = models.CharField("Страна", max_length=100, blank=True, null=True)
    arrival_date = models.DateField("Дата прибытия", blank=True, null=True)
    departure_date = models.DateField("Дата выезда", blank=True, null=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField("Статус", max_length=50, blank=True, null=True)
    rating = models.DecimalField("Рейтинг", max_digits=3, decimal_places=2, blank=True, null=True)
    hotel = models.ForeignKey('Hotels', verbose_name="Отель", on_delete=models.DO_NOTHING, blank=True, null=True)
    transport = models.ForeignKey('Transport', verbose_name="Транспорт", on_delete=models.DO_NOTHING, blank=True, null=True)
    agent = models.ForeignKey('Agent', verbose_name="Агент", on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tours'
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'


class Transport(models.Model):
    type = models.CharField("Тип транспорта", max_length=50, blank=True, null=True)
    cost = models.DecimalField("Стоимость", max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transport'
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспорты'


class TransportInTour(models.Model):
    transport = models.ForeignKey('Transport', verbose_name="Транспорт", on_delete=models.DO_NOTHING, blank=True, null=True)
    tour = models.ForeignKey('Tours', verbose_name="Тур", on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transport_in_tour'
        verbose_name = 'Транспорт в туре'
        verbose_name_plural = 'Транспорты в туре'