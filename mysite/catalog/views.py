# (c) Shahar Gino, December-2018, sgino209@gmail.com
#
# Views creation
# (A view is a function that processes an HTTP request, fetches data from the database as needed, generates an HTML page
#  by rendering this data using an HTML template, and then returns the HTML in an HTTP response to be shown to the user)

from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_text, force_bytes
from django.contrib.auth import login
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from .forms import SignUpForm
from .tokens import account_activation_token

# ---------------------------------------------------------------------------------------------------------------------

def index(request):
    """ View function for home page of site """

    content = {}

    # Generate counts of some of the main objects
    content['num_users'] = User.objects.count()
    content['num_books'] = Book.objects.all().count()
    content['num_instances'] = BookInstance.objects.all().count()
    content['num_instances_available'] = BookInstance.objects.filter(status__exact='a').count()
    content['num_authors'] = Author.objects.count()
    content['num_genres'] = Genre.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    content['num_visits'] = num_visits

    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', content)

# ---------------------------------------------------------------------------------------------------------------------

def signup(request):
    """ SignUp view """

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.username = user.email
            user.save()
            user = User.objects.get(Q(first_name__exact=user.first_name) & Q(last_name__exact=user.last_name))
            user.profile.org_name = form.cleaned_data['org_name']
            user.profile.avatar = request.FILES.get('avatar', None)
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def account_activation_sent(request):
    return render(
        request,
        'index.html',
        {'signup_complete': True}
    )

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')

# ---------------------------------------------------------------------------------------------------------------------

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookCreate(generic.CreateView):
    model = Book
    fields = '__all__'

class BookDetailView(generic.DetailView):
    model = Book

class BookUpdate(generic.UpdateView):
    model = Author
    fields = '__all__'

class BookDelete(generic.DeleteView):
    model = Book
    success_url = reverse_lazy('books')

# ---------------------------------------------------------------------------------------------------------------------
