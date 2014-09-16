# This whole file is taken from https://code.djangoproject.com/ticket/18830
import logging
import inspect

from django import forms
from django.forms.formsets import BaseFormSet
from django.utils.datastructures import SortedDict, MultiValueDict
from django.utils.encoding import StrAndUnicode
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)


class FormContainerMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # logger.debug('%s; attrs = %s' % (whoami(), attrs))
        #
        # Opportunities to land here are: imports of below FormContainer,
        # and its descendant classes.
        #
        # The __new__ signature is the tutorial one for metaclasses
        #   name - name of the class to be created: FormContainer, SubscriberForm.
        #   bases - its base classes: (StrAndUnicode,), (FormContainer,)
        #   attrs - dictionary of the new class attributes, among them its declared
        #       members and methods. For FormContainer, keys become as in usual
        #       __dict__ with neither members nor methods from new class declaration:
        #       '__metaclass__',  '__getitem__', ...
        #       For SubscriberForm, members and methods also appear:
        #         'user': <class 'django.forms.models.UserForm'>,
        #         'server_info': 'server_info': <class 'django.forms.models.FileServersInfoForm'>,
        #         'subscriber': <class 'django.forms.formsets.SubscriberFormFormSet'>,
        #       'subscriber', , 'user': 'broker_credentials'
        #
        form_classes = SortedDict(
            (prefix, attrs.pop(prefix))
            for prefix, form_class in attrs.items()
            if isinstance(form_class, type) and issubclass(form_class, (forms.BaseForm, BaseFormSet))
        )

        #
        # Interested in the dictionary 'attrs' values that happen to inherit from
        # BaseForm or BaseFormSet. This will be empty for FormContainer, for SubscriberForm
        # it contains by-us defined friends - guess? - 'server_info, 'subscriber', 'user',
        # 'broker_credentials'
        #
        new_class = super(FormContainerMetaclass, cls).__new__(cls, name, bases, attrs)

        new_class.form_classes = form_classes

        # Making the form container look like a form, for the
        # sake of the FormWizard.
        new_class.base_fields = {}
        for prefix, form_class in new_class.form_classes.items():
            if issubclass(form_class, BaseFormSet):
                new_class.base_fields.update(form_class.form.base_fields)
            else:
                new_class.base_fields.update(form_class.base_fields)
        #
        # A Django form has base_fields. To make the new class being more like form,
        # compose its base_fields from fields of above collected from its members,
        # forms and formsets. Empty for FormContainer that declares nothing of the sort,
        # for SubscriberForm, collected fields of them all: 'signal_transmission', 'city',
        # 'code', 'address', 'username', 'user', 'client_platform', 'file_servers',
        # 'password', 'email', 'avatar'.
        #

        #
        # The metaclass job was to detect form and formset members of the new class,
        # store them in class member form_fields, and make the new class look
        # form-like by collecting all members' form fields into its base_field.
        #
        return new_class


class FormContainer(StrAndUnicode):
    __metaclass__ = FormContainerMetaclass

    def __init__(self, **kwargs):
        #
        # Make self.forms from the metaclass-added self.form_classes
        # and from instances determined by self.get_form_kwargs
        #
        # When SubscriberForm is inheriting, **kwargs are determined by Django and are
        # {'files': None, 'prefix': 'subscriber', 'initial': {}, 'data': None}
        #
        self._errors = {}
        self.forms = SortedDict()
        container_prefix = kwargs.pop('prefix', '')

        #
        # In self.form_classes dictionary, there are members declared as
        # form or formset classes in descendant class.
        # When SubscriberForm derives from us, these will be
        # {'server_info':        FileServersInfoForm,
        #  'subscriber':         SubscriberFormFormSet,
        #  'user':               UserForm,
        #  'broker_credentials': BrokerCredentialsFormFormSet}
        #
        # The resulting self.forms dictionary will contain them
        # with instances determined by get_form_kwargs that adds 'instance'
        # key to form kwargs before instantiation
        #

        # Instantiate all the forms in the container
        for form_prefix, form_class in self.form_classes.items():
            #
            # For each pair
            # form_prefix => form_class in form_classes dict
            # a pair is constructed in self.forms dictionary
            # form_prefix => form_class(**kwargs + {'instance': <added by get_form_kwargs>})
            # The instantiated form is with prefix container_prefix "-" form_prefix
            #
            logger.debug("%s; form_prefix, form_class are %s, %s" % ('shree', form_prefix, form_class.__name__))
            self.forms[form_prefix] = form_class(
                prefix='-'.join(p for p in [container_prefix, form_prefix] if p),
                **self.get_form_kwargs(form_prefix, **kwargs)
            )
            logger.debug("%s; forms[%s].prefix = %s" % ('shree', form_prefix, self.forms[form_prefix].prefix))
        logger.debug('%s; self.forms = %s' % ('shree', self.forms))
        pass

    def __unicode__(self):
        "Render all the forms in the container"
        return mark_safe(u''.join([f.as_table() for f in self.forms.values()]))

    def __iter__(self):
        "Return each of the forms in the container"
        for prefix in self.forms:
            yield self[prefix]

    def __getitem__(self, prefix):
        "Return a specific form in the container"
        try:
            form = self.forms[prefix]
        except KeyError:
            raise KeyError('Prefix %r not found in Form container' % prefix)
        return form

    def is_valid(self):
        return all(f.is_valid() for f in self.forms.values())

    @property
    def data(self):
        "Return a compressed dictionary of all data from all subforms"
        all_data = MultiValueDict()
        for prefix, form in self.forms.items():
            for key in form.data:
                all_data.setlist(key, form.data.getlist(key))
        return all_data

    @property
    def files(self):
        "Return a compressed dictionary of all files from all subforms"
        all_files = MultiValueDict()
        for prefix, form in self.forms.items():
            for key in form.files:
                all_files.setlist(key, form.files.getlist(key))
        return all_files

    @property
    def errors(self):
        "Return a compressed dictionary of all errors form all subforms"
        return dict((prefix, form.errors) for prefix, form in self.forms.items())

    @property
    def cleaned_data(self):
        return {
            prefix: form.cleaned_data
            for prefix, form in self.forms.iteritems()
        }

    def save(self, *args, **kwargs):
        "Save each of the subforms"
        r = []
        saved = SortedDict()
        for p, f in self.forms.iteritems():
            logger.debug('%s; saving form %s with cleaned data %s' % ('shree', f.__class__.__name__, f.cleaned_data))
            s = f.save(*args, **kwargs)
            logger.debug('%s; saved form %s' % ('shree', f.__class__.__name__))
            r.append(s)
            saved[p] = s
        # Originally with comprehension
        # r = [f.save(*args, **kwargs) for f in self.forms.values()]
        # return r
        return saved

    def save_m2m(self):
        """Save any related objects -- e.g., m2m entries or inline formsets

        This is needed if the original form collection was saved with commit=False
        """
        for prefix, form in self.forms.items():
            try:
                for subform in form.saved_forms:
                    # Because the related instance wasn't saved at the time the
                    # form was created, the new PK value hasn't propegated to
                    # the inline object on the formset. We need to re-set the
                    # instance to update the _id attribute, which will allow the
                    # inline form instance to save.
                    setattr(subform.instance, form.fk.name, form.instance)
                    subform.instance.save()
            except AttributeError:
                pass

            try:
                form.save_m2m()
            except AttributeError:
                pass
