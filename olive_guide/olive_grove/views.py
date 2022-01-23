from .models import *
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .forms import *
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.gis.geos import Polygon


class OliveGroveListView(LoginRequiredMixin, ListView):
    model = OliveGrove
    context_object_name = 'olive_groves'
    template_name = 'olive_groves.html'

    def get_queryset(self):
        ogs = OliveGrove.objects.filter(created_by=self.request.user)
        return ogs


class OliveGroveCreateView(LoginRequiredMixin,SuccessMessageMixin,FormView):
    template_name = 'olive_grove_create.html'
    success_message = _("%(name)s was created successfully.")

    def get(self, request, *args, **kwargs):
        form = OliveGroveForm()
        formset = CoordinatesFormSet()
        return self.render_to_response(self.get_context_data(
            form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        form = OliveGroveForm(request.POST)
        formset = CoordinatesFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            coordinates=[]
            for cord_form in formset:
                if cord_form.has_changed():
                    coordinates.append((cord_form.cleaned_data['x'],cord_form.cleaned_data['y']))
            try:
                poly=Polygon(coordinates,)
                poly.srid=2100
                self.object=OliveGrove.objects.create(name=form.cleaned_data['name'],polygon=poly,created_by=self.request.user)
                return super().form_valid(form)
            except:
                return self.render_to_response(self.get_context_data(form=form,formset=formset,message=_("Wrong Coordinates !")))
        else:
            return self.render_to_response(self.get_context_data(form=form,formset=formset))
    
    def get_success_url(self):
        return self.object.get_absolute_url()


class OliveGroveUpdateView(LoginRequiredMixin,SuccessMessageMixin,UserPassesTestMixin,FormView):
    template_name = 'olive_grove_update.html'
    success_message = _("%(name)s was updated successfully.")
    
    def test_func(self):
        olive_grove = self.get_object()
        user = self.request.user
        if olive_grove.created_by==user:
            return True
        return False
    
    def get(self, request, *args, **kwargs):
        form = OliveGroveForm(instance=self.get_object())
        formset = CoordinatesFormSet()
        coordinates=self.get_object().coordinates[0]
        i=0
        for point in coordinates :
            formset[i].fields['x'].initial=point[0]
            formset[i].fields['y'].initial=point[1]
            i+=1
        return self.render_to_response(self.get_context_data(
            form=form, formset=formset, olive_grove=self.get_object()))
    
    def post(self, request, *args, **kwargs):
        form = OliveGroveForm(request.POST)
        formset = CoordinatesFormSet(request.POST)
        if form.is_valid() and formset.is_valid() :
            coordinates=[]
            for cord_form in formset:
                if cord_form.has_changed():
                    coordinates.append((cord_form.cleaned_data['x'],cord_form.cleaned_data['y']))
            try:
                poly=Polygon(coordinates)
                poly.srid=2100
                olive_grove=self.get_object()
                olive_grove.name=form.cleaned_data['name']
                olive_grove.polygon=poly
                olive_grove.created_by=request.user
                olive_grove.save()
                return super().form_valid(form)
            except:
                return self.render_to_response(self.get_context_data(form=form,formset=formset, message=_("Wrong Coordinates !")))
        else:
            return self.render_to_response(self.get_context_data(form=form,formset=formset))
    
    def get_success_url(self):
        return self.get_object().get_absolute_url()
    
    def get_object(self):
        return OliveGrove.objects.get(id=self.kwargs['pk'])

class OliveGroveDetailView(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    model=OliveGrove
    template_name = 'olive_grove_detail.html'
    context_object_name = 'olive_grove'

    def test_func(self):
        olive_grove = self.get_object()
        user = self.request.user
        if olive_grove.created_by==user:
            return True
        return False


class OliveGroveDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=OliveGrove
    context_object_name = 'olive_grove'

    def test_func(self):
        olive_grove = self.get_object()
        user = self.request.user
        if olive_grove.created_by==user:
            return True
        return False

    def get_success_url(self):
        messages.success(self.request, _("Olive Grove was deleted successfully."))
        return reverse('olive_grove:olive_groves')


class NoteCreateView(LoginRequiredMixin,SuccessMessageMixin,UserPassesTestMixin,CreateView):
    model=Note
    template_name = 'note_create.html'
    context_object_name = 'olive_grove'
    form_class=NoteForm
    success_message = _("%(title)s was created successfully.")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.olive_grove=OliveGrove.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def test_func(self):
        olive_grove = OliveGrove.objects.get(id=self.kwargs['pk'])
        user = self.request.user
        if olive_grove.created_by==user:
            return True
        return False

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(NoteCreateView, self).get_context_data(**kwargs)
        context['olive_grove'] =OliveGrove.objects.get(id=self.kwargs['pk'])
        return context


class NoteUpdateView(LoginRequiredMixin,SuccessMessageMixin,UserPassesTestMixin,UpdateView):
    model=Note
    template_name = 'note_update.html'
    form_class=NoteForm
    success_message = _("%(title)s was updated successfully.")

    def test_func(self):
        note = self.get_object()
        user = self.request.user
        if note.created_by==user:
            return True
        return False

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.olive_grove=OliveGrove.objects.get(id=self.kwargs['og_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return self.get_object().get_absolute_url()


class NoteDetailView(LoginRequiredMixin,SuccessMessageMixin,UserPassesTestMixin,DetailView):
    model=Note
    template_name = 'note_detail.html'
    context_object_name = 'note'

    def test_func(self):
        note = self.get_object()
        print(note)
        user = self.request.user
        if note.created_by==user:
            return True
        return False


class NoteDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Note
    context_object_name = 'note'

    def test_func(self):
        note = self.get_object()
        print(note)
        user = self.request.user
        if note.created_by==user:
            return True
        return False

    def get_success_url(self):
        messages.success(self.request, _("Note was deleted successfully."))
        return reverse('olive_grove:olive_grove_detail', kwargs={'pk': self.kwargs['og_id']})