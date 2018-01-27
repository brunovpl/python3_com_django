from django.conf import settings
from django.db import models

from simplemooc.core.email import send_mail_template


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

    @models.permalink
    def get_absolute_url(self):
        return 'courses:details', (), {'slug': self.slug}


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

    def active(self):
        self.status = 1
        self.save()

    def is_approved(self):
        return self.status == 1

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user', 'course'),)


class Announcements(models.Model):
    course = models.ForeignKey(Course, verbose_name='Curso', on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(verbose_name='Título', max_length=100)
    content = models.TextField(verbose_name='Conteúdo')
    created_at = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-created_at']


class Comment(models.Model):
    announcement = models.ForeignKey(Announcements, verbose_name='Anúncios', related_name='comments',
                                     on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='Comentário')

    created_at = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']


def post_save_announcement(instance, created, **kwargs):
    if created:
        subject = instance.title
        context = {
            'announcement': instance,

        }
        template_name = 'courses/announcement_mail.html'
        enrollments = Enrollment.objects.filter(course=instance.course, status=1)
        for enrollment in enrollments:
            recipient_list = [enrollment.user.email]
            send_mail_template(subject=subject, template_name=template_name, context=context,
                               recipient_list=recipient_list)


models.signals.post_save.connect(post_save_announcement, sender=Announcements, dispatch_uid='post_save_announcement')


class Lesson(models.Model):
    name = models.CharField(verbose_name='Nome', max_length=100)
    description = models.TextField(verbose_name='Descrição', blank=True)
    number = models.IntegerField(verbose_name='Número (ordem)', blank=True, default=0)
    release_date = models.DateField(verbose_name='Data da Liberação', blank=True, null=True)

    course = models.ForeignKey(to=Course, verbose_name='Curso', related_name='lessons', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']


class Material(models.Model):
    name = models.CharField(verbose_name='Nome', max_length=100)
    embedded = models.TextField(verbose_name='Vídeo embedded', blank=True)
    file = models.FileField(upload_to='lessons/materials', blank=True, null=True)
    
    lesson = models.ForeignKey(to=Lesson, verbose_name='Aula', related_name='materials', on_delete=models.CASCADE)

    def is_embedded(self):
        return bool(self.embedded)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'
