from django.forms.models import inlineformset_factory
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic.edit import DeleteView, UpdateView, CreateView, DeleteView, FormView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.signing import BadSignature
from django.core.paginator import Paginator
from .models import AdvUser, Exercise, SetDescription, Workout
from .forms import ExerciseFormSet, SearchForm, ChangeUserInfoForm, RegisterUserForm, WorkoutForm
from .utilities import signer


def index(request):
    """Main page"""
    return render(request, 'main/index.html')


def about(request, page):
    """Page with description about the application"""
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


class UserLoginView(LoginView):
    """Login page"""
    template_name = 'main/login.html'


@login_required
def profile(request):
    workouts = Workout.objects.filter(sportsman_name=request.user.pk)
    context = {'workouts': workouts}
    return render(request, 'main/profile.html')


# 5 view classes for account management - logout, change info, registration
class UserLogoutView(LogoutView, LoginRequiredMixin):
    template_name = 'main/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success__url = reverse_lazy('main:index')
    success_message = "Данные пользователя изменены"

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
                             PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:index')
    success_message = "Пароль пользоваталя изменен"


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, "Пользователь удален")
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def all_workouts(request):
    workouts = Workout.objects.filter(
        sportsman_name=request.user).order_by('-created_at')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(name__icontains=keyword) | Q(comment__icontains=keyword)
        workouts = workouts.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(workouts, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'workouts': workouts, 'page': page, 'form': form}
    return render(request, 'main/workouts.html', context)


def workout(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    exercises = Exercise.objects.filter(workout=workout)
    sets = SetDescription.objects.filter(exercise__in=exercises)
    context = {'workout': workout, 'exercises': exercises, 'sets': sets}
    return render(request, 'main/workout_detail.html', context)


@login_required
def workout_delete(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    if request.method == "POST":
        workout.delete()
        messages.add_message(request, messages.SUCCESS, 'Тренировка удалена')
        return redirect('main:workouts')
    else:
        context = {'workout': workout}
        return render(request, 'main/workout_delete.html', context)


class WorkoutList(ListView):
    model = Workout


class WorkoutAdd(LoginRequiredMixin, CreateView):
    model = Workout
    template_name = 'main/workout_add.html'
    fields = ('__all__')

    def get_context_data(self, **kwargs):
        context = super(WorkoutAdd, self).get_context_data(**kwargs)
        if self.request.POST:
            context['exercises'] = ExerciseFormSet(self.request.POST,
                                                   instance=self.object)
        else:
            context['exercises'] = ExerciseFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['exercises']
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super(WorkoutAdd, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(WorkoutAdd, self).get_form_kwargs()
        if kwargs['instance'] is None:
            kwargs['instance'] = Workout()
        kwargs['instance'].sportsman_name = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('main:workouts')
