from django.views import generic
from .models import Person, Gift

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.forms import modelformset_factory, inlineformset_factory


class ListPersons(generic.ListView):
    model = Person
    # context_object_name = 'persons'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        persons = context["object_list"]
        new_context = {}
        budget_total = 0
        spent = 0
        budget_used = 0
        for person in persons:
            tmp = {
                'instance': person,
                'bought': person.gift_set.filter(bought=True).count(),
                'wrapped': person.gift_set.filter(wrapped=True).count(),
                'total': person.gift_set.count()
            }
            new_context[person.id] = tmp
            budget_total += person.budget

            gifts = person.gift_set.all()
            total_gifts_price = 0
            for gift in gifts:
                total_gifts_price += gift.price
                if gift.bought:
                    spent += gift.price
            budget_used += total_gifts_price

        context["persons"] = new_context
        context["budget_total"] = budget_total
        context["budget_used"] = budget_used
        context["spent"] = spent
        print(context)
        return context

    def get_queryset(self):
        return Person.objects.all()


class DetailPerson(generic.UpdateView):
    model = Person
    template_name = "gifts/person_detail.html"

    # success_url = reverse_lazy('gifts:listPersons')
    form_class = inlineformset_factory(Person, Gift, fields=('bought', 'wrapped'), extra=0, can_delete=False)

    def get_success_url(self):
        return reverse_lazy('gifts:detailPerson', kwargs={"pk": self.kwargs["pk"]})

    def get_form(self, form_class=None):
        forms = super().get_form(form_class)
        for form in forms:
            form.fields["bought"].widget.attrs.update(
                {'class': 'bought-widget'})
            form.fields["wrapped"].widget.attrs.update(
                {'class': 'wrapped-widget'})
            if not form.instance.bought:
                form.fields["wrapped"].widget.attrs.update({
                    'disabled': True
                })
        return forms

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        print(form.is_valid())
        print(form)
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AddPerson(generic.CreateView):
    model = Person
    template_name = 'gifts/person_create.html'
    success_url = reverse_lazy('gifts:listPersons')

    fields = [
        'name',
        'budget'
    ]


class DeletePerson(generic.DeleteView):
    model = Person
    success_url = reverse_lazy('gifts:listPersons')


class UpdatePerson(generic.UpdateView):
    model = Person
    template_name = 'gifts/person_update.html'

    fields = [
        'name',
        'budget'
    ]

    def get_success_url(self):
        return reverse_lazy('gifts:detailPerson', kwargs={'pk': self.kwargs["pk"]})


class AddGift(generic.CreateView):
    model = Gift
    context_object_name = 'gift'

    fields = [
        'description',
        'price'
    ]

    def form_valid(self, form):
        print("hello")
        for i in self.request.GET:
            print(i, self.request.GET[i])
        p = get_object_or_404(Person, pk=self.kwargs["person"])
        form.instance.person = p
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('gifts:detailPerson', kwargs={"pk": self.kwargs["person"]})


class UpdateGift(generic.UpdateView):
    model = Gift
    template_name = 'gifts/gift_update.html'

    fields = [
        'description',
        'price'
    ]

    def get_success_url(self):
        return reverse_lazy('gifts:detailPerson', kwargs={"pk": self.object.person.id})


class DeleteGift(generic.DeleteView):
    model = Gift

    def get_success_url(self):
        return reverse_lazy('gifts:detailPerson', kwargs={"pk": self.object.person.id})
