from django.conf import settings
from django.db import models


class CourseManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query)
        )


class Course(models.Model):
    name = models.CharField(verbose_name='Nome', max_length=100)
    slug = models.SlugField(verbose_name='Atalho')
    description = models.TextField(verbose_name='Descrição Simples', blank=True)
    about = models.TextField(verbose_name="Sobre o Curso", blank=True)
    start_date = models.DateField(verbose_name='Data de Início', null=True, blank=True)
    image = models.ImageField(verbose_name='Imagem', upload_to='courses/images', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

    objects = CourseManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['name']


class Enrollment(models.Model):
    STATUS_CHOICE = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', related_name='enrollments',
                             on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='Curso', related_name='enrollment', on_delete=models.CASCADE)
    status = models.IntegerField(verbose_name='Situação', choices=STATUS_CHOICE, default=0, blank=True)
    created_at = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

    class Meta:
        verbose_name='Inscrição'
        verbose_name_plural='Inscrições'
        unique_together=(('user', 'course'),)
