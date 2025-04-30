from django.db import models


class Agent(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'agent'


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


class Clients(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clients'


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
    hotel = models.ForeignKey('Hotels', models.DO_NOTHING, blank=True, null=True)
    tour = models.ForeignKey('Tours', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hotel_in_tour'


class Hotels(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    number_of_rooms = models.IntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hotels'


class Reviews(models.Model):
    text = models.TextField(blank=True, null=True)
    client = models.ForeignKey(Clients, models.DO_NOTHING, blank=True, null=True)
    tour = models.ForeignKey('Tours', models.DO_NOTHING, blank=True, null=True)
    hotel = models.ForeignKey(Hotels, models.DO_NOTHING, blank=True, null=True)
    room = models.ForeignKey('Rooms', models.DO_NOTHING, blank=True, null=True)
    star_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reviews'


class RoomServices(models.Model):
    room = models.ForeignKey('Rooms', models.DO_NOTHING, blank=True, null=True)
    service_type = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_services'


class Rooms(models.Model):
    status = models.CharField(max_length=50, blank=True, null=True)
    room_number = models.CharField(max_length=10, blank=True, null=True)
    services = models.TextField(blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)
    hotel = models.ForeignKey(Hotels, models.DO_NOTHING, blank=True, null=True)
    bed_count = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rooms'


class Tours(models.Model):
    country = models.CharField(max_length=100, blank=True, null=True)
    arrival_date = models.DateField(blank=True, null=True)
    departure_date = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    hotel = models.ForeignKey(Hotels, models.DO_NOTHING, blank=True, null=True)
    transport = models.ForeignKey('Transport', models.DO_NOTHING, blank=True, null=True)
    agent = models.ForeignKey(Agent, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tours'


class Transport(models.Model):
    type = models.CharField(max_length=50, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transport'


class TransportInTour(models.Model):
    transport = models.ForeignKey(Transport, models.DO_NOTHING, blank=True, null=True)
    tour = models.ForeignKey(Tours, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transport_in_tour'
