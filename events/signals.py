from django.dispatch import receiver
from django.db.models.signals import post_save,m2m_changed
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from events.models import Event


@receiver(post_save, sender=User)
def send_email_activation(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/event/activate/{instance.id}/{token}"

        subject = "Activate Your Account"
        message = f"Hi {instance.first_name} {instance.last_name}\n\nPlease activate your account by clicking link below:\n{activation_url}\n\nThank You"
        email_list = [instance.email]

        try:
            send_mail(subject, message, "nazmulislamfsd@gmail.com", email_list)
        except Exception as error:
            print(f"Failed send to email {instance.email}: {str(error)}")


@receiver(post_save, sender=User)
def assigne_role(sender, instance, created, **kwargs):
    if created:
        user_group = Group.objects.get(name="Participant")
        instance.groups.add(user_group)
        instance.save()


@receiver(m2m_changed, sender=Event.participants.through)
def send_rsvp_email(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":

        for user_id in pk_set:
            
            try:
                user = User.objects.get(id=user_id)
                
                subject = f"Rsvp Confirmation for {instance.name}"
                message = (f"Hello {user.first_name}\n\nYou have successfully Rsvp to the event: {instance.name}.\n\nDate: {instance.date}\nTime: {instance.time}\nLocation: {instance.location}\n\nThank you for your interest")

                send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

            except User.DoesNotExist:
                continue