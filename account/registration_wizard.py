# python imports
from django.contrib.formtools.wizard.views import NamedUrlSessionWizardView
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.decorators import classonlymethod
from registration.models import RegistrationProfile
from registration.signals import user_registered
from registration.forms import RegistrationFormUniqueEmail, RegistrationFormTermsOfService
from django.db.transaction import atomic

# Project imports
from recruiter.models import Profiles
from account.constants import JOB_SEEKER, RECRUITER


class RegistrationWizard(NamedUrlSessionWizardView):

    @classonlymethod
    def as_view(self, *args, **kwargs):
        form_list = (
            ('user', RegistrationFormUniqueEmail),
        )
        return super(RegistrationWizard, self).as_view(form_list, *args, **kwargs)

    #@property
    def profile(self, user_role):
        return Profiles.profile(user_role)

    def get_step_url(self, step):
        kwargs = {'step': step}
        if 'profile' in self.kwargs and self.kwargs.get('profile', JOB_SEEKER):
            self.kwargs.update({'profile': self.kwargs['profile']})
        return reverse(self.url_name, kwargs=kwargs)

    def get_context_data(self, form, **kwargs):
        form.initial = {'user_role': self.kwargs.get('profile', JOB_SEEKER)}
        context = super(RegistrationWizard, self).get_context_data(form=form, **kwargs)
        return context

    def get_template_names(self):
        name = 'registration/%s.html' % self.steps.current
        return [name]

    #@atomic
    def done(self, form_list, **kwargs):
        cd = form_list[self.get_step_index('user')].cleaned_data
        email, password = cd['email'], cd['password1']
        site = Site.objects.get_current()

        new_user = RegistrationProfile.objects.create_inactive_user(email, password, site)

        profile = self.profile(cd['user_role'])(user=new_user)
        profile.gender = cd['gender']
        profile.save()

        return redirect('registration_complete')


registration_wizard = RegistrationWizard.as_view(
    url_name='registration_register',
    done_step_name='finished'
)


def registration_complete(request):
    return render(request, 'registration/registration_complete.html')
