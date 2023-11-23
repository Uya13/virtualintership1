from django.db import models
from django.core.cache import cache


class Users(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=128, verbose_name='Полное имя')
    phone = models.IntegerField(unique=True, verbose_name='Телефон')


class Coords(models.Model):
    latitude = models.FloatField(max_length=20, verbose_name='Широта')
    longitude = models.FloatField(max_length=20, verbose_name='Долгота')
    height = models.IntegerField(verbose_name='Высота')

    def str(self):
        return f'Широта - {self.latitude}, долгота - {self.longitude}, высота - {self.height}'


class Level(models.Model):
    LEVEL = [
        ('1b', '1Б'),
        ('2a', '2А'),
        ('2b', '2Б'),
        ('3a', '3А'),
        ('3b', '3Б'),
        ('4a', '4А'),
        ('4b', '4Б'),
        ('5a', '5А'),
        ('5b', '5Б'),
        ('6a', '6А'),
        ('6b', '6Б')
    ]

    winter = models.CharField(max_length=2, choices=LEVEL, verbose_name='Зима')
    summer = models.CharField(max_length=2, choices=LEVEL, verbose_name='Лето')
    autumn = models.CharField(max_length=2, choices=LEVEL, verbose_name='Осень')
    spring = models.CharField(max_length=2, choices=LEVEL, verbose_name='Весна')

    def str(self):
        return f'Уровень сложности перевала в зимнее время - {self.winter}, в летнее - {self.summer}, ' \
               f'в осеннее - {self.autumn}, в весеннее - {self.spring}'


class Perevals(models.Model):
    new = 'NW'
    pending = 'PN'
    accepted = 'AC'
    rejected = 'RJ'

    CHOICES = [
        (new, 'Новый'),
        (pending, 'Принято в работу'),
        (accepted, 'Успешно'),
        (rejected, 'Отклонено')
    ]

    beautyTitle = models.CharField(max_length=200, verbose_name='Общее название')
    title = models.CharField(max_length=200, verbose_name='Название перевала')
    other_titles = models.CharField(max_length=200)
    connect = models.CharField(max_length=200)
    status = models.CharField(max_length=2, choices=CHOICES, default=new)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    level_id = models.ForeignKey(Level, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    coord_id = models.OneToOneField(Coords, on_delete=models.CASCADE)

    def str(self):
        return f'Это перевал №{self.pk} под названием "{self.beautyTitle}"'


class PerevalAreas(models.Model):
    title = models.CharField(max_length=128, verbose_name='Название горы')


class Images(models.Model):
    title = models.CharField(max_length=128, verbose_name='Название изображения')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    image = models.ImageField(verbose_name='Изображение', upload_to='images')

    pereval_id = models.ForeignKey(Perevals, on_delete=models.CASCADE)


class PerevalImages(models.Model):
    pereval_id = models.ForeignKey(Perevals, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Images, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'image-{self.pk}')


class SprActivitiesTypes(models.Model):
    mountaining = 'MN'
    hiking = 'HK'
    skiing = 'SK'
    biking = 'BK'
    mountain_hiking = 'MH'
    TYPE = [
        (mountaining, 'Горный'),
        (hiking, 'Пеший'),
        (skiing, 'Лыжный'),
        (biking, 'Велосипедный'),
        (mountain_hiking, 'Горно-пеший')
    ]

    title = models.CharField(max_length=128, choices=TYPE, verbose_name='Тип похода')