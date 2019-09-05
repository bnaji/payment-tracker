from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.forms import inlineformset_factory, widgets
from flatpickr import DateTimePickerInput
from webpush import send_user_notification
from django.conf import settings

from .models import Family, Lesson, CustomUser

from .forms import LessonUpdateForm, FamilyForm, CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm


class IndexView(generic.ListView):
    model = Family
    template_name = 'payments/index.html'    
    def get_queryset(self):
        # Check to avoid errors on anonymous user aka not logged in
        if self.request.user.is_authenticated:
            return Family.objects.all().filter(user=self.request.user)
    context_object_name = 'families'

# Use mixin to show a ListView of all lessons of a particular Family
class FamilyDetail(SingleObjectMixin, generic.ListView):
    paginate_by = 10
    model = Family    
    template_name = 'payments/family_detail.html'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Family.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['family'] = self.object
        return context

    def get_queryset(self):
        return self.object.lesson_set.all()

class FamilyList(generic.ListView):
    model = Family
    template_name = 'payments/family.html'
    def get_queryset(self):
        # Check to avoid errors on anonymous user aka not logged in
        if self.request.user.is_authenticated:
            return Family.objects.all().filter(user=self.request.user)
    context_object_name = 'families'

class FamilyCreate(LoginRequiredMixin, CreateView):
    form_class = FamilyForm
    model = Family
    template_name = 'payments/family_form.html'  
    # Override form_valid() to automatically assosiate Logged in User with Family    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class FamilyUpdate(LoginRequiredMixin, UpdateView):
    form_class = FamilyForm
    model = Family
    template_name_suffix = '_update_form'
    
class FamilyDelete(LoginRequiredMixin, DeleteView):
    model = Family
    template_name_suffix = '_confirm_delete'
    success_url = reverse_lazy('payments:family')

def manage_lessons(request, pk):
    family = Family.objects.get(pk=pk)    
    LessonInlineFormSet = inlineformset_factory(
                            Family, 
                            Lesson, 
                            fields=('appt_date', 'status',),
                            widgets={'appt_date': DateTimePickerInput()}, 
                            extra=0,
                            can_delete=False)
    if request.method == "POST":
        formset = LessonInlineFormSet(request.POST, request.FILES, instance=family)
        if formset.is_valid():
            formset.save()
            family.save()
            
            return HttpResponseRedirect(reverse_lazy('payments:family-detail', args=(pk,)))
    else:
        formset = LessonInlineFormSet(instance=family)
    return render(request, 'payments/manage_lessons.html', {'formset': formset})

class LessonUpdate(LoginRequiredMixin, UpdateView):
    form_class = LessonUpdateForm
    model = Lesson
    template_name_suffix = '_update_form' 
    success_url = reverse_lazy('payments:index')
    context_object_name = 'lesson'

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def push_test(request):
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    user = request.user
    return render(request, 'payments/push_template.html', {user: user, 'vapid_key': vapid_key})

# def update_lesson(request, pk):
#     # family = Family.objects.get(pk=pk)
#     lesson = Lesson.objects.get(pk=pk)  
#     if request.method == "POST":
#         form = LessonUpdateForm(request.post)
#         if form.is_valid():
#             form.save()            
#             return HttpResponseRedirect(lesson.get_absolute_url())
#     else:
#         form = LessonUpdateForm()
#     return render(request, 'payments/update_lessons.html', {'form': form})
