from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.forms import modelformset_factory
from django.db.models import Min, Max
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import  reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from post.servises import pythonTelegramBot
from sales.models import Clients
from accounts.utils import DataMixin
from .models import PostChannel, Post, Channels 
from .forms import AddPostForm, AddPostToChannelsForm, PostChannelFormSet, ChannelForm
from accounts.models import CustomUser
from sales.utils import generate_random_string
from transliterate import translit
from django.utils.text import slugify
import datetime

def create_slug(obj, get_slug_with):
    try:
        num = 1
        # Генеруємо базовий slug на основі переданого get_slug_with
        base_slug = slugify(translit(get_slug_with, 'uk', reversed=True))[:255]

        while True:
            random_string = generate_random_string()
            unique_slug = f"{base_slug}-{random_string}"
            
            if not PostChannel.objects.filter(channels_slug=unique_slug).exists():
                break
            num += 1

        obj.channels_slug = unique_slug[:255]
        return obj.save()
    except:
        return print("Не влалось згенерувати слаг")

class ArkhivPosts(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'processing_posts.html'
    title_page = 'Оброблені пости'
    context_object_name = 'posts'
    model = PostChannel
    paginate_by = 500

    def get_queryset(self):
        queryset = PostChannel.objects.filter(
            status_write=True,
        )
        return queryset.order_by('-date_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['previous_title'] = self.title_page 
        return context



def deletPost(request, slug, channel):
        te = PostChannel.objects.get(channels_slug=channel)
        te.delete()
        return redirect('posts:work_posts')



class UpdatePostView(LoginRequiredMixin, DataMixin, UpdateView):
    model = Post
    form_class = AddPostForm
    template_name = 'adpost.html'
    success_url = reverse_lazy('posts:detailPost')
    title_page = 'Внести зміни в пост для'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        # Отримуємо об'єкт Post за slug
        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            raise Http404("Пост не знайдено")
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        self.request.session['previous_title'] = self.title_page + " " + post.username

        # Отримуємо список каналів для форми вибору великої кількості каналів
        channels = Channels.objects.select_related('category').all().order_by('-category__id')
        grouped_channels = {}
        for channel in channels:
                category_name = channel.category.name
                if category_name not in grouped_channels:
                    grouped_channels[category_name] = []
                grouped_channels[category_name].append(channel)

        # Отримуємо всі пов'язані з постом об'єкти PostChannel
        post_channels = PostChannel.objects.filter(post=post)
        
        # Створюємо формсет
        PostChannelFormSet = modelformset_factory(PostChannel, form=AddPostToChannelsForm, extra=1)
        formset = PostChannelFormSet(queryset=post_channels, prefix="postchannel_set",
                                     form_kwargs={'user': self.request.user,})

        
        post = self.get_object()
        sales_data = PostChannel.objects.filter(post__username=post.username).aggregate(
            first_purchase=Min('date_post'),
            last_purchase=Max('date_post')
        )
        post_channels = [v for v in post_channels if isinstance(v.tarif, (int, float)) or (isinstance(v.tarif, str) and v.tarif.strip().replace('.', '', 1).isdigit())]


            # Підрахунок суми, конвертуємо тариф в число
        total_sum = sum(float(v.tarif) for v in post_channels)

        context['grouped_channels'] = grouped_channels
        context['is_update'] = True 
        context['client'] = Clients.objects.filter(social_media=post.username).last()
        context['client_cost'] = PostChannel.objects.filter(post__username=post.username).count()
        context['total_tarif'] = total_sum 
        context['data_the_first_buys'] = sales_data['first_purchase']
        context['data_the_last_buys'] = sales_data['last_purchase']
        context['post'] = post 
        context['formset'] = formset
        context['post_form'] = AddPostForm(instance=post)
        context['title'] = self.title_page + " " + post.username

        return context


    def post(self, request, *args, **kwargs):
        post = self.get_object()  # Отримуємо об'єкт поста
        post_form = AddPostForm(request.POST, request.FILES, instance=post)

        # Створюємо formset і передаємо в нього queryset
        PostChannelFormSet = modelformset_factory(PostChannel, form=AddPostToChannelsForm, extra=1, can_delete=True)
        formset = PostChannelFormSet(request.POST, queryset=PostChannel.objects.filter(post=post), prefix="postchannel_set",
                                     form_kwargs={'user': self.request.user})

        


        if post_form.is_valid() and formset.is_valid():
            # Зберігаємо основний об'єкт поста
            self.object = post_form.save(commit=False)
            self.object.content = CustomUser.objects.get(pk=request.user.id)
            self.object.save()  # Зберігаємо об'єкт поста, щоб у нього був id

            # Прив'язуємо об'єкт поста до кожного об'єкта у формсеті та зберігаємо
            post_channels = formset.save(commit=False)
            for post_channel in post_channels:
                post_channel.post = self.object  # Прив'язуємо об'єкт Post до кожного PostChannel
                post_channel.status_write = False
                post_channel.save()
            
            formset.save_m2m()  # Якщо є зв'язки M2M у формсеті, зберігаємо їх

            # Переадресація на сторінку деталізації поста
            return redirect('posts:view_invoice', slug=self.object.slug)

        # Відображення помилок, якщо є проблеми з формами
        errors_string = "\n".join(
            f"{field}: {', '.join(errors)}"
            for field, errors in post_form.errors.items()
        )
        
        return render(request, self.template_name, {
            'post_form': AddPostForm(instance=post),
            'title': self.title_page + " " + post.username,
            'errors': f"Помилки: {errors_string}",
        })






class AddPostView(LoginRequiredMixin, DataMixin, CreateView):
    template_name = 'adpost.html'
    title_page = 'Додати новий пост'
    model = Post
    form_class = AddPostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_form = AddPostForm()
        self.request.session['previous_title'] = self.title_page 

        channels = Channels.objects.select_related('category').all().order_by('-category__id')
        grouped_channels = {}
        for channel in channels:
                category_name = channel.category.name
                if category_name not in grouped_channels:
                    grouped_channels[category_name] = []
                grouped_channels[category_name].append(channel)
        context['grouped_channels'] = grouped_channels
        # Якщо пост вже існує, передаємо екземпляр поста у формсет
        formset = PostChannelFormSet(user=self.request.user)
        slug = self.kwargs.get('slug')
        client = get_object_or_404(Clients, slug=slug)
        context['is_update'] = False
        context['client'] = client
        sales_data = PostChannel.objects.filter(post__username=client.social_media).aggregate(
            first_purchase=Min('date_post'),
            last_purchase=Max('date_post')
        )

        context['data_the_first_buys'] = sales_data['first_purchase']
        context['data_the_last_buys'] = sales_data['last_purchase']
        context['client_cost'] = PostChannel.objects.filter(post__username=client.social_media).count()
        context['post_form'] = post_form
        context['formset'] = formset
        return context
    
    def post(self, request, *args, **kwargs):
        post_form = self.form_class(request.POST, request.FILES)

        formset = PostChannelFormSet(request.POST, user=request.user)

        if post_form.is_valid() and formset.is_valid():
            # Зберігаємо пост без збереження у базі для прив'язки до формсетів
            self.object = post_form.save(commit=False)
            slug = kwargs.get('slug')
            client = Clients.objects.get(slug=slug)
            self.object.username = client.social_media if client.social_media != "-" else client.phones
            self.object.sales = CustomUser.objects.get(pk=request.user.id)
            self.object.content = None
            self.object.status = False


            if not self.object.slug:
                num = 1
                base_slug = slugify(translit(self.object.username, 'uk', reversed=True))[:255]

                while True:
                    # Генерує унікальний slug з випадковим рядком
                    random_string = generate_random_string()
                    unique_slug = f"{base_slug}-{random_string}"
                    
                    # Перевіряє, чи існує вже такий slug
                    if not Channels.objects.filter(slug=unique_slug).exists():
                        break
                    num += 1

                self.object.slug = unique_slug[:255]  # Обмежити довжину до 255 символів

            # Збереження змін у клієнті та пості
            client.status_id = 3
            client.data_processing = datetime.datetime.now()

            client.save()
            self.object.save()
            # Прив'язка поста до кожної форми у формсеті
            formset.instance = self.object
            post_channels = formset.save(commit=False)

            for post_channel in post_channels:
                # Генеруємо slug, якщо потрібно
                if not post_channel.channels_slug:
                    create_slug(obj=post_channel, get_slug_with=post_channel.channel.name)
                
                post_channel.post = self.object  # Пов'язуємо з основним об'єктом
                post_channel.status_write = False  # Встановлюємо статус
                post_channel.save()

            return redirect(f'/view-invoice/{self.object.slug}/')

        # Відображення помилок, якщо є проблеми з формами
        return render(request, self.template_name, {
            'post_form': post_form,
            'formset': formset,
            'title': self.title_page,
        })


class InvoiceView(LoginRequiredMixin, DataMixin, ListView):
    model = PostChannel
    template_name = "invoice.html"
    context_object_name = "posts"
    title_page = 'Invoice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        post = PostChannel.objects.filter(post__slug=slug).first()

        if post:
            usr = post.post.username
            get_client = Clients.objects.filter(social_media=usr).first()
            if get_client:
                if get_client.data_processing:
                    context['date_now'] = get_client.data_processing.date()
                else:
                    # Оновлюємо поле data_processing, якщо його немає
                    get_client.data_processing = datetime.datetime.now().date()
                    get_client.save()  # Зберігаємо зміни в базі даних
                    context['date_now'] = datetime.datetime.now().date()
            else:
                context['date_now'] = "Дані відсутні"

            context['post_data'] = post
            context['post'] = PostChannel.objects.filter(post__slug=slug)
        else:
            context['date_now'] = "Дані відсутні"
            context['post_data'] = None
            context['post'] = None

        self.request.session['previous_title'] = self.title_page 
        return context

class DetailPost(LoginRequiredMixin, DataMixin, ListView):
    model = Post
    template_name = 'post.html'
    title_page = 'Деталі поста'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        channel_post = self.kwargs.get('id')
        # Отримуємо об'єкт поста за `slug`
        post = get_object_or_404(Post, slug=slug)
        
        # Фільтруємо PostChannel за постом, каналом, датою і часом
        channel_post = PostChannel.objects.get(
            id=channel_post
        )
        formatted_time = channel_post.time_post.strftime("%H:%M")
        # Додаємо дані в контекст
        context['post'] = post
        context['title'] = f"{self.title_page} для каналу {channel_post.channel.name} {channel_post.date_post} о {formatted_time}" if channel_post else self.title_page
        context['channel_post'] = channel_post
        return context


class ChannelsListView(LoginRequiredMixin, DataMixin, ListView):
    model = Channels
    template_name = "ChannelsList.html"
    context_object_name = "channels"
    title_page = 'Підключені канали'

    def get_queryset(self):
        queryset = Channels.objects.all()
        return queryset.order_by('category')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    


class EditorPostView(LoginRequiredMixin, DataMixin, UpdateView):
    model = Post
    form_class = AddPostForm
    template_name = 'editor.html'
    success_url = reverse_lazy('posts:detailPost')
    title_page = 'Запланувати публікацію'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        # Отримуємо об'єкт Post за slug
        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            raise Http404("Пост не знайдено")
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        post_channel_id = self.kwargs.get('post_channel_id')

        self.request.session['previous_title'] = self.title_page + " " + post.username

        # Отримуємо всі пов'язані з постом об'єкти PostChannel
        post_channel = PostChannel.objects.get(post=post, id=post_channel_id)
    
        post = self.get_object()

        context['post_channel'] = post_channel 
        context['post'] = post 
        context['post_form'] = AddPostForm(instance=post)
        context['title'] = self.title_page + " " + post_channel.channel.name

        return context


    def post(self, request, *args, **kwargs):
        post = self.get_object()  # Отримуємо об'єкт поста
        post_form = AddPostForm(request.POST, request.FILES, instance=post)

        # Створюємо formset і передаємо в нього queryset
        PostChannelFormSet = modelformset_factory(PostChannel, form=AddPostToChannelsForm, extra=1, can_delete=True)
        formset = PostChannelFormSet(request.POST, queryset=PostChannel.objects.filter(post=post), prefix="postchannel_set",
                                     form_kwargs={'user': self.request.user})

        


        if post_form.is_valid() and formset.is_valid():
            # Зберігаємо основний об'єкт поста
            self.object = post_form.save(commit=False)
            self.object.content = CustomUser.objects.get(pk=request.user.id)
            self.object.save()  # Зберігаємо об'єкт поста, щоб у нього був id

            # Прив'язуємо об'єкт поста до кожного об'єкта у формсеті та зберігаємо
            post_channels = formset.save(commit=False)
            for post_channel in post_channels:
                post_channel.post = self.object  # Прив'язуємо об'єкт Post до кожного PostChannel
                post_channel.status_write = False
                post_channel.save()
            
            formset.save_m2m()  # Якщо є зв'язки M2M у формсеті, зберігаємо їх

            # Переадресація на сторінку деталізації поста
            return redirect('posts:view_invoice', slug=self.object.slug)

        # Відображення помилок, якщо є проблеми з формами
        errors_string = "\n".join(
            f"{field}: {', '.join(errors)}"
            for field, errors in post_form.errors.items()
        )
        
        return render(request, self.template_name, {
            'post_form': AddPostForm(instance=post),
            'title': self.title_page + " " + post.username,
            'errors': f"Помилки: {errors_string}",
        })



def ChangeChannel(request, channel_id):
    channel = get_object_or_404(Channels, id=channel_id)

    if request.method == 'POST':
        form = ChannelForm(request.POST, instance=channel)
        if form.is_valid():
            channel_instance = form.save(commit=False) 
            channel_instance.save()  

            return JsonResponse({'success': True, 'message': 'Інформацію про канал оновлено успішно!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ChannelForm(instance=channel)
        return render(request, 'edit_channel_form.html', {'form': form})


def AddChannel(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            channel_instance = form.save(commit=False) 
            channel_instance.save()  

            return JsonResponse({'success': True, 'message': 'Канал успішно додано!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ChannelForm()
        return render(request, 'edit_channel_form.html', {'form': form})


def GetPostInfo(request,channel_id):
    if request.method == 'GET':
        post = get_object_or_404(PostChannel, id=channel_id)
        return render(request, 'post_info.html', {'post': post})


    



def DeleteChannel(request, channel_id):
    channel = get_object_or_404(Channels, id=channel_id)
    channel.delete()
    return JsonResponse({'success': True})





# GET 

def check_time(request):
    channel_id = request.GET.get('channel_id')
    time_post = request.GET.get('time_post')
    date_post = request.GET.get('date_post')

    
    if channel_id and time_post:
        exists = PostChannel.objects.filter(channel_id=channel_id, time_post=time_post, date_post=date_post).exists()
        if exists:
            channel_name = PostChannel.objects.get(channel_id=channel_id, time_post=time_post, date_post=date_post).channel.name
            return JsonResponse({'exists': True, 'channel_name': channel_name})
    return JsonResponse({'exists': False})






### WORK HERE

def save_to_avtoposting(request, post_chanel_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        post_channel = PostChannel.objects.get(id = post_chanel_id)

        post = post_channel.post
        post.posts_text = content
        post_channel.status_write = True
        post_channel.content_update = request.user
        post.save()
        post_channel.save()
        # HERE
        pythonTelegramBot()

    return redirect('posts:arkhiv_posts')





def delete_to_avtoposting(request, post_chanel_id):
    if request.method == 'POST':
        post_channel = PostChannel.objects.get(id = post_chanel_id)
        post_channel.status_write = False
        post_channel.content_update = request.user
        post_channel.save()
        # HERE
        print(post_channel.channel) # object channel - pk to model Channels 
        print(post_channel.time_post) # datetime
        print(post_channel.date_post) # datetime

        pythonTelegramBot()

    return redirect('posts:arkhiv_posts')