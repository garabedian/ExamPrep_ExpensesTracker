from django.shortcuts import render, redirect
from main.models import Profile, Expenses
from main.forms import ProfileForm, ExpensesForm, DeleteExpensesForm


# Create your views here.
def index(request):
    if Profile.objects.first():
        budget = Profile.objects.first().budget
        expenses = Expenses.objects.all()
        total_expenses = 0
        prices = []
        for entry in expenses:
            total_expenses += entry.price
            prices.append(f'{entry.price:.2f}')
        context = {
            'profiles': Profile.objects.all(),
            'expenses': expenses,
            'budget': f'{budget:.2f}',
            'left': f'{(budget - total_expenses):.2f}',
            'prices': prices,
        }
        return render(request, 'home-with-profile.html', context)

    if request.method == "GET":
        form = ProfileForm()
        return render(request, 'home-no-profile.html', {'form': form})
    else:
        form = ProfileForm(request.POST)
        if form.is_valid():
            # new_profile = form.save()
            # new_profile.save()
            form.save()
            return redirect('index')
        return render(request, 'home-no-profile.html', {'form': form})


def create_expense(request):
    if request.method == "GET":
        form = ExpensesForm()
        return render(request, 'expense-create.html', {'form': form})
    else:
        form = ExpensesForm(request.POST)
        if form.is_valid():
            # entry = form.save()
            # entry.save()
            form.save()
            return redirect('index')
        return render(request, 'expense-create.html', {'form': form})


def edit_expense(request, pk):
    entry = Expenses.objects.get(pk=pk)
    if request.method == "GET":
        form = ExpensesForm(instance=entry)
        return render(request, 'expense-edit.html', {'form': form})
    else:
        form = ExpensesForm(request.POST, instance=entry)
        if form.is_valid():
            # entry = form.save()
            # entry.save()
            form.save()
            return redirect('index')
        return render(request, 'expense-edit.html', {'form': form})


def delete_expense(request, pk):
    entry = Expenses.objects.get(pk=pk)

    if request.method == "GET":
        # Use this without templated .html
        # return render(request, 'expense-delete.html', {'entry': entry})

        # Use this with templated .html
        entry.price = f'{entry.price:.2f}'
        context = {
            'entry': entry,
            'form': DeleteExpensesForm(instance=entry),
        }
        return render(request, 'expense-delete.html', context)

    entry.delete()
    return redirect('index')


def profile(request):
    users = {
        'user': Profile.objects.first()
    }
    total_expenses = 0
    for entry in Expenses.objects.all():
        total_expenses += entry.price
    users['user'].budget -= total_expenses
    return render(request, 'profile.html', users)


def edit_profile(request):
    user = Profile.objects.first()
    if request.method == "GET":
        form = ProfileForm(instance=user)
        return render(request, 'profile-edit.html', {'form': form})
    else:
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            # user = form.save()
            # user.save()
            form.save()
            return redirect('index')
        return render(request, 'profile-edit.html', {'form': form})


def delete_profile(request):
    if request.method == "GET":
        return render(request, 'profile-delete.html')

    user = Profile.objects.first()
    user.delete()
    for entry in Expenses.objects.all():
        entry.delete()
    return redirect('index')
